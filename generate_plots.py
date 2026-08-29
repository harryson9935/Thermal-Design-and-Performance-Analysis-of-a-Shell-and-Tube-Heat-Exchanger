import numpy as np
import matplotlib.pyplot as plt
import csv
import json

datadir = "/home/claude/hx_project/data"
outdir = "/home/claude/hx_project/outputs"
plt.rcParams.update({"font.size": 10, "figure.dpi": 150})

with open(f"{datadir}/process_spec.json") as f:
    P = json.load(f)
with open(f"{datadir}/design_comparison.json") as f:
    C = json.load(f)
base = C["baseline"]; opt = C["optimized"]; imp = C["improvement"]

rows = list(csv.DictReader(open(f"{datadir}/optimization_sweep.csv")))
for r in rows:
    for k in r:
        if k not in ("layout",):
            r[k] = float(r[k])

# ------------------------------------------------------------------
# 1. Temperature profile along exchanger length (counter-current, using
#    NTU/effectiveness-style linear-in-UA marching, standard for a
#    counter-current HX with ~constant U along the length)
# ------------------------------------------------------------------
Q = P["Q_W"]; m_hot = P["m_hot_kgs"]; Th_in = P["Th_in_C"]; Th_out = P["Th_out_C"]
m_cold = P["m_cold_kgs"]; Tc_in = P["Tc_in_C"]; Tc_out = P["Tc_out_C"]
cp_hot, cp_cold = 2500.0, 4180.0

N = 200
Cr_hot = m_hot*cp_hot
Cr_cold = m_cold*cp_cold
UA_total = Q/P["LMTD_countercurrent_C"]   # idealized pure counter-current UA (uncorrected by F)
x = np.linspace(0, 1, N)  # fractional position, x=0 at cold-inlet/hot-outlet end

# Exact analytic counter-current profile (constant U, Cr assumption):
# Th(u) - Tc(u) = dT0 * exp(k*u),  k = 1/Cr_hot - 1/Cr_cold
u = x*UA_total
dT0 = Th_out - Tc_in
k = 1.0/Cr_hot - 1.0/Cr_cold
if abs(k) < 1e-9:
    Th = Th_out + dT0*u/Cr_hot
    Tc = Tc_in + dT0*u/Cr_cold
else:
    Th = Th_out + (dT0/(Cr_hot*k))*(np.exp(k*u) - 1)
    Tc = Tc_in + (dT0/(Cr_cold*k))*(np.exp(k*u) - 1)
print(f"Profile check: Th(L)={Th[-1]:.2f} (expect {Th_in}), Tc(L)={Tc[-1]:.2f} (expect {Tc_out})")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(x*P["L_tube_m"], Th, color="#c0392b", linewidth=2.2, label="Hot oil (shell side)")
ax.plot(x*P["L_tube_m"], Tc, color="#1f4e79", linewidth=2.2, label="Cold water (tube side)")
ax.fill_between(x*P["L_tube_m"], Th, Tc, color="#f0e6d2", alpha=0.5, label="Local $\\Delta T$")
ax.set_xlabel("Position along exchanger, tube-pass length (m)")
ax.set_ylabel("Temperature (\u00b0C)")
ax.set_title("Counter-Current Temperature Profile\n(Hot oil 150\u2192100\u00b0C | Cold water 30\u219270\u00b0C)")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{outdir}/01_temperature_profile.png")
plt.close()

# ------------------------------------------------------------------
# 2. U and pressure drop vs baffle spacing (parametric trade-off)
# ------------------------------------------------------------------
tri125 = [r for r in rows if r["layout"] == "triangular" and r["pitch_ratio"] == 1.25]
tri125.sort(key=lambda r: r["baffle_ratio"])
br = [r["baffle_ratio"] for r in tri125]
U_ = [r["U"] for r in tri125]
dp_ = [r["dP_shell_kPa"] for r in tri125]

fig, ax1 = plt.subplots(figsize=(7.2, 4.5))
ax1.plot(br, U_, color="#1f4e79", marker="o", markersize=3, linewidth=2, label="Overall U")
ax1.set_xlabel("Baffle spacing ratio, B/Ds")
ax1.set_ylabel("Overall U (W/m$^2$K)", color="#1f4e79")
ax1.tick_params(axis='y', labelcolor="#1f4e79")
ax2 = ax1.twinx()
ax2.plot(br, dp_, color="#c0392b", marker="s", markersize=3, linewidth=2, linestyle="--", label="Shell-side $\\Delta P$")
ax2.axhline(70, color="#c0392b", linestyle=":", linewidth=1)
ax2.text(0.22, 72, "70 kPa allowable limit", color="#c0392b", fontsize=8)
ax2.set_ylabel("Shell-side pressure drop (kPa)", color="#c0392b")
ax2.tick_params(axis='y', labelcolor="#c0392b")
ax1.axvline(1.0, color="gray", linestyle=":", linewidth=1)
ax1.axvline(opt["baffle_ratio"], color="green", linestyle=":", linewidth=1.5)
ax1.annotate("Baseline\n(B/Ds=1.00)", xy=(1.0, base["U"]), xytext=(0.85, base["U"]+120),
             fontsize=8, ha="center")
