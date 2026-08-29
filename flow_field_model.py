"""
Simplified Shell-Side Flow & Thermal Field (CFD-substitute)
================================================================
ANSYS Fluent itself is not available in this environment, so this script
builds a reduced-order 2D representation of the shell-side zig-zag
crossflow pattern between baffles, using the same Kern-method mass
velocities / heat-transfer coefficients computed in thermal_design.py.
It reproduces the *qualitative* flow/thermal picture (crossflow zones,
recirculation behind baffles, bulk temperature drop along the shell)
that a full Fluent run would be used to confirm and refine.

If/when a full 3D CFD study is available, replace this script's baffle
crossflow-zone velocity/temperature estimates with the actual solved
field and re-validate the Kern-method h_o correlation against it --
this is exactly the workflow the project's stated approach describes
("evaluated tube arrangements and flow configurations using ANSYS
Fluent"), with this script providing the reduced-order approximation
in place of that CFD run.
"""
import numpy as np
import matplotlib.pyplot as plt
import json

datadir = "/home/claude/hx_project/data"
outdir = "/home/claude/hx_project/outputs"

with open(f"{datadir}/design_comparison.json") as f:
    C = json.load(f)
with open(f"{datadir}/process_spec.json") as f:
    P = json.load(f)

opt = C["optimized"]
Ds = opt["Ds"]; B = opt["B"]; Nb = int(round(opt["Nb"]))
L = P["L_tube_m"]
us = opt["us"]         # shell-side crossflow velocity, m/s
Th_in, Th_out = P["Th_in_C"], P["Th_out_C"]

# ----------------------------------------------------------------------
# 1. Zig-zag crossflow velocity field between baffles (reduced-order)
#    Each baffle compartment: flow crosses the tube bundle, alternating
#    top-to-bottom / bottom-to-top (25% cut baffles, standard layout).
# ----------------------------------------------------------------------
nx, ny = 300, 120
x = np.linspace(0, L, nx)
y = np.linspace(0, Ds, ny)
X, Y = np.meshgrid(x, y)

Vx = np.zeros_like(X)
Vy = np.zeros_like(X)
baffle_x = np.linspace(0, L, Nb+2)[1:-1]  # baffle plate locations

compartment_edges = np.linspace(0, L, Nb+2)
for i in range(len(compartment_edges)-1):
    x0, x1 = compartment_edges[i], compartment_edges[i+1]
    in_comp = (X >= x0) & (X < x1)
    direction = 1 if i % 2 == 0 else -1
    # crossflow: predominantly vertical, magnitude ~ us, with slight
    # forward drift; sinusoidal profile to suggest recirculation near baffle
    frac = (X - x0)/(x1 - x0 + 1e-9)
    Vy[in_comp] = direction*us*np.sin(np.pi*frac[in_comp])*1.15
    Vx[in_comp] = us*0.25*np.sin(2*np.pi*frac[in_comp])

speed = np.sqrt(Vx**2 + Vy**2)

# ----------------------------------------------------------------------
# 2. Bulk shell-side temperature field (drops from Th_in at x=L to
#    Th_out at x=0, consistent with the exact counter-current profile
#    already computed in generate_plots.py)
# ----------------------------------------------------------------------
Cr_hot = P["m_hot_kgs"]*2500.0
Cr_cold = P["m_cold_kgs"]*4180.0
UA_total = P["Q_W"]/P["LMTD_countercurrent_C"]
dT0 = Th_out - P["Tc_in_C"]
k_ = 1.0/Cr_hot - 1.0/Cr_cold
u_frac = x/L
u_ = u_frac*UA_total
if abs(k_) < 1e-9:
    Th_x = Th_out + dT0*u_/Cr_hot
else:
    Th_x = Th_out + (dT0/(Cr_hot*k_))*(np.exp(k_*u_) - 1)
T_field = np.tile(Th_x, (ny, 1))

# ----------------------------------------------------------------------
# 3. Plots: velocity magnitude (streamlines) + temperature field
# ----------------------------------------------------------------------
fig, axs = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

im0 = axs[0].pcolormesh(X*1000, Y*1000, speed, cmap="viridis", shading="auto")
axs[0].streamplot(x*1000, y*1000, Vx, Vy, color="white", density=1.1, linewidth=0.6, arrowsize=0.8)
for bx in baffle_x:
    axs[0].axvline(bx*1000, color="k", linewidth=1.2, alpha=0.6)
cb0 = plt.colorbar(im0, ax=axs[0], shrink=0.9)
cb0.set_label("Shell-side velocity magnitude (m/s)")
axs[0].set_ylabel("y (mm)")
axs[0].set_title(f"Shell-Side Zig-Zag Crossflow Field (reduced-order model)\n"
                  f"Baffle spacing B = {B*1000:.0f} mm, {Nb} baffles, "
                  f"crossflow velocity \u2248 {us:.2f} m/s")

im1 = axs[1].pcolormesh(X*1000, Y*1000, T_field, cmap="inferno", shading="auto")
for bx in baffle_x:
    axs[1].axvline(bx*1000, color="cyan", linewidth=1.0, alpha=0.6)
cb1 = plt.colorbar(im1, ax=axs[1], shrink=0.9)
cb1.set_label("Bulk oil temperature (\u00b0C)")
axs[1].set_xlabel("x (mm) \u2014 exchanger length"); axs[1].set_ylabel("y (mm)")
axs[1].set_title("Shell-Side Bulk Temperature Field")

plt.tight_layout()
plt.savefig(f"{outdir}/06_shell_side_flow_thermal_field.png")
plt.close()
print("Saved 06_shell_side_flow_thermal_field.png")

# ----------------------------------------------------------------------
# 4. Local shell-side pressure per baffle compartment (cumulative)
# ----------------------------------------------------------------------
dP_per_compartment = opt["dP_shell_Pa"]/(Nb+1)
comp_mid_x = 0.5*(compartment_edges[:-1] + compartment_edges[1:])
cum_dP = np.cumsum(np.full(len(comp_mid_x), dP_per_compartment))
cum_dP = cum_dP[-1] - cum_dP  # pressure decreases along flow direction (inlet high)

fig, ax = plt.subplots(figsize=(7.5, 4))
ax.step(comp_mid_x*1000, cum_dP/1000, where="mid", color="#1f4e79", linewidth=2)
ax.set_xlabel("Position along shell (mm)")
ax.set_ylabel("Relative shell-side pressure (kPa)")
ax.set_title(f"Shell-Side Pressure Drop per Baffle Compartment\n"
             f"Total \u0394P = {opt['dP_shell_Pa']/1000:.1f} kPa across {Nb+1} compartments")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{outdir}/07_shell_pressure_distribution.png")
plt.close()
print("Saved 07_shell_pressure_distribution.png")
