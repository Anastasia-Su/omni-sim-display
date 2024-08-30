import omni.ext
import omni.ui as ui
from omni.kit.viewport.utility import get_active_viewport_window
from .viewport_scene import ViewportSceneInfo
from .context_storage import selected_prims


class SimInfoDisplayExtension(omni.ext.IExt):
    def __init__(self) -> None:
        super().__init__()
        self.obj_model = None
        self.viewport_scene = None

    def on_startup(self, ext_id):
        viewport_window = get_active_viewport_window()
        self.viewport_scene = ViewportSceneInfo(viewport_window, ext_id)
        self.create_window()

    def on_shutdown(self):
        if self.viewport_scene:
            self.viewport_scene.destroy()
            self.viewport_scene = None

    def create_window(self):
        self._window = ui.Window("Manage Selections", width=200, height=200)
        with self._window.frame:
            with ui.VStack():
                ui.Button("Turn info off", clicked_fn=self.on_click)
                self.info_label = ui.Label(
                    "Click the button to remove info display for the selected prim."
                )

    def on_click(self):
        print("Clicked")
        # usd_context = omni.usd.get_context()

        # # Get the current selection
        # selection = usd_context.get_selection()

        # # Get the selected prim paths
        # sel_prims = selection.get_selected_prim_paths()

        # # Print the paths of selected prims
        # for prim_path in sel_prims:
        #     print("selpr_ext",sel_prims)
        #     # print("Selected Prim Path:", prim_path)
        #     if prim_path in selected_prims:
        #         selected_prims.remove(prim_path)
        #         print("final_sel_pr", selected_prims)
