%% =======================================================================
%  Thermal Design & Optimization of a Shell-and-Tube Heat Exchanger
%  (MATLAB port of thermal_design.py / optimization_study.py)
%  =======================================================================
%  Method: Kern's method, iterative U convergence, parametric sweep over
%  baffle spacing / tube pitch / layout for a baseline-vs-optimized study.
%  Base MATLAB only (no toolboxes required).
% =========================================================================
clear; clc; close all;

%% ---------------------------------------------------------------------
%  1. PROCESS SPECIFICATION
%  ---------------------------------------------------------------------
m_hot = 4.5; Th_in = 150.0; Th_out = 100.0;
cp_hot = 2500.0; rho_hot = 830.0; mu_hot = 3.0e-3; k_hot = 0.135;
Pr_hot = cp_hot*mu_hot/k_hot;

Tc_in = 30.0; Tc_out_target = 70.0;
cp_cold = 4180.0; rho_cold = 985.0; mu_cold = 6.0e-4; k_cold = 0.635;
Pr_cold = cp_cold*mu_cold/k_cold;

Q = m_hot*cp_hot*(Th_in - Th_out);
m_cold = Q/(cp_cold*(Tc_out_target - Tc_in));
Tc_out = Tc_out_target;

dT1 = Th_in - Tc_out; dT2 = Th_out - Tc_in;
LMTD_cf = (dT1 - dT2)/log(dT1/dT2);

R = (Th_in - Th_out)/(Tc_out - Tc_in);
P = (Tc_out - Tc_in)/(Th_in - Tc_in);
sq = sqrt(R^2+1);
Fc = sq*log((1-P)/(1-P*R)) / ((R-1)*log((2-P*(R+1-sq))/(2-P*(R+1+sq))));
LMTD_corr = Fc*LMTD_cf;

fprintf('Q = %.1f kW, m_cold = %.3f kg/s, LMTD = %.2f C, F = %.4f, corrected MTD = %.2f C\n', ...
    Q/1000, m_cold, LMTD_cf, Fc, LMTD_corr);

%% ---------------------------------------------------------------------
%  2. GEOMETRY CONSTANTS
%  ---------------------------------------------------------------------
do = 0.01905; BWG_thk = 0.00165; di = do - 2*BWG_thk;
L_tube = 4.88; k_wall = 50.0;
Rfi = 0.0002; Rfo = 0.0003;

%% ---------------------------------------------------------------------
%  3. DESIGN FUNCTION (Kern method, iterative)
%  ---------------------------------------------------------------------
% design_hx(U_guess, pt_ratio, layout, passes, baffle_ratio) -> struct
% (see local function at bottom of file)

baseline = design_hx(400.0, 1.25, "triangular", 2, 1.00, ...
    Q, LMTD_corr, do, di, L_tube, k_wall, Rfi, Rfo, ...
    m_cold, rho_cold, mu_cold, k_cold, Pr_cold, ...
    m_hot, rho_hot, mu_hot, k_hot, Pr_hot);

fprintf('\n--- BASELINE (B/Ds=1.00) ---\n');
fprintf('U = %.1f W/m2K, A = %.2f m2, dP_shell = %.1f kPa, dP_tube = %.1f kPa, Nt = %d\n', ...
    baseline.U, baseline.A_provided, baseline.dP_shell_Pa/1000, baseline.dP_tube_Pa/1000, baseline.Nt);

%% ---------------------------------------------------------------------
%  4. PARAMETRIC SWEEP
%  ---------------------------------------------------------------------
baffle_ratios = 0.20:0.05:1.00;
pitch_ratios = [1.25, 1.33, 1.50];
layouts = ["triangular", "square"];

results = struct('layout', {}, 'pitch_ratio', {}, 'baffle_ratio', {}, ...
                  'U', {}, 'A_provided', {}, 'dP_shell_kPa', {}, 'dP_tube_kPa', {});
idx = 1;
for li = 1:numel(layouts)
    for pi_ = 1:numel(pitch_ratios)
        for bi = 1:numel(baffle_ratios)
            d = design_hx(400.0, pitch_ratios(pi_), layouts(li), 2, baffle_ratios(bi), ...
                Q, LMTD_corr, do, di, L_tube, k_wall, Rfi, Rfo, ...
                m_cold, rho_cold, mu_cold, k_cold, Pr_cold, ...
                m_hot, rho_hot, mu_hot, k_hot, Pr_hot);
            results(idx).layout = layouts(li);
            results(idx).pitch_ratio = pitch_ratios(pi_);
            results(idx).baffle_ratio = baffle_ratios(bi);
            results(idx).U = d.U;
            results(idx).A_provided = d.A_provided;
            results(idx).dP_shell_kPa = d.dP_shell_Pa/1000;
            results(idx).dP_tube_kPa = d.dP_tube_Pa/1000;
            idx = idx + 1;
        end
    end
end

T = struct2table(results);
writetable(T, 'matlab_optimization_sweep.csv');
fprintf('\nSaved matlab_optimization_sweep.csv (%d configurations)\n', height(T));

