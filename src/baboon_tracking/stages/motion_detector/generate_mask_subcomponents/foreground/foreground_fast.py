"""
Calculate the foreground of the current frame.
"""
import numpy as np
import time
from baboon_tracking.mixins.foreground_mixin import ForegroundMixin
from baboon_tracking.mixins.intersected_frames_mixin import IntersectedFramesMixin
from baboon_tracking.mixins.preprocessed_frame_mixin import PreprocessedFrameMixin
from baboon_tracking.mixins.unioned_frames_mixin import UnionedFramesMixin
from baboon_tracking.mixins.group_shifted_history_frames_mixin import (
    GroupShiftedHistoryFramesMixin,
)
from baboon_tracking.mixins.quantized_frames_mixin import QuantizedFramesMixin
from baboon_tracking.mixins.shifted_history_frames_mixin import (
    ShiftedHistoryFramesMixin,
)
from baboon_tracking.mixins.weights_mixin import WeightsMixin
from baboon_tracking.stages.motion_detector.generate_mask_subcomponents.foreground import (
    foreground_c,
)

from pipeline import Stage
from pipeline.decorators import config, stage
from pipeline.stage_result import StageResult


@stage("shifted_history_frames")
@stage("quantized_frames")
@stage("preprocessed_frame")
@stage("weights")
@config(parameter_name="history_frames", key="history_frames")
class ForegroundFast(
    Stage,
    GroupShiftedHistoryFramesMixin,
    IntersectedFramesMixin,
    UnionedFramesMixin,
    ForegroundMixin,
):
    """
    Calculate the foreground of the current frame.
    """

    def __init__(
        self,
        shifted_history_frames: ShiftedHistoryFramesMixin,
        quantized_frames: QuantizedFramesMixin,
        preprocessed_frame: PreprocessedFrameMixin,
        weights: WeightsMixin,
        history_frames: int,
    ) -> None:
        Stage.__init__(self)
        GroupShiftedHistoryFramesMixin.__init__(self)
        IntersectedFramesMixin.__init__(self)
        UnionedFramesMixin.__init__(self)
        ForegroundMixin.__init__(self)

        self._shifted_history_frames = shifted_history_frames
        self._quantized_frames = quantized_frames
        self._preprocessed_frame = preprocessed_frame
        self._weights = weights
        self._history_frames = history_frames

    def _intersect_frames(self, frames, q_frames):
        """
        Intersect two consecutive frames to find common background between those two frames
        Returns the single frame produced by intersection
        """
        mask = np.abs(q_frames[0] - q_frames[1]) <= 1
        combined = frames[0].get_frame().copy()
        combined[mask] = 0

        return combined

    def _intersect_all_frames(
        self, grouped_shifted_history_frames, grouped_quantized_frames
    ):
        """
        Takes in two lists of frames, performs intersect on each pair and returns array of intersects
        """
        return [
            self._intersect_frames(z[0], z[1])
            for z in zip(grouped_shifted_history_frames, grouped_quantized_frames)
        ]

    def execute(self) -> StageResult:
        s = time.time()
        shifted_history_frames = self._shifted_history_frames.shifted_history_frames
        quantized_frames = self._quantized_frames.quantized_frames
        """
        frame_group_index = range(len(shifted_history_frames) - 1)
        frame_group_index = [(r, r + 1) for r in frame_group_index]

        self.grouped_shifted_history_frames = [
            (shifted_history_frames[g[0]], shifted_history_frames[g[1]])
            for g in frame_group_index
        ]
        self.grouped_quantized_frames = [
            (quantized_frames[g[0]], quantized_frames[g[1]]) for g in frame_group_index
        ]
        
        intersected_frames_actual = self._intersect_all_frames(
            self.grouped_shifted_history_frames, self.grouped_quantized_frames
        )
        """
        #shifted_history_frames = np.stack([f.get_frame() for f in shifted_history_frames], axis=0)
        #quantized_frames = np.stack(quantized_frames, axis=0)
        # self.intersected_frames = intersected_frames_actual
        '''
        self.unioned_frames = foreground_c.foreground(
            shifted_history_frames, quantized_frames
        )
        '''
        '''
        intersected_frames_fast = foreground_c.foreground(
            shifted_history_frames, quantized_frames
        )
        self.intersected_frames = intersected_frames_fast
        
        self.unioned_frames = foreground_c.union_frames(self.intersected_frames)
        '''
        #s = time.time()
        #t1 = time.time()
        self.foreground = foreground_c.foreground_all(
            shifted_history_frames,
            quantized_frames,
            self._preprocessed_frame.processed_frame.get_frame(),
            self._weights.weights,
            self._history_frames,
        )
        #t2 = time.time()
        #print('pre: ' + str((t1-s)*1000))
        #print('foreground: ' + str((t2-t1)*1000))
        #t = time.time()
        #print('subtract_background: ' + str((t-s)*1000))
        """
        print(type(intersected_frames_actual[0]))
        print(type(self.intersected_frames[0]))
        print(intersected_frames_actual[0].shape)
        print(self.intersected_frames[0].shape)
        
        eq = np.array_equal(intersected_frames_actual,self.intersected_frames)
        if(not eq):
            np.where(intersected_frames_actual!=self.intersected_frames)
            exit()
        
        self.grouped_shifted_history_frames = foreground_c.group_history(shifted_history_frames)
        self.grouped_quantized_frames = foreground_c.group_quantized(quantized_frames)
        
        self.grouped_shifted_history_frames, self.grouped_quantized_frames = (
                foreground_c.group_frames(shifted_history_frames, quantized_frames)
        )
        
        self.intersected_frames = (
            foreground_c.intersect_frames(self.grouped_shifted_history_frames, 
                    self.grouped_quantized_frames)
        )

        self.unioned_frames = foreground_c.union_frames(self.intersected_frames)

        self.foreground = foreground_c.subtract_background(
            self._preprocessed_frame.processed_frame,
            self.unioned_frames,
            self._weights.weights,
            self._history_frames
        )
        """
        return StageResult(True, True)