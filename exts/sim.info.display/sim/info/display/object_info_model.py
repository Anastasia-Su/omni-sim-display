# from pxr import Tf
# from pxr import Usd
# from pxr import UsdGeom

# from omni.ui import scene as sc
# from .object_info_manipulator import ObjInfoManipulator
# import omni.usd


# class ObjInfoModel(sc.AbstractManipulatorModel):
#     """
#     The model tracks the position and info of the selected object.
#     """

#     class PositionItem(sc.AbstractManipulatorItem):
#         """
#         The Model Item represents the position. It doesn't contain anything
#         because we take the position directly from USD when requesting.
#         """
#         def __init__(self) -> None:
#             super().__init__()
#             self.value = [0, 0, 0]


#     def __init__(self, manipulator) -> None:
#         super().__init__()

#         self.prim = None
#         self.current_path = ""
#         self.stage_listener = None
#         self.position = ObjInfoModel.PositionItem()
#         self.usd_context = omni.usd.get_context()

#         # Track selection changes
#         self.events = self.usd_context.get_stage_event_stream()
#         self.stage_event_delegate = self.events.create_subscription_to_pop(
#             self.on_stage_event, name="Object Info Selection Update"
#         )
#         self.manipulator = manipulator

#     def on_stage_event(self, event):
#         if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):

#             prim_paths = self.usd_context.get_selection().get_selected_prim_paths()
#             print(prim_paths)
            
#             if not prim_paths:
#                 self.current_path = ""
#                 self._item_changed(self.position)
#                 return
            
           
            
#             stage = self.usd_context.get_stage()
#             # prim = stage.GetPrimAtPath(prim_path[0])

#             # if not prim.IsA(UsdGeom.Imageable):
#             #     self.prim = None
#             #     if self.stage_listener:
#             #         self.stage_listener.Revoke()
#             #         self.stage_listener = None
#             #     return

#             for prim_path in prim_paths:
#                 prim = stage.GetPrimAtPath(prim_path)
                
#                 if not prim.IsA(UsdGeom.Imageable):
#                     continue
            
            
#             if self.manipulator:
#                 self.manipulator.add_selected_prim(prim_path)

#             if not self.stage_listener:
#                 self.stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self.notice_changed, stage)

#             self.prim = prim
#             self.current_path = prim_path[0]

#             # Position is changed because new selected object has a different position
#             self._item_changed(self.position)

#     def get_item(self, identifier):
#         if identifier == "name":
#             return self.current_path
        
#         elif identifier == "position":
#             return self.position

#     def get_position(self):
#         stage = self.usd_context.get_stage()
#         if not stage or self.current_path == "":
#             return [0, 0, 0]

#         prim = stage.GetPrimAtPath(self.current_path)
#         return self.get_position_for_prim(prim)

#     def get_position_for_prim(self, prim):
#         """Returns position of the given prim"""
#         stage = self.usd_context.get_stage()
#         if not stage or not prim:
#             return [0, 0, 0]

#         box_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_])
#         bound = box_cache.ComputeWorldBound(prim)
#         range = bound.ComputeAlignedBox()
#         bboxMin = range.GetMin()
#         bboxMax = range.GetMax()

#         x_Pos = (bboxMin[0] + bboxMax[0]) * 0.5
#         y_Pos = bboxMax[1] + 5
#         z_Pos = (bboxMin[2] + bboxMax[2]) * 0.5
#         position = [x_Pos, y_Pos, z_Pos]
#         return position
        
#     # def get_as_floats(self, item):
#     #     if item == self.position:
#     #         return self.get_position()
#     #     if item:
#     #         return item.value

#     #     return []

    
#     def notice_changed(self, notice: Usd.Notice, stage: Usd.Stage) -> None:
#         """Called by Tf.Notice.  Used when the current selected object changes in some way."""
#         for p in notice.GetChangedInfoOnlyPaths():
#             if self.current_path in str(p.GetPrimPath()):
#                 self._item_changed(self.position)

#     def destroy(self):
#         self.events = None
#         self.stage_event_delegate.unsubscribe()

from pxr import Tf
from pxr import Usd
from pxr import UsdGeom

from omni.ui import scene as sc
import omni.usd
from .object_info_manipulator import ObjInfoManipulator
from context_storage import selected_prims


class ObjInfoModel(sc.AbstractManipulatorModel):
    """
    The model tracks the position and info of the selected object.
    """

    class PositionItem(sc.AbstractManipulatorItem):
        """
        The Model Item represents the position. It doesn't contain anything
        because we take the position directly from USD when requesting.
        """
        def __init__(self) -> None:
            super().__init__()
            self.value = [0, 0, 0]


    def __init__(self, manipulator) -> None:
        super().__init__()

        self.prim = None
        self.current_path = ""
        self.stage_listener = None
        self.position = ObjInfoModel.PositionItem()
        self.usd_context = omni.usd.get_context()

        # Track selection changes
        self.events = self.usd_context.get_stage_event_stream()
        self.stage_event_delegate = self.events.create_subscription_to_pop(
            self.on_stage_event, name="Object Info Selection Update"
        )
        self.manipulator = manipulator

    def on_stage_event(self, event):
        # manipulator = ObjInfoManipulator()
        # print(f"Manipulator selected prims: {manipulator.selected_prims}")
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):

            prim_path = self.usd_context.get_selection().get_selected_prim_paths()
            print("Selected paths:", prim_path)
            
            if not prim_path:
                self.current_path = ""
                self._item_changed(self.position)
                return
            
            if self.manipulator:
                self.manipulator.add_selected_prim(prim_path[0])
            else:
                print("No prim path selected.") 

            stage = self.usd_context.get_stage()
            prim = stage.GetPrimAtPath(prim_path[0])
            print("prmbpth", prim)



            if not prim.IsA(UsdGeom.Imageable):
                self.prim = None
                if self.stage_listener:
                    self.stage_listener.Revoke()
                    self.stage_listener = None
                return

            if not self.stage_listener:
                self.stage_listener = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self.notice_changed, stage)

            self.prim = prim
            self.current_path = prim_path[0]

            # Position is changed because new selected object has a different position
            self._item_changed(self.position)

    def get_item(self, identifier):
        if identifier == "name":
            return self.current_path
        
        elif identifier == "position":
            return self.position

    def get_position(self):
        stage = self.usd_context.get_stage()
        if not stage or self.current_path == "":
            return [0, 0, 0]

        prim = stage.GetPrimAtPath(self.current_path)
        return self.get_position_for_prim(prim)

    # New method to get position for any given prim
    def get_position_for_prim(self, prim):
        """Returns position of the given prim"""
        stage = self.usd_context.get_stage()
        if not stage or not prim:
            return [0, 0, 0]

        box_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_])
        bound = box_cache.ComputeWorldBound(prim)
        range = bound.ComputeAlignedBox()
        bboxMin = range.GetMin()
        bboxMax = range.GetMax()

        x_Pos = (bboxMin[0] + bboxMax[0]) * 0.5
        y_Pos = bboxMax[1] + 5
        z_Pos = (bboxMin[2] + bboxMax[2]) * 0.5
        position = [x_Pos, y_Pos, z_Pos]
        return position
        
   
    def notice_changed(self, notice: Usd.Notice, stage: Usd.Stage) -> None:
        """Called by Tf.Notice.  Used when the current selected object changes in some way."""
        for p in notice.GetChangedInfoOnlyPaths():
            if self.current_path in str(p.GetPrimPath()):
                self._item_changed(self.position)

    def destroy(self):
        self.events = None
        self.stage_event_delegate.unsubscribe()