ax1.annotate("Optimized\n(B/Ds=%.2f)" % opt["baffle_ratio"], xy=(opt["baffle_ratio"], opt["U"]),
             xytext=(opt["baffle_ratio"]-0.05, opt["U"]+130), fontsize=8, ha="center", color="green")
ax1.set_title("Heat-Transfer / Pressure-Drop Trade-off vs Baffle Spacing\n(triangular pitch, Pt/do = 1.25)")
plt.tight_layout()
plt.savefig(f"{outdir}/02_baffle_tradeoff.png")
plt.close()

# ------------------------------------------------------------------
# 3. Effect of tube layout & pitch ratio on U (at the chosen baffle ratio)
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.5))
colors = {"triangular": "#1f4e79", "square": "#c0392b"}
markers = {1.25: "o", 1.33: "s", 1.50: "^"}
for layout in ["triangular", "square"]:
    for ptr in [1.25, 1.33, 1.50]:
        sub = [r for r in rows if r["layout"] == layout and r["pitch_ratio"] == ptr]
        sub.sort(key=lambda r: r["baffle_ratio"])
        ax.plot([r["baffle_ratio"] for r in sub], [r["U"] for r in sub],
                color=colors[layout], marker=markers[ptr], markersize=3, linewidth=1.5,
                label=f"{layout}, Pt/do={ptr}")
ax.set_xlabel("Baffle spacing ratio, B/Ds")
ax.set_ylabel("Overall U (W/m$^2$K)")
ax.set_title("Effect of Tube Layout & Pitch Ratio on Overall U")
ax.legend(fontsize=7, ncol=2)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{outdir}/03_layout_pitch_study.png")
plt.close()

# ------------------------------------------------------------------
# 4. Baseline vs Optimized comparison bar chart
# ------------------------------------------------------------------
metrics = ["U", "A_provided", "dP_shell_Pa", "Nt"]
labels = ["Overall U\n(W/m$^2$K)", "Heat-transfer\narea (m$^2$)", "Shell $\\Delta P$\n(kPa)", "Tube count"]
base_vals = [base["U"], base["A_provided"], base["dP_shell_Pa"]/1000, base["Nt"]]
opt_vals = [opt["U"], opt["A_provided"], opt["dP_shell_Pa"]/1000, opt["Nt"]]

fig, axs = plt.subplots(1, 4, figsize=(11, 4))
for i, (lbl, bv, ov) in enumerate(zip(labels, base_vals, opt_vals)):
    axs[i].bar(["Baseline", "Optimized"], [bv, ov], color=["#95a5a6", "#27ae60"])
    axs[i].set_title(lbl, fontsize=9)
    pct = (ov/bv - 1)*100
    axs[i].text(0.5, max(bv, ov)*1.05, f"{pct:+.1f}%", ha="center", fontsize=9, fontweight="bold")
    axs[i].set_ylim(0, max(bv, ov)*1.25)
fig.suptitle("Baseline vs Optimized Shell-and-Tube HX Design", fontsize=12)
plt.tight_layout()
plt.savefig(f"{outdir}/04_baseline_vs_optimized.png")
plt.close()

# ------------------------------------------------------------------
# 5. LMTD / correction factor diagram (temperature vs heat duty fraction)
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.3))
qfrac = np.linspace(0, 1, 100)
Th_line = Th_out + qfrac*(Th_in - Th_out)
Tc_line = Tc_in + qfrac*(Tc_out - Tc_in)
ax.plot(qfrac*100, Th_line, color="#c0392b", linewidth=2, label="Hot oil")
ax.plot(qfrac*100, Tc_line, color="#1f4e79", linewidth=2, label="Cold water")
ax.set_xlabel("Heat duty transferred (%)")
ax.set_ylabel("Temperature (\u00b0C)")
ax.set_title(f"Temperature-Duty Diagram\nLMTD (counter-current) = {P['LMTD_countercurrent_C']:.1f} \u00b0C, "
             f"F = {P['F']:.3f}")
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{outdir}/05_lmtd_diagram.png")
plt.close()

print("All figures saved to", outdir)
