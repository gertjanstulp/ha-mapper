import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from custom_components.react.const import CONF_ENTITY_MAPS

from custom_components.react.plugin.const import PROVIDER_TYPE_MQTT
from custom_components.react.plugin.factory import ApiSetupCallback, InputBlockSetupCallback, OutputBlockSetupCallback, PluginSetup, ProviderSetupCallback
from custom_components.react.plugin.mqtt.api import MqttApi
from custom_components.react.plugin.mqtt.config import MqttConfig
from custom_components.react.plugin.mqtt.const import (
    ATTR_MQTT_PROVIDER, 
    MQTT_GENERIC_PROVIDER
)
from custom_components.react.plugin.mqtt.input.double_press_input_block import MqttDoublePressInputBlock
from custom_components.react.plugin.mqtt.input.long_press_input_block import MqttLongPressInputBlock
from custom_components.react.plugin.mqtt.input.short_press_input_block import MqttShortPressInputBlock
from custom_components.react.plugin.mqtt.output.publish_output_block import MqttPublishOutputBlock
from custom_components.react.plugin.mqtt.provider import MqttProvider


MQTT_PLUGIN_CONFIG_SCHEMA = vol.Schema({
    vol.Optional(ATTR_MQTT_PROVIDER) : cv.string,
    vol.Optional(CONF_ENTITY_MAPS) : dict,
})


class Setup(PluginSetup[MqttConfig]):
    def __init__(self) -> None:
        super().__init__(MQTT_PLUGIN_CONFIG_SCHEMA)


    def setup_config(self, raw_config: dict) -> MqttConfig:
        return MqttConfig(raw_config)
    

    def setup_api(self, setup: ApiSetupCallback):
        setup(MqttApi)


    def setup_provider(self, setup: ProviderSetupCallback):
        setup(MqttProvider, PROVIDER_TYPE_MQTT, MQTT_GENERIC_PROVIDER)
    
    
    def setup_input_blocks(self, setup: InputBlockSetupCallback):
        setup(MqttShortPressInputBlock)
        setup(MqttLongPressInputBlock)
        setup(MqttDoublePressInputBlock)
    

    def setup_output_blocks(self, setup: OutputBlockSetupCallback):
        setup(MqttPublishOutputBlock)
