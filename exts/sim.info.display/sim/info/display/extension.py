import omni.ext
import omni.ui as ui
from omni.kit.viewport.utility import get_active_viewport_window
from .viewport_scene import ViewportSceneInfo


class SimInfoDisplayExtension(omni.ext.IExt):
    def __init__(self) -> None:
        super().__init__()
        self.obj_model = None
        self.viewport_scene = None

    def on_startup(self, ext_id):
        viewport_window = get_active_viewport_window()
        self.viewport_scene = ViewportSceneInfo(viewport_window, ext_id)

    def on_shutdown(self):
        if self.viewport_scene:
            self.viewport_scene.destroy()
            self.viewport_scene = None
