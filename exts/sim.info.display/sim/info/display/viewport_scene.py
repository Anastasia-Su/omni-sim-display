from omni.ui import scene as sc
import omni.ui as ui

from .object_info_manipulator import ObjInfoManipulator
from .object_info_model import ObjInfoModel

class ViewportSceneInfo():
    """The Object Info Manipulator, placed into a Viewport"""
    def __init__(self, viewport_window, ext_id) -> None:
        self.scene_view = None
        self.viewport_window = viewport_window


        with self.viewport_window.get_frame(ext_id):
            self.scene_view = sc.SceneView()

            # Add the manipulator into the SceneView's scene
            with self.scene_view.scene:
                obj_manipulator = ObjInfoManipulator()
                # ObjInfoManipulator(model=ObjInfoModel(manipulator=obj_manipulator))
                obj_info_model = ObjInfoModel(manipulator=obj_manipulator) 
                obj_manipulator.model = obj_info_model  
                print(f"Manipulator assigned to model: {obj_info_model.manipulator}") 
           
            self.viewport_window.viewport_api.add_scene_view(self.scene_view)

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self.scene_view:
            self.scene_view.scene.clear()
            if self.viewport_window:
                self.viewport_window.viewport_api.remove_scene_view(self.scene_view)
       
        self.viewport_window = None
        self.scene_view = None