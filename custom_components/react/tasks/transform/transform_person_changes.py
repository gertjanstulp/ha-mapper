""""Store React data."""
from __future__ import annotations
from typing import Any

from homeassistant.core import Event as HassEvent

from ..transform_base import NonBinaryStateData, StateData, StateTransformTask

from ...base import ReactBase

from ...const import (
    PERSON, 
    PERSON_PREFIX,
)


async def async_setup_task(react: ReactBase) -> Task:
    """Set up this task."""
    return Task(react=react)


class PersonStateData(NonBinaryStateData):
    
    def __init__(self, event_payload: dict[str, Any]):
        super().__init__(PERSON_PREFIX, event_payload)

        if self.old_state_value != self.new_state_value:
            self.actions.append(self.new_state_value)


class Task(StateTransformTask):
    """ "React task base."""
    
    def __init__(self, react: ReactBase) -> None:
        super().__init__(react, PERSON_PREFIX, PERSON)
        self.can_run_disabled = True


    def read_state_data(self, hass_event: HassEvent) -> StateData:
        return PersonStateData(hass_event.data)
