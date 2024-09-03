from omni.ui import scene as sc
import omni.usd
import omni.ui as ui
from omni.ui import color as cl


class WidgetInfoManipulator(sc.Manipulator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.usd_context = omni.usd.get_context()
        self.widgets = []
        self._root = None
        self.destroy()

    def destroy(self):
        self._root = None

    @staticmethod
    def on_build_widgets(prim):
        custom_style = {"font_size": 25, "margin": 20}

        with ui.ZStack():
            ui.Rectangle(
                style={
                    "background_color": cl(0.2),
                    "border_color": cl(0.7),
                    "border_width": 2,
                    "border_radius": 4,
                }
            )

            with ui.VStack():
                if prim.GetCustomData():
                    formatted_data = "\n".join(
                        f"{key}: {value}" for key, value in prim.GetCustomData().items()
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

    def on_build(self):
        self.widgets.clear()

        if not self.model:
            return

        if self.model.get_item("name") == "":
            return

        stage = self.model.usd_context.get_stage()

        if not stage:
            return

        all_prims = self.model.get_item("all_prims")

        self._root = sc.Transform()

        with self._root:
            for prim_path in all_prims:
                prim = stage.GetPrimAtPath(prim_path)

                position = self.model.get_position_for_prim(prim)

                with sc.Transform(
                    transform=sc.Matrix44.get_translation_matrix(*position)
                ):
                    with sc.Transform(scale_to=sc.Space.SCREEN):
                        widget = sc.Widget(
                            500,
                            150,
                            update_policy=sc.Widget.UpdatePolicy.ON_MOUSE_HOVERED,
                        )
                        widget.frame.set_build_fn(
                            lambda prim=prim: WidgetInfoManipulator.on_build_widgets(
                                prim
                            )
                        )
                        self.widgets.append(widget)

    def on_model_updated(self, item):
        self.invalidate()
        self.destroy()
