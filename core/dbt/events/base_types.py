from abc import ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass
from datetime import datetime
import os
<<<<<<< HEAD
from typing import Any, Optional
=======
from typing import Any, Dict, Optional
>>>>>>> 31c9528b (fixed some merg issues)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# These base types define the _required structure_ for the concrete event #
# types defined in types.py                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# in preparation for #3977
class TestLevel():
    def level_tag(self) -> str:
        return "test"


class DebugLevel():
    def level_tag(self) -> str:
        return "debug"


class InfoLevel():
    def level_tag(self) -> str:
        return "info"


class WarnLevel():
    def level_tag(self) -> str:
        return "warn"


class ErrorLevel():
    def level_tag(self) -> str:
        return "error"


@dataclass
class ShowException():
    # N.B.:
    # As long as we stick with the current convention of setting the member vars in the
    # `message` method of subclasses, this is a safe operation.
    # If that ever changes we'll want to reassess.
    def __post_init__(self):
        self.exc_info: Any = True
        self.stack_info: Any = None
        self.extra: Any = None


# TODO add exhaustiveness checking for subclasses
# can't use ABCs with @dataclass because of https://github.com/python/mypy/issues/5374
# top-level superclass for all events
class Event(metaclass=ABCMeta):
    # fields that should be on all events with their default implementations
    log_version: int = 1
    ts: Optional[datetime] = None  # use getter for non-optional
    pid: Optional[int] = None  # use getter for non-optional

    # four digit string code that uniquely identifies this type of event
    # uniqueness and valid characters are enforced by tests
    @abstractproperty
    @staticmethod
    def code() -> str:
        raise Exception("code() not implemented for event")

    # do not define this yourself. inherit it from one of the above level types.
    @abstractmethod
    def level_tag(self) -> str:
        raise Exception("level_tag not implemented for Event")

    # Solely the human readable message. Timestamps and formatting will be added by the logger.
    # Must override yourself
    @abstractmethod
    def message(self) -> str:
        raise Exception("msg not implemented for Event")

    # exactly one time stamp per concrete event
    def get_ts(self) -> datetime:
        if not self.ts:
            self.ts = datetime.now()
        return self.ts

    # exactly one pid per concrete event
    def get_pid(self) -> int:
        if not self.pid:
            self.pid = os.getpid()
        return self.pid
    
    def node_info(self, state: str) -> Dict:
    #          Examples
    # "node_info": 
    #     {"node_path": "models/slow.sql", 
    #     "node_name": "slow", 
    #     "resource_type": "model", 
    #     "node_materialized": "table", 
    #     "node_started_at": "2021-10-05T13:17:28.018613", 
    #     "unique_id": "model.my_new_project.slow", 
    #     "run_state": "running"}}
    # "node_info": 
    #     {"node_path": "models/slow.sql", 
    #     "node_name": "slow", 
    #     "resource_type": "model", 
    #     "node_materialized": "table", 
    #     "node_started_at": "2021-10-05T13:17:28.018613", 
    #     "unique_id": "model.my_new_project.slow", 
    #     "node_finished_at": "2021-10-05T13:17:29.134126", 
    #     "node_status": "passed", 
    #     "run_state": "running"}}
        return {
            "node_path": self.path, 
            "node_name": self.name, 
            "resource_type": self.resource_type, 
            "node_materialized": self.materialized, 
            "node_started_at": "TODO", 
            "unique_id": self.unique_id, 
            "node_finished_at": "TODO", 
            "node_status": "TODO", 
            "run_state": state
        }


class File(Event, metaclass=ABCMeta):
    # Solely the human readable message. Timestamps and formatting will be added by the logger.
    def file_msg(self) -> str:
        # returns the event msg unless overriden in the concrete class
        return self.message()


class Cli(Event, metaclass=ABCMeta):
    # Solely the human readable message. Timestamps and formatting will be added by the logger.
    def cli_msg(self) -> str:
        # returns the event msg unless overriden in the concrete class
        return self.message()
