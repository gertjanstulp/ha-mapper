from custom_components.react.plugin.google_translate.const import TTS_GOOGLE_TRANSLATE_PROVIDER
from custom_components.react.plugin.media_player.config import TtsConfig
from custom_components.react.plugin.media_player.provider import TtsProvider
from custom_components.react.plugin.plugin_factory import HassApi, PluginApi


class GoogleTranslateTtsProvider(TtsProvider):
    def __init__(self, plugin_api: PluginApi, hass_api: HassApi, config: TtsConfig) -> None:
        super().__init__(plugin_api, hass_api, config, TTS_GOOGLE_TRANSLATE_PROVIDER)
