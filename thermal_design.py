"""
Thermal Design of a Shell-and-Tube Heat Exchanger (Kern's Method)
====================================================================
Recovers thermal energy from a hot process stream (hot oil) into a cold
water stream. Performs:
  1. Heat duty, LMTD, and correction factor (1 shell pass / 2 tube passes)
  2. Iterative sizing: tube count, bundle/shell diameter (Kern/Sinnott
     bundle-diameter correlation), tube-side & shell-side film
     coefficients, overall U (converged), required area, overdesign
  3. Tube-side pressure drop (Dittus-Boelter + friction/return losses)
  4. Shell-side pressure drop (Kern method, baffled cross-flow)

All correlations are standard, widely published shell-and-tube design
correlations (Kern / Sinnott "Chemical Engineering Design"), implemented
here from the governing equations -- not copied text.
"""
import numpy as np
import json
import csv
import os

# ----------------------------------------------------------------------
# 1. PROCESS SPECIFICATION
# ----------------------------------------------------------------------
# Hot stream: process oil (waste-heat recovery source)
m_hot = 4.5          # kg/s
Th_in = 150.0         # deg C
Th_out = 100.0        # deg C
cp_hot = 2500.0        # J/kg.K (light process oil)
rho_hot = 830.0        # kg/m^3
mu_hot = 3.0e-3        # Pa.s  (at mean bulk temp, representative)
k_hot = 0.135          # W/m.K
Pr_hot = cp_hot*mu_hot/k_hot

# Cold stream: water (energy recovery sink, e.g. preheat / process water)
Tc_in = 30.0
cp_cold = 4180.0
rho_cold = 985.0        # kg/m^3 (mean temp ~45 C)
mu_cold = 6.0e-4         # Pa.s
k_cold = 0.635           # W/m.K
Pr_cold = cp_cold*mu_cold/k_cold

# ----------------------------------------------------------------------
# 2. HEAT DUTY, MASS BALANCE, LMTD
# ----------------------------------------------------------------------
Q = m_hot*cp_hot*(Th_in - Th_out)     # W

Tc_out_target = 70.0
m_cold = Q/(cp_cold*(Tc_out_target - Tc_in))
Tc_out = Tc_out_target

dT1 = Th_in - Tc_out     # counter-current end differences
dT2 = Th_out - Tc_in
LMTD_cf = (dT1 - dT2)/np.log(dT1/dT2)

# Correction factor F for 1 shell pass / 2 (or multiple of 2) tube passes
R = (Th_in - Th_out)/(Tc_out - Tc_in)
P = (Tc_out - Tc_in)/(Th_in - Tc_in)

def F_correction(R, P):
    if abs(R - 1.0) < 1e-6:
        num = np.sqrt(2)*(1-P)/P
        den = np.log((2-P*(2-np.sqrt(2)))/(2-P*(2+np.sqrt(2))))
        return num/den if den != 0 else 1.0
    sq = np.sqrt(R**2+1)
    num = sq*np.log((1-P)/(1-P*R))
    den = (R-1)*np.log((2-P*(R+1-sq))/(2-P*(R+1+sq)))
    return num/den

F = F_correction(R, P)
LMTD_corrected = F*LMTD_cf

print(f"Heat duty Q            : {Q/1000:.1f} kW")
print(f"Cold water flow rate   : {m_cold:.3f} kg/s")
print(f"Counter-current LMTD   : {LMTD_cf:.2f} C")
print(f"R = {R:.3f}, P = {P:.3f}, F = {F:.4f}")
print(f"Corrected MTD (F*LMTD) : {LMTD_corrected:.2f} C")

# ----------------------------------------------------------------------
# 3. TUBE / LAYOUT GEOMETRY (fixed mechanical standards)
# ----------------------------------------------------------------------
do = 0.01905          # tube OD, m (3/4 in)
BWG_thk = 0.00165      # wall thickness, m (16 BWG)
di = do - 2*BWG_thk
L_tube = 4.88          # tube length, m (16 ft)
k_wall = 50.0           # W/m.K, carbon steel tube wall

Rfi = 0.0002           # fouling resistance tube side (water), m^2.K/W
Rfo = 0.0003           # fouling resistance shell side (oil), m^2.K/W

def bundle_diameter(Nt, do, layout="triangular", passes=2):
    # Kern/Sinnott correlation: Db = do*(Nt/K1)^(1/n1)
    table = {
        ("triangular", 1): (0.319, 2.142),
        ("triangular", 2): (0.249, 2.207),
        ("triangular", 4): (0.175, 2.285),
        ("square", 1): (0.215, 2.207),
        ("square", 2): (0.156, 2.291),
        ("square", 4): (0.158, 2.263),
    }
    K1, n1 = table[(layout, passes)]
    return do*(Nt/K1)**(1/n1)

def shell_clearance(Db):
    # representative pull-through floating-head bundle-shell clearance (m)
    return 0.05 if Db < 0.6 else 0.07

