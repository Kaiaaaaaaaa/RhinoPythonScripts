# kk_sum_selected_textdots_to_selected_brep.py
# Uses current selection only:
#   - exactly 1 Brep (surface or polysurface)
#   - 1..n TextDots
# Sums TextDot values and writes them to Brep user text.

import rhinoscriptsyntax as rs

KEY = "kkOP:Gravearbeider_Merknad|Mengde"


def _try_parse_float(text):
    if text is None:
        return None
    t = str(text).strip()
    if not t:
        return None

    # Allow decimal comma
    t = t.replace(",", ".")

    try:
        return float(t)
    except:
        return None


def main():
    sel = rs.SelectedObjects()
    if not sel:
        rs.MessageBox("Nothing selected.\nSelect 1 Brep and 1 or more TextDots, then run the command.", 0)
        return

    breps = []
    dots = []

    for obj_id in sel:
        if rs.IsSurface(obj_id) or rs.IsPolysurface(obj_id):
            breps.append(obj_id)
        elif rs.IsTextDot(obj_id):
            dots.append(obj_id)

    if len(breps) != 1:
        rs.MessageBox(
            "Selection error:\n\n"
            "Expected exactly ONE Brep.\n"
            "Found: {0}".format(len(breps)),
            0
        )
        return

    if len(dots) == 0:
        rs.MessageBox(
            "Selection error:\n\n"
            "Expected at least ONE TextDot.",
            0
        )
        return

    total = 0.0
    invalid = []

    for dot_id in dots:
        txt = rs.TextDotText(dot_id)
        val = _try_parse_float(txt)
        if val is None:
            invalid.append(txt)
            continue
        total += val
        rs.HideObject(dot_id)

    value_str = "{0:.2f}".format(total)

    # Overwrite if it exists
    if not rs.SetUserText(breps[0], KEY, value_str):
        rs.MessageBox("Failed to write user text to Brep.", 0)
        return

    if invalid:
        rs.MessageBox(
            "Sum written: {0}\n\n"
            "Skipped non-numeric TextDots ({1}):\n- {2}".format(
                value_str,
                len(invalid),
                "\n- ".join([str(x) for x in invalid])
            ),
            0
        )


if __name__ == "__main__":
    main()
