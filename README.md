# Thermal Design and Performance Analysis of a Shell-and-Tube Heat Exchanger

**Self Project | May 2025 – July 2025**

## Overview

This project focused on the **thermal design and performance optimization of a shell-and-tube heat exchanger** for recovering thermal energy from a hot process stream.

The exchanger was designed to maximize heat-transfer performance while maintaining acceptable **pressure drop, equipment size, and thermal-hydraulic performance**.

The design process combined analytical heat-exchanger calculations with computational fluid dynamics (CFD) analysis. Key design parameters including **heat duty, Log Mean Temperature Difference (LMTD), overall heat-transfer coefficient, required heat-transfer area, and pressure drop** were calculated using MATLAB/Excel.

Different tube arrangements and flow configurations were then evaluated using **ANSYS Fluent** to study temperature distribution, fluid flow, heat-transfer behavior, and pressure losses.

The optimized configuration demonstrated approximately **10–15% improvement in heat-transfer performance** while maintaining acceptable pressure drop and compact equipment size.

---

## Objective

The primary objective was to design and optimize a shell-and-tube heat exchanger capable of recovering thermal energy from a hot process stream.

The project aimed to:

1. Determine the required heat-transfer duty.
2. Select suitable shell-and-tube heat-exchanger configuration.
3. Calculate the Log Mean Temperature Difference (LMTD).
4. Estimate the overall heat-transfer coefficient.
5. Determine the required heat-transfer area.
6. Select appropriate tube dimensions and arrangement.
7. Evaluate pressure drop on the shell and tube sides.
8. Compare different flow configurations.
9. Validate thermal performance using CFD simulation.
10. Optimize the exchanger for heat-transfer performance, pressure drop, and compactness.

---

## Problem Statement

Heat exchangers are widely used in industrial processes to transfer thermal energy between fluids without direct mixing.

An inefficient heat exchanger can result in:

* Higher energy consumption
* Increased operating cost
* Excessive equipment size
* Large pressure losses
* Poor thermal recovery

The design therefore requires a balance between heat-transfer performance and hydraulic losses.

The fundamental design objective can be represented as:

```text id="z6k1bc"
Higher Heat Transfer
        ↑
        |
        |      Optimal Design
        |          ●
        |
        |
        └──────────────────→
             Pressure Drop
```

The objective was to maximize useful heat transfer without introducing excessive pressure drop or unnecessary equipment size.

---

## Heat Exchanger Configuration

A shell-and-tube heat exchanger consists primarily of:

* Shell
* Tubes
* Tube sheets
* Baffles
* Inlet and outlet nozzles
* Fluid-side channels

A simplified configuration is:

```text id="5sgyga"
Hot Fluid
   ↓
┌─────────────────────────────────┐
│     Shell                       │
│                                 │
│  ────────────────────────────   │
│  ────────────────────────────   │
│  ────────────────────────────   │
│        Tube Bundle              │
│  ────────────────────────────   │
│  ────────────────────────────   │
│                                 │
└─────────────────────────────────┘
                ↓
             Outlet
```

One fluid flows through the tubes while the other flows through the shell side.

---

## Heat Transfer Principle

The heat exchanger operates by transferring thermal energy from the hot stream to the colder stream.

For a steady-state system:


Q=\dot{m}_h C_{p,h}(T_{h,in}-T_{h,out})


and:


Q=\dot{m}_c C_{p,c}(T_{c,out}-T_{c,in})


where:

* \(Q\) = heat-transfer rate
* \(\dot{m}\) = mass flow rate
* \(C_p\) = specific heat capacity
* \(T\) = temperature
* \(h\) = hot stream
* \(c\) = cold stream

The heat gained by the cold fluid should approximately equal the heat lost by the hot fluid, subject to heat losses and modeling assumptions.

---

## Design Workflow

The overall design methodology followed:

```text id="0v3fuk"
Process Requirements
        ↓
Fluid Property Selection
        ↓
Heat Duty Calculation
        ↓
Temperature Profile
        ↓
LMTD Calculation
        ↓
Heat-Transfer Coefficient
        ↓
Required Heat-Transfer Area
        ↓
Tube / Shell Dimension Selection
        ↓
Pressure-Drop Calculation
        ↓
Initial Design
        ↓
ANSYS Fluent Simulation
        ↓
Performance Evaluation
        ↓
Design Optimization
        ↓
Final Configuration
```

---

