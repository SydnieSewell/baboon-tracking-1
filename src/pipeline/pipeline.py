from abc import ABC
from typing import Callable, List
from pipeline.parent_stage import ParentStage

from pipeline.stage import Stage
from pipeline.serial import Serial
from pipeline.parallel import Parallel
from pipeline.stage_result import StageResult


class Pipeline(ABC):
    def __init__(
        self, name: str, *stage_types: List[Stage], parallel=False, runtime_config=None
    ):
        ParentStage.static_stages = []

        if parallel:
            self.stage = Parallel(name, runtime_config, *stage_types)
        else:
            self.stage = Serial(name, runtime_config, *stage_types)

        self.stage.on_init()

    def step(self) -> StageResult:
        """
        Runs one step of the algorithm.
        """
        self.stage.before_execute()
        result = self.stage.execute()
        self.stage.after_execute()

        return result

    def run(self):
        """
        Runs the algorithm until it finishes.
        """

        while True:
            result = self.step()

            if not result.continue_pipeline:
                print("Average Runtime per stage:")
                self.stage.get_time().print_to_console()

                self.stage.on_destroy()

                return

    def get(self, stage_type: Callable):
        """
        Get a type from the pipeline.
        """
        candidate_stages = [
            s for s in ParentStage.static_stages if isinstance(s, stage_type)
        ]

        return candidate_stages[-1]
