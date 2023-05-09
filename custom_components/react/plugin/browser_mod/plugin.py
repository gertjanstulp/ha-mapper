from custom_components.react.plugin.browser_mod.provider import BrowserModProvider
from custom_components.react.plugin.browser_mod.const import MEDIA_PLAYER_BROWSER_MOD_PROVIDER
from custom_components.react.plugin.const import PROVIDER_TYPE_MEDIA_PLAYER
from custom_components.react.plugin.api import HassApi, PluginApi
from custom_components.react.plugin.factory import PluginBase
from custom_components.react.utils.logger import get_react_logger
from custom_components.react.utils.struct import DynamicData


class Plugin(PluginBase):
    def load(self, plugin_api: PluginApi, hass_api: HassApi, config: DynamicData):
        get_react_logger().debug(f"Browser mod plugin: Loading")
        
        plugin_api.register_plugin_provider(
            PROVIDER_TYPE_MEDIA_PLAYER, 
            MEDIA_PLAYER_BROWSER_MOD_PROVIDER, 
            BrowserModProvider(plugin_api, hass_api))
