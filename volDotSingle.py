import rhinoscriptsyntax as rs

objs = rs.SelectedObjects()

for obj in objs:
    vol = rs.SurfaceVolume(obj)[0]
    text = "{:.3f}".format(vol)

    bbox = rs.BoundingBox(obj)
    center = (bbox[0] + bbox[6]) / 2

    rs.AddTextDot(text, center)
    rs.DeleteObject(obj)