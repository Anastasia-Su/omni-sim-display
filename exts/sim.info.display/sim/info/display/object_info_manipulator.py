from omni.ui import scene as sc
import omni.ui as ui
from pxr import UsdGeom


class ObjInfoManipulator(sc.Manipulator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_prims = []

    def on_build(self):

        if not self.model:
            return
        
        if self.model.get_item("name") == "":
            return
        
        stage = self.model.usd_context.get_stage()

        if not stage:
            return
        
        for prim in stage.Traverse():
            prim_path = str(prim.GetPath())


            # if prim.IsA(UsdGeom.Imageable) and not prim.GetPath().pathString in (
            #     '/World', '/Environment/ground', '/Environment'
            # ):
            if prim_path not in self.selected_prims:
                continue
            position = self.model.get_position_for_prim(prim)


            with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
                with sc.Transform(scale_to=sc.Space.SCREEN):
                    sc.Label(f"Path: {prim.GetPath().pathString}")

        # position = self.model.get_as_floats(self.model.get_item("position"))

        # with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
        #     with sc.Transform(scale_to=sc.Space.SCREEN):
        #         sc.Label(f"Path: {self.model.get_item('name')}")

    def add_selected_prim(self, prim_path):
        """Adds a prim path to the list of selected prims."""
        if prim_path not in self.selected_prims:
            self.selected_prims.append(prim_path)
            # self.invalidate()  


    def on_model_updated(self, item):
        self.invalidate()
