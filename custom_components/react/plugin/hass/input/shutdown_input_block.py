from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from custom_components.react.base import ReactBase
from custom_components.react.const import (
    ACTION_SHUTDOWN, 
    ATTR_ACTION, 
    ATTR_ENTITY, 
    ATTR_TYPE, 
    ENTITY_HASS, 
    TYPE_SYSTEM,
)
from custom_components.react.tasks.filters import EVENT_TYPE_FILTER_STRATEGY    
from custom_components.react.tasks.plugin.base import InputBlock
from custom_components.react.utils.events import HassEvent
from custom_components.react.utils.struct import DynamicData


class HassEventShutdownInputBlock(InputBlock[DynamicData]):
    def __init__(self, react: ReactBase) -> None:
        super().__init__(react, HassEvent)
        self.track_event_filter = EVENT_TYPE_FILTER_STRATEGY.get_filter(EVENT_HOMEASSISTANT_STOP)


    def create_action_event_payloads(self, source_event: HassEvent) -> list[dict]:
        source_event.session.debug(self.logger, f"Hass shutdown caught")
        return [{
            ATTR_ENTITY: ENTITY_HASS,
            ATTR_TYPE: TYPE_SYSTEM,
            ATTR_ACTION: ACTION_SHUTDOWN,
        }]