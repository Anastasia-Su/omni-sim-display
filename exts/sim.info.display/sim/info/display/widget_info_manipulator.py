from omni.ui import scene as sc
from omni.ui import color as cl
import omni.ui as ui
from pxr import Gf


class WidgetInfoManipulator(sc.Manipulator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._widget = None
        self._root = None
        self._name_label = None
        self.destroy()

    def destroy(self):
        self._widget = None
        self._root = None
        self._name_label = None
        
        # self._slider_model = None

    def on_build_widgets(self):
        custom_style = {
            "font_size": 25,
            "margin": 20
        }
        with ui.ZStack():
            ui.Rectangle(style={
                "background_color": cl(0.2),
                "border_color": cl(0.7),
                "border_width": 2,
                "border_radius": 4,
            })

            with ui.VStack():
                self._name_label = ui.Label("", height=0, alignment=ui.Alignment.LEFT, style=custom_style)

          
        self.on_model_updated(None)

    def on_build(self):
        self._root = sc.Transform(visible=False)
        with self._root:
            with sc.Transform(scale_to=sc.Space.SCREEN):
                with sc.Transform(transform=sc.Matrix44.get_translation_matrix(0, 100, 0)):
                    self._widget = sc.Widget(500, 150, update_policy=sc.Widget.UpdatePolicy.ON_MOUSE_HOVERED)
                    self._widget.frame.set_build_fn(self.on_build_widgets)

    def on_model_updated(self, _):
        # if you don't have selection then show nothing
        if not self.model or not self.model.get_item("name"):
            if self._root:
                self._root.visible = False
            return
        
        if self._root:
            self._root.visible = True
        

        all_prims = self.model.get_item("all_prims")
        stage = self.model.usd_context.get_stage()

        for prim_path in all_prims:
            prim = stage.GetPrimAtPath(prim_path)

            position = self.model.get_position_for_prim(prim)

            if self._root:
                self._root.transform = sc.Matrix44.get_translation_matrix(*position)
                self._root.visible = True

            if self._name_label:
                if prim.GetCustomData():
                    formatted_data = "\n".join(
                        f"{key}: {value}"
                        for key, value in prim.GetCustomData().items()
                    )
                    self._name_label.text = f"{formatted_data}"
                else:
                    self._name_label.text = "No meta found for this prim"

            # self._name_label.text = f"Prim:{self.model.get_item('name')}"