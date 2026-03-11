import rhinoscriptsyntax as rs

objs = rs.SelectedObjects()

u = rs.BooleanUnion(objs)[0] if len(objs) > 1 else objs[0]

vol = rs.SurfaceVolume(u)[0]
text = "{:.3f}".format(vol)

bbox = rs.BoundingBox(u)
center = (bbox[0] + bbox[6]) / 2

rs.AddTextDot(text, center)

rs.DeleteObject(u)
