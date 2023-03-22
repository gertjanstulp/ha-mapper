from __future__ import annotations

from homeassistant.core import Event
from homeassistant.const import STATE_OFF

from custom_components.react.base import ReactBase
from custom_components.react.const import REACT_TYPE_SWITCH
from custom_components.react.plugin.switch.api import Api
from custom_components.react.plugin.switch.const import PLUGIN_NAME
from custom_components.react.tasks.plugin.base import PluginReactionTask
from custom_components.react.utils.events import ReactionEvent
from custom_components.react.utils.logger import get_react_logger
from custom_components.react.utils.struct import DynamicData

_LOGGER = get_react_logger()


class SwitchTurnOffTask(PluginReactionTask):

    def __init__(self, react: ReactBase, api: Api) -> None:
        super().__init__(react, SwitchTurnOffReactionEvent)
        self.api = api


    def _debug(self, message: str):
        _LOGGER.debug(f"Switch plugin: SwitchTurnOffTask - {message}")


    async def async_execute_plugin(self, event: SwitchTurnOffReactionEvent):
        self._debug(f"Turning off switch '{event.payload.entity}'")
        await self.api.async_switch_turn_off(event.context, event.payload.entity)
        

class SwitchTurnOffReactionEventData(DynamicData):

    def __init__(self, source: dict) -> None:
        super().__init__()
        
        self.plugin: str = None

        self.load(source)


class SwitchTurnOffReactionEvent(ReactionEvent[SwitchTurnOffReactionEventData]):
    
    def __init__(self, event: Event) -> None:
        super().__init__(event, SwitchTurnOffReactionEventData)
        

    @property
    def applies(self) -> bool:
        return (
            self.payload.type == REACT_TYPE_SWITCH and
            self.payload.action == STATE_OFF and 
            (not self.payload.data or
             (self.payload.data and (
              (not self.payload.data.plugin or 
               self.payload.data.plugin == PLUGIN_NAME))))
        )
