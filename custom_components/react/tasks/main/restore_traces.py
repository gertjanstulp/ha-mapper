from __future__ import annotations

from homeassistant.components.trace import async_restore_traces
from homeassistant.components.trace.const import DATA_TRACE_STORE

from ..base import ReactTask

from ...base import ReactBase
from ...enums import ReactStage


async def async_setup_task(react: ReactBase) -> Task:
    """Set up this task."""
    return Task(react=react)


class Task(ReactTask):
    """Restore React data."""

    def __init__(self, react: ReactBase) -> None:
        super().__init__(react)
        
        self.stages = [ReactStage.SETUP]


    async def async_execute(self) -> None:
        if DATA_TRACE_STORE in self.react.hass.data:
            await async_restore_traces(self.react.hass)