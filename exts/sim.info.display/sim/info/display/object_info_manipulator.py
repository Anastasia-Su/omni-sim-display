from omni.ui import scene as sc
import omni.ui as ui
from pxr import UsdGeom


class ObjInfoManipulator(sc.Manipulator):

    def on_build(self):

        if not self.model:
            return
        
        if self.model.get_item("name") == "":
            return
        
        stage = self.model.usd_context.get_stage()

        if not stage:
            return
        
        for prim in stage.Traverse():
            if prim.IsA(UsdGeom.Imageable) and not prim.GetPath().pathString in (
                '/World', '/Environment/ground', '/Environment'
            ):
                # Get the position of the current prim
                position = self.model.get_position_for_prim(prim)


                with ui.Style(
            {
                "Label": {"font_size": 20}  # Set font size for Label
            }
        ):
                # Create a label for each prim
                    with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
                        with sc.Transform(scale_to=sc.Space.SCREEN):
                            sc.Label(f"Path: {prim.GetPath().pathString}")

        # position = self.model.get_as_floats(self.model.get_item("position"))

        # with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
        #     with sc.Transform(scale_to=sc.Space.SCREEN):
        #         sc.Label(f"Path: {self.model.get_item('name')}")


    def on_model_updated(self, item):
        self.invalidate()
