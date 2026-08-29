# -*- coding: utf-8 -*-
"""
FreeCAD macro: Parametric Shell-and-Tube Heat Exchanger
==========================================================
Run inside FreeCAD (Macro -> Macros... -> Execute), or headless:
    freecadcmd freecad_hx_macro.py

Builds, in the active document:
  1. "HX_Shell"          - hollow cylindrical shell with 4 nozzles
  2. "HX_TubeBundle"      - full tube bundle (triangular pitch) as a
                            single compound of tube solids
  3. "HX_Baffles"         - segmental baffles (25% cut, alternating)
                            with drilled tube holes
  4. "HX_TubeSheet_Front/Back" - tubesheets with drilled tube holes

Parameters below match the optimized Kern-method design from
optimization_study.py -- edit PARAMETERS to match a different run
(read directly from design_comparison.json if you want to stay in sync).
"""
import FreeCAD as App
import Part
import math
import json

# ----------------------------------------------------------------------
# PARAMETERS (mm) -- optimized design from design_comparison.json
# ----------------------------------------------------------------------
try:
    with open("/home/claude/hx_project/data/design_comparison.json") as f:
        _C = json.load(f)
    with open("/home/claude/hx_project/data/process_spec.json") as f:
        _P = json.load(f)
    OPT = _C["optimized"]
    DO = _P["do_m"]*1000
    DI = _P["di_m"]*1000
    L = _P["L_tube_m"]*1000
    PT = OPT["pt"]*1000
    NT = OPT["Nt"]
    DS = OPT["Ds"]*1000
    DB = OPT["Db"]*1000
    NB = int(round(OPT["Nb"]))
    B = OPT["B"]*1000
except Exception:
    # Fallback defaults if JSON not available (matches the documented design)
    DO, DI, L = 19.05, 15.75, 4880.0
    PT, NT, DS, DB = 23.8125, 60, 278.6, 228.6
    NB, B = 21, 222.9

SHELL_THK = 6.0
BAFFLE_THK = 4.0
TUBESHEET_THK = 25.0
NOZZLE_OD = 100.0
NOZZLE_LEN = 80.0
BAFFLE_CUT = 0.25   # 25% segmental cut

DOC_NAME = "ShellTubeHX"
doc = App.newDocument(DOC_NAME) if DOC_NAME not in [d.Name for d in App.listDocuments().values()] \
      else App.getDocument(DOC_NAME)

# ----------------------------------------------------------------------
# 1. Tube bundle centers (triangular pitch, packed to bundle diameter)
# ----------------------------------------------------------------------
def tube_centers(pt, db, nt):
    row_spacing = pt*math.sqrt(3)/2
    n_rows = int(math.ceil(db/row_spacing)) + 2
    pts = []
    for r in range(-n_rows, n_rows+1):
        y = r*row_spacing
        x_off = (pt/2) if (r % 2 != 0) else 0.0
        n_cols = int(math.ceil(db/pt)) + 2
        for c in range(-n_cols, n_cols+1):
            x = c*pt + x_off
            if x*x + y*y <= (db/2)**2:
                pts.append((x, y))
    pts.sort(key=lambda p: p[0]**2 + p[1]**2)
    return pts[:nt]

centers = tube_centers(PT, DB, NT)
App.Console.PrintMessage(f"Placed {len(centers)} tubes (target {NT}).\n")

# ----------------------------------------------------------------------
# 2. Shell (hollow cylinder) + 4 nozzles
# ----------------------------------------------------------------------
shell_outer = Part.makeCylinder(DS/2 + SHELL_THK, L, App.Vector(0,0,0), App.Vector(1,0,0))
shell_inner = Part.makeCylinder(DS/2, L, App.Vector(0,0,0), App.Vector(1,0,0))
shell_solid = shell_outer.cut(shell_inner)

# nozzles: hot-in (top, near x=L end), hot-out (top, near x=0 end)
def make_nozzle(x_pos, angle_deg, r_shell):
    ang = math.radians(angle_deg)
    dirv = App.Vector(0, math.cos(ang), math.sin(ang))
    base = App.Vector(x_pos, r_shell*math.cos(ang), r_shell*math.sin(ang))
    return Part.makeCylinder(NOZZLE_OD/2, NOZZLE_LEN, base, dirv)

