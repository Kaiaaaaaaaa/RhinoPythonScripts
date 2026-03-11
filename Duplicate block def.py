import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def _unique_idef_name(base_name):
    name = base_name
    i = 1
    while sc.doc.InstanceDefinitions.Find(name) is not None:
        name = "{}_{}".format(base_name, i)
        i += 1
    return name

def duplicate_block_definition_from_instance():
    obj_id = rs.GetObject(
        "Select a block instance to duplicate",
        rs.filter.instance,
        preselect=True
    )
    if not obj_id:
        return

    guid = rs.coerceguid(obj_id)
    rh_obj = sc.doc.Objects.FindId(guid)
    if rh_obj is None:
        rs.MessageBox("Could not find object in document.")
        return

    # Cast to InstanceObject (Rhino 7)
    inst_obj = rh_obj
    if not isinstance(inst_obj, Rhino.DocObjects.InstanceObject):
        rs.MessageBox("Selected object is not an InstanceObject (block instance).")
        return

    src_idef = inst_obj.InstanceDefinition
    if src_idef is None:
        rs.MessageBox("Selected instance has no instance definition.")
        return

    # Get the objects that belong to this definition (RhinoCommon API)
    def_objs = src_idef.GetObjects()  # returns RhinoObject[]
    if def_objs is None or len(def_objs) == 0:
        rs.MessageBox("Block definition contains no objects (or is not accessible).")
        return

    geoms = []
    attrs = []

    for o in def_objs:
        if o is None:
            continue
        g = o.Geometry
        if g is None:
            continue
        geoms.append(g.Duplicate())
        attrs.append(o.Attributes.Duplicate())

    if len(geoms) == 0:
        rs.MessageBox("No valid geometry found in the source block definition.")
        return

    new_name = _unique_idef_name("{}_copy".format(src_idef.Name))

    # Rhino 7-safe: definitions do not expose a basepoint; definition-space is origin.
    base_point = Rhino.Geometry.Point3d.Origin

    new_index = sc.doc.InstanceDefinitions.Add(
        new_name,
        src_idef.Description,
        base_point,
        geoms,
        attrs
    )

    if new_index < 0:
        rs.MessageBox("Failed to create new block definition.")
        return

    # Optional: replace the selected instance with the new definition at same transform
    replace = rs.GetString(
        "Replace selected instance with the new block? (Yes/No)",
        "Yes",
        ["Yes", "No"]
    )
    if replace == "Yes":
        xform = inst_obj.InstanceXform  # correct Rhino 7 API :contentReference[oaicite:2]{index=2}
        sc.doc.Objects.Delete(inst_obj, True)
        sc.doc.Objects.AddInstanceObject(new_index, xform)  # :contentReference[oaicite:3]{index=3}

    sc.doc.Views.Redraw()
    print("Created new block definition: {}".format(new_name))

if __name__ == "__main__":
    duplicate_block_definition_from_instance()
