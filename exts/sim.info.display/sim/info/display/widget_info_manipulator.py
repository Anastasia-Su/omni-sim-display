from omni.ui import scene as sc
from pxr import UsdGeom
import omni.usd
import omni.ui as ui
from omni.ui import color as cl


class WidgetInfoManipulator(sc.Manipulator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.usd_context = omni.usd.get_context()
        self.widgets = []

    def on_build(self):

        for widget in self.widgets:
            widget.frame.clear()
        self.widgets.clear()

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
                        widget = sc.Widget(550, 150)
                        self.widgets.append(widget)

                        custom_style = {"font_size": 25, "margin": 20}
                        with widget.frame:
                            with ui.ZStack():
                                ui.Rectangle(
                                    style={
                                        "background_color": cl(0.2),
                                        "border_color": cl(0.7),
                                        "border_width": 2,
                                        "border_radius": 4,
                                    }
                                )
                                if prim.IsA(UsdGeom.Imageable):
                                    with ui.VStack():
                                        if prim.GetCustomData():
                                            formatted_data = "\n".join(
                                                f"{key}: {value}"
                                                for key, value in prim.GetCustomData().items()
                                            )
                                            ui.Label(
                                                formatted_data,
                                                height=0,
                                                alignment=ui.Alignment.LEFT,
                                                style=custom_style,
                                            )
                                        else:
                                            ui.Label(
                                                "No meta found for this prim",
                                                style=custom_style,
                                            )

    def on_model_updated(self, item):
        self.invalidate()