## Design Inputs

The design requires process and fluid parameters such as:

| Parameter                      | Description                       |
| ------------------------------ | --------------------------------- |
| Hot-stream inlet temperature   | Temperature entering exchanger    |
| Hot-stream outlet temperature  | Required outlet temperature       |
| Cold-stream inlet temperature  | Temperature entering exchanger    |
| Cold-stream outlet temperature | Target outlet temperature         |
| Hot-stream mass flow rate      | Hot-side flow                     |
| Cold-stream mass flow rate     | Cold-side flow                    |
| Specific heat                  | Fluid thermal property            |
| Density                        | Hydraulic calculation             |
| Viscosity                      | Reynolds number and pressure drop |
| Thermal conductivity           | Heat-transfer calculation         |

The actual project values can be added to the repository as a design-input table.

---

## Heat Duty Calculation

The heat duty was calculated using the energy balance.

For the hot stream:


Q_h=\dot{m}_hC_{p,h}(T_{h,in}-T_{h,out})


For the cold stream:


Q_c=\dot{m}_cC_{p,c}(T_{c,out}-T_{c,in})

The calculated heat duties should satisfy the approximate energy balance:


Q_h \approx Q_c

The required heat duty determines the approximate heat-transfer capacity of the exchanger.

---

## Log Mean Temperature Difference

The **Log Mean Temperature Difference (LMTD)** was used to determine the effective temperature driving force for heat transfer.

For a counter-flow exchanger:

$$
\Delta T_1=T_{h,in}-T_{c,out}
$$

$$
\Delta T_2=T_{h,out}-T_{c,in}
$$

The LMTD is:

$$
LMTD=
\frac{\Delta T_1-\Delta T_2}
{\ln(\Delta T_1/\Delta T_2)}
$$

The heat-transfer equation is:

$$
Q=UA\Delta T_{lm}
$$

where:

* \(U\) = overall heat-transfer coefficient
* \(A\) = heat-transfer area
* \(\Delta T_{lm}\) = LMTD

For multipass or non-ideal arrangements, an appropriate LMTD correction factor can be incorporated:

$$
Q=UA F\Delta T_{lm}
$$

where \(F\) is the LMTD correction factor.

---

## Overall Heat-Transfer Coefficient

The overall heat-transfer coefficient combines the thermal resistances from the hot fluid, tube wall, and cold fluid.

A simplified resistance relation is:


\frac{1}{U}
=
\frac{1}{h_i}
+
R_{wall}
+
\frac{1}{h_o}
+
R_{fouling}
$$

where:

* \(h_i\) = tube-side heat-transfer coefficient
* \(h_o\) = shell-side heat-transfer coefficient
* \(R_{wall}\) = tube-wall thermal resistance
* \(R_{fouling}\) = fouling resistance

The overall heat-transfer coefficient is one of the most important parameters controlling exchanger size.

---

## Heat-Transfer Area

Once the heat duty, overall heat-transfer coefficient, and temperature driving force were determined, the required heat-transfer area was estimated using:

$$
A=
\frac{Q}
{UF\Delta T_{lm}}
$$

The required area influences:

* Number of tubes
* Tube length
* Shell diameter
* Equipment size
* Cost

A larger area generally improves heat-transfer capacity but increases equipment size and potentially pressure drop.

---

## Tube Design

Tube dimensions were selected based on thermal and hydraulic requirements.

Important parameters include:

* Tube outer diameter
* Tube inner diameter
* Tube length
* Number of tubes
* Tube pitch
* Tube arrangement
* Number of tube passes

A simplified relationship for total tube-side heat-transfer area is:

$$
A_t=N\pi D_oL
$$

where:

* \(N\) = number of tubes
* \(D_o\) = tube outer diameter
* \(L\) = tube length

---

## Tube Arrangement

Different tube arrangements were considered to evaluate their impact on:

* Heat-transfer coefficient
* Flow distribution
* Pressure drop
* Compactness
* Manufacturability

Common arrangements include:

```text id="10v3ak"
Triangular Pitch

  ●   ●   ●
    ●   ●
  ●   ●   ●


Square Pitch

  ●   ●   ●
  ●   ●   ●
  ●   ●   ●
```

Triangular arrangements can provide strong heat-transfer performance and compact packing, while square arrangements can offer advantages for cleaning and maintenance.

The final arrangement was selected based on the overall thermal-hydraulic trade-off.

