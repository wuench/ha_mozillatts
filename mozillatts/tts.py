import voluptuous as vol
import urllib, logging
import http.client as http
from urllib.parse import urlencode

from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_HOST, CONF_PORT
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_VOICE = "voice"
CONF_CODEC = "codec"

SUPPORT_LANGUAGES = ["en_US"]
SUPPORT_CODEC = ["WAVE_FILE"]

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5002
DEFAULT_LANG = "en_US"
DEFAULT_CODEC = "WAVE_FILE"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port
    }
)

def get_engine(hass, config, discovery_info=None):
    return MozillaTTSProvider(hass, config)


class MozillaTTSProvider(Provider):
    def __init__(self, hass, conf):
        """Init MaryTTS TTS service."""
        self.hass = hass
        self.name = "MozillaTTS"
        self._host = conf.get(CONF_HOST)
        self._port = conf.get(CONF_PORT)

    @property
    def default_language(self):
        """Return the default language."""
        return DEFAULT_LANG
    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    def get_tts_audio(self, message, language, options=None):
        raw_params = {
            "text": message
        }

        conn = http.HTTPConnection(self._host, self._port)

        conn.request("GET", "/api/tts?" + urlencode(raw_params))
        response = conn.getresponse()

        if response.status != 200:
            raise Exception("{0} - {1}: '{2}''".format(response.status, response.reason, response.readline()))

        return 'wav', response.read()
