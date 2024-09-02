from omni.ui import scene as sc
from pxr import UsdGeom
import omni.usd


class ObjInfoManipulator(sc.Manipulator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.usd_context = omni.usd.get_context()

    def on_build(self):
        if not self.model:
            return

        if self.model.get_item("name") == "":
            return

        stage = self.model.usd_context.get_stage()

        if not stage:
            return

        all_prims = self.model.get_item("all_prims")

        for prim_path in all_prims:
            prim = stage.GetPrimAtPath(prim_path)

            if prim.IsA(UsdGeom.Imageable):
                position = self.model.get_position_for_prim(prim)

                with sc.Transform(
                    transform=sc.Matrix44.get_translation_matrix(*position)
                ):
                    with sc.Transform(scale_to=sc.Space.SCREEN):
                        if prim.GetCustomData():
                            formatted_data = "\n".join(
                                f"{key}: {value}"
                                for key, value in prim.GetCustomData().items()
                            )
                            sc.Label(f"{formatted_data}")
                        else:
                            sc.Label(f"No meta found for this prim")

    def on_model_updated(self, item):
        self.invalidate()