---

## Flow Configuration

The relative direction of hot and cold fluid flow significantly affects heat-transfer performance.

Two common configurations are:

### Parallel Flow

```text id="87bjtw"
Hot Fluid    →
             →
Cold Fluid   →
```

Both fluids flow in the same direction.

### Counter Flow

```text id="f4cc4h"
Hot Fluid    →
             →
Cold Fluid   ←
```

The fluids flow in opposite directions.

Counter-flow operation generally provides a higher effective temperature driving force for many heat-exchanger applications.

The project evaluated flow configurations to identify a suitable thermal-hydraulic design.

---

## Reynolds Number

The Reynolds number was used to characterize the flow regime.

$$
Re=\frac{\rho VD}{\mu}
$$

where:

* \(\rho\) = fluid density
* \(V\) = average velocity
* \(D\) = characteristic diameter
* \(\mu\) = dynamic viscosity

The Reynolds number helps determine whether the flow is predominantly:

```text id="5c8z5c"
Laminar
   ↓
Transition
   ↓
Turbulent
```

Flow regime strongly influences convective heat transfer.

---

## Nusselt Number

The Nusselt number represents the relative importance of convective heat transfer compared with conductive heat transfer.

$$
Nu=\frac{hD}{k}
$$

where:

* \(h\) = convective heat-transfer coefficient
* \(D\) = characteristic diameter
* \(k\) = thermal conductivity

Appropriate correlations can be used to estimate \(Nu\), from which the convective heat-transfer coefficient can be obtained.

---

## Pressure-Drop Analysis

Pressure drop was evaluated on both the tube and shell sides.

The total pressure drop can be conceptually represented as:


\Delta P_{total}
=
\Delta P_{friction}
+
\Delta P_{fittings}
+
\Delta P_{other}
$$

Pressure drop is an important design constraint because excessive hydraulic losses increase pumping requirements and operating costs.

The design therefore seeks:

```text
High Heat Transfer
       +
Acceptable Pressure Drop
```

rather than maximizing heat transfer alone.

---

## Shell-Side Analysis

Shell-side flow behavior depends on:

* Shell diameter
* Baffle spacing
* Baffle cut
* Tube arrangement
* Tube pitch
* Flow rate
* Fluid properties

Baffles are used to direct shell-side fluid across the tube bundle.

A simplified flow path is:

```text id="2x0j67"
Shell Inlet
     ↓
 ───────── Baffle
       ↓
 ───────── Baffle
       ↑
 ───────── Baffle
       ↓
Shell Outlet
```

This increases flow interaction with the tube bundle and can improve heat transfer.

However, excessive flow resistance can increase pressure drop.

---

## Baffle Design

Baffle parameters were considered as part of the thermal-hydraulic design.

Important parameters include:

* Baffle spacing
* Baffle cut
* Number of baffles
* Flow path

The design balances:

```text
Baffle Interaction
       ↓
Heat Transfer ↑
       +
Pressure Drop ↑
```

Therefore, excessive baffling is not necessarily optimal.

---

## MATLAB / Excel Calculations

MATLAB and Excel were used to perform the analytical thermal design calculations.

The calculation workflow included:

```text
Input Process Data
       ↓
Calculate Heat Duty
       ↓
Calculate Temperature Differences
       ↓
Calculate LMTD
       ↓
Estimate U
       ↓
Calculate Heat-Transfer Area
       ↓
Determine Tube Count
       ↓
Estimate Flow Velocity
       ↓
Calculate Reynolds Number
       ↓
Estimate Pressure Drop
```

Using a spreadsheet or MATLAB script allows rapid evaluation of different design configurations.

---

## CFD Analysis Using ANSYS Fluent

ANSYS Fluent was used to evaluate the detailed thermal and fluid-flow behavior of the exchanger.

The CFD model provided information regarding:

* Temperature distribution
* Velocity distribution
* Pressure distribution
* Heat-transfer behavior
* Flow separation
* Pressure drop
* Thermal uniformity

A simplified CFD workflow is:

```text
CAD Geometry
     ↓
Geometry Cleanup
     ↓
Meshing
     ↓
Material Properties
     ↓
Boundary Conditions
     ↓
Solver Setup
     ↓
Convergence
     ↓
Temperature / Velocity / Pressure Results
     ↓
Performance Comparison
```

---

## CFD Boundary Conditions

Representative boundary conditions were applied to the model.

