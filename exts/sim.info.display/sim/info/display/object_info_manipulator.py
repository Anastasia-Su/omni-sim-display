from omni.ui import scene as sc
import omni.ui as ui


class ObjInfoManipulator(sc.Manipulator):

    def on_build(self):

        if not self.model:
            return
        
        if self.model.get_item("name") == "":
            return

        position = self.model.get_as_floats(self.model.get_item("position"))

        with sc.Transform(transform=sc.Matrix44.get_translation_matrix(*position)):
            with sc.Transform(scale_to=sc.Space.SCREEN):
                sc.Label(f"Path: {self.model.get_item('name')}")


    def on_model_updated(self, item):
        self.invalidate()
