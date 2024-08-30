from omni.ui import scene as sc
import omni.ui as ui
from pxr import UsdGeom
from .context_storage import selected_prims


class ObjInfoManipulator(sc.Manipulator):

    def on_build(self):

        if not self.model:
            return
        
        if self.model.get_item("name") == "":
            return
        
        stage = self.model.usd_context.get_stage()

        if not stage:
            return
        
        if len(selected_prims):
            print("selprims", selected_prims)

            for prim_path in selected_prims:
                prim = stage.GetPrimAtPath(prim_path)

                if prim.IsA(UsdGeom.Imageable):
                    # Get the position of the current prim
                    position = self.model.get_position_for_prim(prim)

                    with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
                        with sc.Transform(scale_to=sc.Space.SCREEN):
                            sc.Label(f"Path: {prim.GetPath().pathString}")
        else:
            print("No selected")

    def on_model_updated(self, item):
        self.invalidate()