nozzle_hot_in = make_nozzle(L - 200, 90, DS/2)
nozzle_hot_out = make_nozzle(200, 90, DS/2)
nozzle_cold_in = make_nozzle(150, -90, DS/2)
nozzle_cold_out = make_nozzle(L - 150, -90, DS/2)

shell_with_nozzles = shell_solid.fuse([nozzle_hot_in, nozzle_hot_out, nozzle_cold_in, nozzle_cold_out])
obj_shell = doc.addObject("Part::Feature", "HX_Shell")
obj_shell.Shape = shell_with_nozzles

# ----------------------------------------------------------------------
# 3. Tube bundle (compound of tube solids), drilled through tubesheets
# ----------------------------------------------------------------------
tube_solids = []
for (y, z) in centers:
    outer = Part.makeCylinder(DO/2, L, App.Vector(0, y, z), App.Vector(1,0,0))
    inner = Part.makeCylinder(DI/2, L + 2, App.Vector(-1, y, z), App.Vector(1,0,0))
    tube_solids.append(outer.cut(inner))
tube_bundle = tube_solids[0]
for t in tube_solids[1:]:
    tube_bundle = tube_bundle.fuse(t)
obj_tubes = doc.addObject("Part::Feature", "HX_TubeBundle")
obj_tubes.Shape = tube_bundle

# ----------------------------------------------------------------------
# 4. Tubesheets (drilled disks at each end)
# ----------------------------------------------------------------------
def make_tubesheet(x_pos):
    disk = Part.makeCylinder(DS/2, TUBESHEET_THK, App.Vector(x_pos, 0, 0), App.Vector(1,0,0))
    for (y, z) in centers:
        hole = Part.makeCylinder(DO/2 + 0.2, TUBESHEET_THK + 2,
                                  App.Vector(x_pos - 1, y, z), App.Vector(1,0,0))
        disk = disk.cut(hole)
    return disk

sheet_front = make_tubesheet(0.0)
sheet_back = make_tubesheet(L - TUBESHEET_THK)
obj_sheet_f = doc.addObject("Part::Feature", "HX_TubeSheet_Front")
obj_sheet_f.Shape = sheet_front
obj_sheet_b = doc.addObject("Part::Feature", "HX_TubeSheet_Back")
obj_sheet_b.Shape = sheet_back

# ----------------------------------------------------------------------
# 5. Segmental baffles (25% cut, alternating top/bottom), drilled for tubes
# ----------------------------------------------------------------------
baffle_positions = [ (i+1)*L/(NB+1) for i in range(NB) ]
baffle_solids = []
for i, bx in enumerate(baffle_positions):
    disk = Part.makeCylinder(DS/2, BAFFLE_THK, App.Vector(bx - BAFFLE_THK/2, 0, 0), App.Vector(1,0,0))
    # cut segment: remove a chord on alternating sides
    cut_box_h = DS*BAFFLE_CUT
    z_lo = -DS if (i % 2 == 0) else (DS/2 - cut_box_h)
    z_hi = (-DS/2 + cut_box_h) if (i % 2 == 0) else DS
    cutter = Part.makeBox(BAFFLE_THK + 2, DS*2, z_hi - z_lo,
                           App.Vector(bx - BAFFLE_THK/2 - 1, -DS, z_lo))
    disk = disk.cut(cutter)
    for (y, z) in centers:
        hole = Part.makeCylinder(DO/2 + 0.3, BAFFLE_THK + 2,
                                  App.Vector(bx - BAFFLE_THK/2 - 1, y, z), App.Vector(1,0,0))
        disk = disk.cut(hole)
    baffle_solids.append(disk)

baffles = baffle_solids[0]
for b in baffle_solids[1:]:
    baffles = baffles.fuse(b)
obj_baffles = doc.addObject("Part::Feature", "HX_Baffles")
obj_baffles.Shape = baffles

doc.recompute()

# ----------------------------------------------------------------------
# 6. Export
# ----------------------------------------------------------------------
import Import
try:
    Import.export([obj_shell, obj_tubes, obj_baffles, obj_sheet_f, obj_sheet_b],
                   "/tmp/shell_tube_hx_freecad.step")
    App.Console.PrintMessage("Exported STEP to /tmp/shell_tube_hx_freecad.step\n")
except Exception as e:
    App.Console.PrintWarning(f"STEP export skipped: {e}\n")

doc.saveAs("/tmp/shell_tube_hx_freecad.FCStd")
App.Console.PrintMessage("Saved FreeCAD document to /tmp/shell_tube_hx_freecad.FCStd\n")
