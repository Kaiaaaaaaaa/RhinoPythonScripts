# -*- coding: utf-8 -*-

import re
import rhinoscriptsyntax as rs


KEY = "kkOP:NONS_Process|Fase bygget"
PHASE_RE = re.compile(r"-([0-9]+)$")

def layer_short_name(layer_full_path):
    # Rhino layer paths are like "A::B::skråning-030960"
    if not layer_full_path:
        return None
    return layer_full_path.split("::")[-1]

def extract_phase(short_layer_name):
    if not short_layer_name:
        return None
    m = PHASE_RE.search(short_layer_name)
    if not m:
        return None
    return m.group(1)

# --- main ---
ids = rs.SelectedObjects()
if not ids:
    print("No objects selected.")
else:
    updated = 0
    skipped = 0

    for obj_id in ids:
        layer_full = rs.ObjectLayer(obj_id)
        short_name = layer_short_name(layer_full)
        phase = extract_phase(short_name)

        if not phase:
            skipped += 1
            print("Skipped: {} (layer shortname: {})".format(obj_id, short_name))
            continue

        # Write user text to object
        rs.SetUserText(obj_id, KEY, phase)
        updated += 1

    print("Done. Updated: {} | Skipped: {}".format(updated, skipped))
