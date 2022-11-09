from homeassistant.const import Platform
from homeassistant.core import Context
from homeassistant.components.telegram_bot import (
    DOMAIN, 
    SERVICE_EDIT_MESSAGE
)

from custom_components.react.base import ReactBase
from custom_components.react.utils.logger import get_react_logger
from custom_components.react.utils.struct import DynamicData

_LOGGER = get_react_logger()

class ApiConfig(DynamicData):
    """ api config """

class Api():
    def __init__(self, react: ReactBase, config: ApiConfig) -> None:
        self.react = react
        self.config = config


    def _debug(self, message: str):
        _LOGGER.debug(f"Telegram plugin: Api - {message}")


    def _exception(self, message: str):
        _LOGGER.exception(f"Telegram plugin: Api - {message}")


    async def async_send_message(self, entity: str, message_data: dict, context: Context):
        self._debug("Sending message to telegram")
        try:
            await self.react.hass.services.async_call(
                Platform.NOTIFY, 
                entity,
                message_data, 
                context)
        except:
            _LOGGER.exception("Sending message to telegram failed")


    async def async_confirm_feedback(self, feedback_data: dict, context: Context):
        self._debug("Confirming feedback to telegram")
        try:
            await self.react.hass.services.async_call(
                DOMAIN,
                SERVICE_EDIT_MESSAGE,
                service_data=feedback_data, 
                context=context)
        except:
            _LOGGER.exception("Confirming feedback to telegram failed")