# ----------------------------------------------------------------------
# 4. ITERATIVE THERMAL/HYDRAULIC DESIGN
# ----------------------------------------------------------------------
def design_hx(U_guess, pt_ratio=1.25, layout="triangular", passes=2,
              baffle_ratio=0.4, baffle_cut=0.25):
    """Full Kern-method design for a given assumed U (W/m2K),
    tube pitch ratio (pt/do), layout, tube passes, and baffle spacing
    ratio (B/Ds). Returns a dict of the converged design."""
    pt = pt_ratio*do

    for _ in range(60):
        A_req = Q/(U_guess*LMTD_corrected)
        Nt = max(4, round(A_req/(np.pi*do*L_tube)))
        # round to even number per pass for clean layout
        Nt = int(np.ceil(Nt/passes)*passes)

        Db = bundle_diameter(Nt, do, layout, passes)
        clearance = shell_clearance(Db)
        Ds = Db + clearance

        # ---- Tube-side film coefficient (Dittus-Boelter, heating) ----
        tubes_per_pass = Nt/passes
        Ai_flow = tubes_per_pass*(np.pi/4)*di**2
        v_tube = m_cold/(rho_cold*Ai_flow)
        Re_tube = rho_cold*v_tube*di/mu_cold
        Nu_tube = 0.023*Re_tube**0.8*Pr_cold**0.4
        hi = Nu_tube*k_cold/di
        hi_o = hi*(di/do)   # referred to outside area

        # ---- Shell-side film coefficient (Kern method) ----
        C = pt - do                      # clearance between tubes
        B = baffle_ratio*Ds               # baffle spacing
        As = (Ds*C*B)/pt                  # cross-flow area
        Gs = m_hot/As
        if layout == "triangular":
            de = 1.10/do*(pt**2 - 0.917*do**2)
        else:
            de = 1.27/do*(pt**2 - 0.785*do**2)
        Re_shell = Gs*de/mu_hot
        Nu_shell = 0.36*Re_shell**0.55*Pr_hot**(1/3)
        ho = Nu_shell*k_hot/de

        # ---- Overall U (based on outside area) ----
        U_new = 1.0/(1/ho + Rfo + do*np.log(do/di)/(2*k_wall) +
                     Rfi*(do/di) + (do/di)/hi)

        if abs(U_new - U_guess)/U_guess < 1e-4:
            U_guess = U_new
            break
        U_guess = 0.5*U_guess + 0.5*U_new  # relaxed update

    A_provided = Nt*np.pi*do*L_tube
    A_required_final = Q/(U_guess*LMTD_corrected)
    overdesign_pct = (A_provided/A_required_final - 1)*100

    # ---- Tube-side pressure drop ----
    f_tube = (1.82*np.log10(Re_tube) - 1.64)**-2   # Darcy friction factor
    dP_tube_friction = passes*(f_tube*(L_tube/di))*rho_cold*v_tube**2/2
    dP_tube_return = passes*4*(rho_cold*v_tube**2/2)   # ~4 velocity heads/pass
    dP_tube = dP_tube_friction + dP_tube_return

    # ---- Shell-side pressure drop (Kern) ----
    jf = 0.72*Re_shell**-0.238  # approximate Kern friction-factor curve fit
    us = Gs/rho_hot
    Nb = L_tube/B - 1  # number of baffles
    dP_shell = 8*jf*(Ds/de)*(L_tube/B)*(rho_hot*us**2/2)

    return {
        "U": U_guess, "A_required": A_required_final, "A_provided": A_provided,
        "overdesign_pct": overdesign_pct, "Nt": Nt, "Ds": Ds, "Db": Db,
        "hi": hi, "hi_o": hi_o, "ho": ho, "Re_tube": Re_tube, "Re_shell": Re_shell,
        "v_tube": v_tube, "us": us, "dP_tube_Pa": dP_tube, "dP_shell_Pa": dP_shell,
        "B": B, "Nb": Nb, "pt": pt, "layout": layout, "passes": passes,
        "baffle_ratio": baffle_ratio, "pt_ratio": pt_ratio
    }

# ----------------------------------------------------------------------
# 5. BASELINE DESIGN
# ----------------------------------------------------------------------
baseline = design_hx(U_guess=400.0, pt_ratio=1.25, layout="triangular",
                      passes=2, baffle_ratio=0.5)

print("\n--- BASELINE DESIGN (B/Ds = 0.50) ---")
for k_, v_ in baseline.items():
    if isinstance(v_, float):
        print(f"{k_:16s}: {v_:.4g}")
    else:
        print(f"{k_:16s}: {v_}")

# ----------------------------------------------------------------------
# 6. SAVE
# ----------------------------------------------------------------------
datadir = "/home/claude/hx_project/data"
os.makedirs(datadir, exist_ok=True)

process = {
    "Q_W": Q, "m_hot_kgs": m_hot, "Th_in_C": Th_in, "Th_out_C": Th_out,
    "m_cold_kgs": m_cold, "Tc_in_C": Tc_in, "Tc_out_C": Tc_out,
    "LMTD_countercurrent_C": LMTD_cf, "R": R, "P": P, "F": F,
    "LMTD_corrected_C": LMTD_corrected,
    "do_m": do, "di_m": di, "L_tube_m": L_tube
}
with open(f"{datadir}/process_spec.json", "w") as fjson:
    json.dump(process, fjson, indent=2)
with open(f"{datadir}/baseline_design.json", "w") as fjson:
    json.dump(baseline, fjson, indent=2)

print("\nSaved process_spec.json and baseline_design.json")