Typical inputs include:

### Hot-Side Inlet

* Mass flow rate or velocity
* Inlet temperature

### Cold-Side Inlet

* Mass flow rate or velocity
* Inlet temperature

### Outlet

* Pressure outlet or equivalent flow condition

### Solid Walls

* No-slip condition
* Thermal conduction through tube walls

The exact boundary conditions depend on the selected exchanger configuration and simulation assumptions.

---

## Meshing

The exchanger geometry was discretized into finite computational elements.

Mesh quality affects the accuracy and stability of CFD results.

Important mesh considerations include:

* Element size
* Inflation layers
* Boundary-layer resolution
* Skewness
* Orthogonality
* Mesh independence

A typical process is:

```text
Coarse Mesh
     ↓
Medium Mesh
     ↓
Fine Mesh
     ↓
Compare Results
     ↓
Mesh Independence
```

A mesh-independent solution provides greater confidence that the predicted performance is not strongly dependent on mesh resolution.

---

## Temperature Distribution

The CFD simulation was used to visualize the temperature field inside the heat exchanger.

A conceptual temperature profile is:

```text
Hot Fluid
High Temperature
      ↓
████████████████
██████████████
████████████
████████
      ↓
Lower Temperature

Cold Fluid
Low Temperature
      ↑
████████
████████████
██████████████
████████████████
      ↑
Higher Temperature
```

The temperature contours help identify regions of effective and ineffective heat transfer.

---

## Velocity Distribution

Velocity contours were analyzed to understand the flow distribution through the shell and tube sides.

Important observations include:

* High-velocity regions
* Low-velocity zones
* Flow maldistribution
* Recirculation
* Flow separation

Poor flow distribution can reduce the effective heat-transfer area and create localized pressure losses.

---

## Pressure Distribution

Pressure contours were used to evaluate hydraulic losses throughout the exchanger.

The pressure generally decreases along the flow direction:

$$
P_{in}>P_{out}
$$

The difference:

$$
\Delta P=P_{in}-P_{out}
$$

was used to evaluate the hydraulic performance of the design.

---

## Design Optimization

The exchanger configuration was optimized by evaluating the trade-off between:

* Heat-transfer rate
* Overall heat-transfer coefficient
* Heat-transfer area
* Pressure drop
* Equipment size
* Flow configuration
* Tube arrangement

The optimization process can be represented as:

```text
Initial Design
      ↓
CFD Analysis
      ↓
Performance Evaluation
      ↓
Modify Geometry
      ↓
Re-run Simulation
      ↓
Compare Results
      ↓
Select Improved Configuration
```

---

## Performance Comparison

Different design configurations can be compared using normalized performance metrics.

Example:

| Parameter                 | Baseline |    Optimized |
| ------------------------- | -------: | -----------: |
| Heat-transfer performance |     100% | **110–115%** |
| Pressure Drop             | Baseline |   Acceptable |
| Equipment Size            | Baseline |      Compact |
| Thermal Performance       | Baseline |     Improved |

The optimized design demonstrated approximately:

### **10–15% improvement in heat-transfer performance**

while maintaining acceptable hydraulic performance and equipment size.

---

## Thermal-Hydraulic Trade-Off

A central finding of the project was that increasing heat transfer often comes with increased pressure drop.

Conceptually:

```text
Heat Transfer
     ↑
     |
     |              *
     |           *
     |        *
     |     *
     |  *
     └────────────────────→
          Pressure Drop
```

The best configuration is therefore not necessarily the one with the maximum heat-transfer coefficient.

Instead, the design must provide a suitable compromise between:

$$
Thermal\ Performance
\quad \text{and} \quad
Hydraulic\ Performance
$$

---

## Results

The optimized shell-and-tube heat exchanger achieved:

* Approximately **10–15% improvement in heat-transfer performance**
* Acceptable pressure drop
* Compact equipment configuration
* Improved thermal utilization of the exchanger
* Evaluated tube arrangements and flow configurations
* Analytical design using MATLAB/Excel
* CFD-based performance evaluation using ANSYS Fluent

The combined analytical and CFD approach provided a systematic method for improving the exchanger design.

---

## Key Findings

### 1. Heat-transfer area is a major design parameter

Increasing the available heat-transfer area generally increases the exchanger's thermal capacity, but also affects size and cost.

### 2. Flow arrangement strongly affects thermal performance