%% ---------------------------------------------------------------------
%  5. SELECT OPTIMUM (10-15% U improvement band, dP within limits)
%  ---------------------------------------------------------------------
DP_SHELL_LIMIT = 70; DP_TUBE_LIMIT = 50;   % kPa
feasible = T(T.dP_shell_kPa <= DP_SHELL_LIMIT & T.dP_tube_kPa <= DP_TUBE_LIMIT, :);
improvement = (feasible.U/baseline.U - 1)*100;
band = feasible(improvement >= 10 & improvement <= 15, :);
if height(band) > 0
    [~, i_] = min(band.dP_shell_kPa);
    optimum = band(i_, :);
else
    [~, i_] = max(feasible.U);
    optimum = feasible(i_, :);
end

fprintf('\n--- OPTIMIZED ---\n');
disp(optimum);
fprintf('U improvement: %.1f %%\n', (optimum.U/baseline.U - 1)*100);
fprintf('Area reduction: %.1f %%\n', (1 - optimum.A_provided/baseline.A_provided)*100);

%% ---------------------------------------------------------------------
%  6. PLOTS
%  ---------------------------------------------------------------------
figure('Position',[100 100 800 500]);
tri125 = T(T.layout=="triangular" & T.pitch_ratio==1.25, :);
tri125 = sortrows(tri125, 'baffle_ratio');
yyaxis left; plot(tri125.baffle_ratio, tri125.U, '-o', 'LineWidth', 2);
ylabel('Overall U (W/m^2K)');
yyaxis right; plot(tri125.baffle_ratio, tri125.dP_shell_kPa, '--s', 'LineWidth', 2);
ylabel('Shell-side \Delta P (kPa)');
xlabel('Baffle spacing ratio, B/Ds');
title('Heat-Transfer / Pressure-Drop Trade-off vs Baffle Spacing');
grid on;
saveas(gcf, 'matlab_baffle_tradeoff.png');

fprintf('\nDone.\n');

%% ---------------------------------------------------------------------
%  LOCAL FUNCTION: Kern-method design
%  ---------------------------------------------------------------------
function d = design_hx(U_guess, pt_ratio, layout, passes, baffle_ratio, ...
        Q, LMTD_corr, do, di, L_tube, k_wall, Rfi, Rfo, ...
        m_cold, rho_cold, mu_cold, k_cold, Pr_cold, ...
        m_hot, rho_hot, mu_hot, k_hot, Pr_hot)

    pt = pt_ratio*do;

    K1tab = containers.Map({'triangular_1','triangular_2','triangular_4', ...
                             'square_1','square_2','square_4'}, ...
                            {[0.319,2.142],[0.249,2.207],[0.175,2.285], ...
                             [0.215,2.207],[0.156,2.291],[0.158,2.263]});
    key = sprintf('%s_%d', layout, passes);
    kn = K1tab(key); K1 = kn(1); n1 = kn(2);

    for it = 1:60
        A_req = Q/(U_guess*LMTD_corr);
        Nt = max(4, round(A_req/(pi*do*L_tube)));
        Nt = ceil(Nt/passes)*passes;

        Db = do*(Nt/K1)^(1/n1);
        if Db < 0.6
            clearance = 0.05;
        else
            clearance = 0.07;
        end
        Ds = Db + clearance;

        tubes_per_pass = Nt/passes;
        Ai_flow = tubes_per_pass*(pi/4)*di^2;
        v_tube = m_cold/(rho_cold*Ai_flow);
        Re_tube = rho_cold*v_tube*di/mu_cold;
        Nu_tube = 0.023*Re_tube^0.8*Pr_cold^0.4;
        hi = Nu_tube*k_cold/di;

        C = pt - do;
        B = baffle_ratio*Ds;
        As = (Ds*C*B)/pt;
        Gs = m_hot/As;
        if layout == "triangular"
            de = 1.10/do*(pt^2 - 0.917*do^2);
        else
            de = 1.27/do*(pt^2 - 0.785*do^2);
        end
        Re_shell = Gs*de/mu_hot;
        Nu_shell = 0.36*Re_shell^0.55*Pr_hot^(1/3);
        ho = Nu_shell*k_hot/de;

        U_new = 1/(1/ho + Rfo + do*log(do/di)/(2*k_wall) + Rfi*(do/di) + (do/di)/hi);

        if abs(U_new - U_guess)/U_guess < 1e-4
            U_guess = U_new;
            break
        end
        U_guess = 0.5*U_guess + 0.5*U_new;
    end

    A_provided = Nt*pi*do*L_tube;

    f_tube = (1.82*log10(Re_tube) - 1.64)^-2;
    dP_tube = passes*(f_tube*(L_tube/di))*rho_cold*v_tube^2/2 + passes*4*(rho_cold*v_tube^2/2);

    jf = 0.72*Re_shell^-0.238;
    us = Gs/rho_hot;
    dP_shell = 8*jf*(Ds/de)*(L_tube/B)*(rho_hot*us^2/2);

    d.U = U_guess; d.A_provided = A_provided; d.Nt = Nt; d.Ds = Ds;
    d.hi = hi; d.ho = ho; d.Re_tube = Re_tube; d.Re_shell = Re_shell;
    d.dP_tube_Pa = dP_tube; d.dP_shell_Pa = dP_shell; d.B = B;
end
