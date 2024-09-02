from pxr import Tf
from pxr import Usd
from pxr import UsdGeom

from omni.ui import scene as sc
import omni.usd
import json
import os


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

    def __init__(self) -> None:
        super().__init__()

        self.prim = None
        self.current_path = ""
        self.stage_listener = None
        self.position = ObjInfoModel.PositionItem()
        self.usd_context = omni.usd.get_context()

        self.events = self.usd_context.get_stage_event_stream()
        self.stage_event_delegate = self.events.create_subscription_to_pop(
            self.on_stage_event, name="Object Info Selection Update"
        )
        self.all_prims = None
        # self.selected_children = None
        self.custom_data = self._load_json_data()

    @staticmethod
    def _load_json_data():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "custom_data.json")

        with open(file_path, "r", encoding="utf-8") as json_data:
            loaded_data = json.load(json_data)

        return loaded_data

    def on_stage_event(self, event):
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):

            self.all_prims = self.usd_context.get_selection().get_selected_prim_paths()

            if not self.all_prims:
                self.current_path = ""
                self._item_changed(self.position)
                return

            stage = self.usd_context.get_stage()

            for prim_path in self.all_prims:
                prim = stage.GetPrimAtPath(prim_path)

                if prim.GetTypeName() == "Scope":
                    self.select_all_children(prim.GetAllChildren())

                if not prim.IsA(UsdGeom.Imageable):
                    self.prim = None
                    if self.stage_listener:
                        self.stage_listener.Revoke()
                        self.stage_listener = None
                    return

                if not self.stage_listener:
                    self.stage_listener = Tf.Notice.Register(
                        Usd.Notice.ObjectsChanged, self.notice_changed, stage
                    )

                self.prim = prim
                self.current_path = prim_path

                self._item_changed(self.position)

                # Setting metadata based on prim path
                if self.custom_data:
                    for data_object in self.custom_data:
                        if prim_path in data_object.values():
                            prim.SetCustomData(data_object)
                print("Meta", prim.GetCustomData())

    def get_item(self, identifier):
        if identifier == "name":
            return self.current_path

        elif identifier == "position":
            return self.position

        elif identifier == "all_prims":
            return self.all_prims

    def get_position(self):
        stage = self.usd_context.get_stage()
        if not stage or self.current_path == "":
            return [0, 0, 0]

        prim = stage.GetPrimAtPath(self.current_path)
        return self.get_position_for_prim(prim)

    @staticmethod
    def get_position_for_prim(prim):
        """Returns position of the given prim"""

        box_cache = UsdGeom.BBoxCache(
            Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_]
        )
        bound = box_cache.ComputeWorldBound(prim)
        range = bound.ComputeAlignedBox()
        bboxMin = range.GetMin()
        bboxMax = range.GetMax()

        x_Pos = (bboxMin[0] + bboxMax[0]) * 0.5
        y_Pos = bboxMax[1] + 5
        z_Pos = (bboxMin[2] + bboxMax[2]) * 0.5
        position = [x_Pos, y_Pos, z_Pos]
        return position

    def select_all_children(self, prims):
        """Selects all prims given a list of prim objects."""
        # Convert prim objects to their paths
        prim_paths = [prim.GetPath().pathString for prim in prims]
        selection = self.usd_context.get_selection()
        selection.set_selected_prim_paths(prim_paths, False)

    def notice_changed(self, notice: Usd.Notice, stage: Usd.Stage) -> None:
        """Called by Tf.Notice.  Used when the current selected object changes in some way."""

        for p in notice.GetChangedInfoOnlyPaths():
            if self.current_path in str(p.GetPrimPath()):
                self._item_changed(self.position)

    def destroy(self):
        self.events = None
        self.stage_event_delegate.unsubscribe()