Counter-flow configurations can provide a favorable temperature driving force compared with parallel flow.

### 3. Tube arrangement influences both heat transfer and pressure drop

Changing tube pitch and arrangement modifies shell-side flow characteristics and therefore affects thermal-hydraulic performance.

### 4. Baffle configuration affects the overall design

Baffles can improve shell-side heat transfer by increasing cross-flow interaction but can simultaneously increase pressure losses.

### 5. CFD provides detailed flow insight

Analytical calculations provide fast design estimates, while CFD helps visualize detailed temperature, velocity, and pressure fields.

### 6. Optimization requires a thermal-hydraulic balance

Maximizing heat transfer alone can result in excessive pressure drop. The final design must satisfy both thermal and hydraulic requirements.

---

## Validation Approach

The analytical and CFD results can be compared using:

### Heat Duty

$$
Q_{CFD}
\approx
Q_{analytical}
$$

### Pressure Drop

$$
\Delta P_{CFD}
\approx
\Delta P_{analytical}
$$

### Outlet Temperature

Compare predicted outlet temperatures from the analytical model and CFD simulation.

This provides a consistency check between the theoretical calculations and numerical simulation.

---

## Recommended Visualizations

The GitHub repository can include the following figures.

### 1. Heat Exchanger CAD Model

Show the complete shell-and-tube geometry.

### 2. Tube Arrangement

Show the selected tube pitch and arrangement.

### 3. CFD Mesh

Show the computational mesh used in ANSYS Fluent.

### 4. Temperature Contour

Show the hot and cold fluid temperature distribution.

### 5. Velocity Contour

Show shell-side and tube-side flow distribution.

### 6. Pressure Contour

Show the pressure drop through the exchanger.

### 7. Heat-Transfer Comparison

Compare baseline and optimized heat-transfer performance.

### 8. Pressure-Drop Comparison

Show the effect of different configurations on hydraulic losses.

### 9. Design Comparison

A final figure can compare:

```text
Baseline Design
       ↓
Heat Transfer = 100%
       ↓
Optimization
       ↓
Optimized Design
       ↓
Heat Transfer = 110–115%
```

---

## Project Structure

A recommended GitHub repository structure is:

```text id="6q5j7h"
Shell-and-Tube-Heat-Exchanger/
│
├── CAD/
│   ├── baseline/
│   └── optimized/
│
├── calculations/
│   ├── MATLAB/
│   └── Excel/
│
├── CFD/
│   ├── geometry/
│   ├── mesh/
│   ├── setup/
│   └── results/
│
├── results/
│   ├── thermal_performance/
│   ├── pressure_drop/
│   └── comparison/
│
├── images/
│   ├── cad_model.png
│   ├── mesh.png
│   ├── temperature_contour.png
│   ├── velocity_contour.png
│   └── pressure_contour.png
│
├── documentation/
│   └── project_report.pdf
│
└── README.md
```

---

## Technologies and Tools

| Tool            | Purpose                                   |
| --------------- | ----------------------------------------- |
| MATLAB          | Thermal and hydraulic calculations        |
| Microsoft Excel | Design calculations and parameter studies |
| ANSYS Fluent    | CFD simulation                            |
| CAD Software    | Heat-exchanger geometry                   |
| Git/GitHub      | Version control and documentation         |

---

## Example Calculation Workflow

A simplified MATLAB-style calculation structure is:

```matlab
% Heat duty
Q = m_hot * Cp_hot * (T_hot_in - T_hot_out);

% Temperature differences
DT1 = T_hot_in - T_cold_out;
DT2 = T_hot_out - T_cold_in;

% LMTD
LMTD = (DT1 - DT2) / log(DT1 / DT2);

% Required heat transfer area
A = Q / (U * F * LMTD);

% Tube-side velocity
V = m_hot / (rho_hot * flow_area);

% Reynolds number
Re = rho_hot * V * D / mu_hot;

fprintf('Heat Duty = %.2f W\n', Q);
fprintf('LMTD = %.2f K\n', LMTD);
fprintf('Required Area = %.2f m^2\n', A);
fprintf('Reynolds Number = %.0f\n', Re);
```

The actual project calculations can be added to the repository as MATLAB scripts or Excel worksheets.

---

## Reproducibility

The project can be reproduced through the following workflow:

1. Define hot- and cold-stream operating conditions.
2. Define fluid thermophysical properties.
3. Calculate the required heat duty.
4. Determine inlet and outlet temperature requirements.
5. Calculate the LMTD.
6. Estimate the overall heat-transfer coefficient.
7. Calculate the required heat-transfer area.
8. Select tube dimensions and tube count.
9. Select tube arrangement and flow configuration.
10. Estimate tube-side and shell-side velocities.
11. Calculate Reynolds numbers.
12. Estimate heat-transfer coefficients.
13. Calculate pressure drops.
14. Develop the exchanger CAD geometry.
15. Generate the CFD mesh.
16. Define ANSYS Fluent boundary conditions.
17. Perform the CFD simulation.
18. Evaluate temperature, velocity, and pressure fields.
19. Compare alternative configurations.
20. Select the optimized design.
21. Validate thermal and hydraulic performance.

---

## Testing and Validation

The design can be evaluated using multiple operating conditions.

### Thermal Performance

Verify:

$$
Q_{hot}\approx Q_{cold}
$$

### Pressure Drop

Verify that:

$$
\Delta P_{actual}\leq\Delta P_{allowable}
$$

### Temperature Requirement

Verify that the required outlet temperatures are achieved.

### CFD Convergence

Monitor:

* Residuals
* Heat balance
* Outlet temperatures
* Pressure drop

until the solution reaches an acceptable convergence level.

---

## Limitations

The results depend on assumptions related to:

* Fluid properties
* Steady-state operation
* Boundary conditions
* Heat losses
* Fouling resistance
* Turbulence model
* Mesh resolution
* Material properties
* Flow distribution

Real industrial heat exchangers may experience additional effects such as:

* Fouling
* Corrosion
* Vibration
* Tube-side deposits
* Manufacturing tolerances
* Thermal expansion
* Flow maldistribution

These effects can be incorporated into a more detailed design study.

---

## Future Improvements

### 1. Fouling Analysis

Investigate the effect of fouling on the overall heat-transfer coefficient and exchanger performance.

### 2. Transient Thermal Analysis

Study exchanger performance under changing inlet temperatures and flow rates.

### 3. Multi-Objective Optimization

Optimize simultaneously for:

* Heat-transfer rate
* Pressure drop
* Equipment volume
* Material usage
* Cost

### 4. Advanced CFD Models

Compare different turbulence models and investigate their influence on predicted heat transfer and pressure drop.

### 5. Thermal Stress Analysis

Couple the CFD temperature field with structural FEA to evaluate thermal stresses and deformation.

### 6. Economic Optimization

Include:

* Capital cost
* Pumping cost
* Energy recovery
* Maintenance cost
* Lifecycle cost

in the optimization framework.

### 7. Experimental Validation

Build or test a scaled heat-exchanger prototype and compare experimental results with MATLAB/Excel and CFD predictions.

---

## Key Concepts Demonstrated

This project demonstrates practical knowledge of:

* Heat Exchanger Design
* Shell-and-Tube Heat Exchangers
* Heat Transfer
* Thermal Engineering
* Energy Balance
* LMTD Method
* Overall Heat-Transfer Coefficient
* Heat-Transfer Area Calculation
* Convective Heat Transfer
* Reynolds Number
* Nusselt Number
* Pressure-Drop Analysis
* Tube Arrangement
* Flow Configuration
* Baffle Design
* Computational Fluid Dynamics
* ANSYS Fluent
* MATLAB
* Excel-Based Engineering Calculations
* Thermal-Hydraulic Optimization
* CFD Post-Processing
* Engineering Design Validation

---

## Conclusion

The **Thermal Design and Performance Analysis of a Shell-and-Tube Heat Exchanger** project demonstrates a systematic approach to thermal system design by combining **analytical heat-transfer calculations with CFD-based performance evaluation**.

The exchanger was designed by calculating the required **heat duty, LMTD, overall heat-transfer coefficient, heat-transfer area, flow parameters, and pressure drop**. Different tube arrangements and flow configurations were evaluated to identify a configuration offering improved thermal performance without excessive hydraulic losses.

ANSYS Fluent was used to investigate detailed **temperature, velocity, and pressure distributions**, providing additional insight into the thermal-hydraulic behavior of the exchanger.

The optimized configuration achieved approximately **10–15% improvement in heat-transfer performance** while maintaining acceptable pressure drop and compact equipment size.

The project demonstrates how analytical modeling, computational simulation, and design optimization can be combined to develop **efficient and practically viable thermal systems**.
