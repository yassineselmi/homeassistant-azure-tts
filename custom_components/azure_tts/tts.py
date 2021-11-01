"""Support for the Microsoft Azure TTS service."""
import logging
import voluptuous as vol
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_API_KEY, CONF_REGION, CONF_TYPE, PERCENTAGE
import homeassistant.helpers.config_validation as cv
import requests
from xml.etree import ElementTree

speech_url_template = "https://{}.tts.speech.microsoft.com/cognitiveservices/v1"

_LOGGER = logging.getLogger(__name__)

CONF_GENDER = "gender"
CONF_OUTPUT = "output"
CONF_RATE = "rate"
CONF_VOLUME = "volume"
CONF_PITCH = "pitch"
CONF_CONTOUR = "contour"

#todo
SUPPORTED_LANGUAGES = [
    "en-US", "fr-FR", "fr-CA"
]

GENDERS = ["Female", "Male"]

DEFAULT_LANG = "en-US"
DEFAULT_GENDER = "Female"
DEFAULT_TYPE = "AriaNeural"
DEFAULT_OUTPUT = "audio-16khz-128kbitrate-mono-mp3"
DEFAULT_RATE = 0
DEFAULT_VOLUME = 0
DEFAULT_PITCH = "default"
DEFAULT_CONTOUR = ""
DEFAULT_REGION = "eastus"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORTED_LANGUAGES),
        vol.Optional(CONF_GENDER, default=DEFAULT_GENDER): vol.In(GENDERS),
        vol.Optional(CONF_TYPE, default=DEFAULT_TYPE): cv.string,
        vol.Optional(CONF_RATE, default=DEFAULT_RATE): vol.All(
            vol.Coerce(int), vol.Range(-100, 100)
        ),
        vol.Optional(CONF_VOLUME, default=DEFAULT_VOLUME): vol.All(
            vol.Coerce(int), vol.Range(-100, 100)
        ),
        vol.Optional(CONF_PITCH, default=DEFAULT_PITCH): cv.string,
        vol.Optional(CONF_CONTOUR, default=DEFAULT_CONTOUR): cv.string,
        vol.Optional(CONF_REGION, default=DEFAULT_REGION): cv.string,
    }
)


def get_engine(hass, config, discovery_info=None):
    """Set up Reverso speech component."""
    return AzureProvider(
        config[CONF_API_KEY],
        config[CONF_LANG],
        config[CONF_GENDER],
        config[CONF_TYPE],
        config[CONF_RATE],
        config[CONF_VOLUME],
        config[CONF_PITCH],
        config[CONF_CONTOUR],
        config[CONF_REGION],
    )

class AzureProvider(Provider):
    def __init__(
        self, apikey, lang, gender, ttype, rate, volume, pitch, contour, region
        ):
        """Initialize Azure TTS provider."""
        self._apikey = apikey
        self._lang = lang
        self._gender = gender
        self._type = ttype
        self._output = DEFAULT_OUTPUT
        self._rate = f"{rate}{PERCENTAGE}"
        self._volume = f"{volume}{PERCENTAGE}"
        self._pitch = pitch
        self._contour = contour
        self._region = region
        self.name = "AzureTTS"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORTED_LANGUAGES

    def get_tts_audio(self, message, language, options=None):
        """Load TTS using pyttsreverso."""
        if language is None:
            language = self._lang
        
        endpoint = speech_url_template.format(self._region)

        try:
            headers = {
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": self._output,
                "Ocp-Apim-Subscription-Key": self._apikey,
                "User-Agent": "HASSTTS"
                }
            

            body = ElementTree.Element('speak', version='1.0')
            body.set('{http://www.w3.org/XML/1998/namespace}lang', language)

            voice = ElementTree.SubElement(body, 'voice')
            voice.set('{http://www.w3.org/XML/1998/namespace}lang', language)
            voice.set('{http://www.w3.org/XML/1998/namespace}gender', self._gender)
            voice.set(
                'name', 'Microsoft Server Speech Text to Speech Voice (' + language + ', ' + self._type +')')


            voice.append(ElementTree.XML('<prosody>' + message + '</prosody>'))
            prosody = voice.find('prosody')
            prosody.set('rate', self._rate)
            prosody.set('volume', self._volume)
            prosody.set('pitch', self._pitch)
            prosody.set('contour', self._contour)

            _LOGGER.info(ElementTree.tostring(body))

            response = requests.post(endpoint, ElementTree.tostring(body), headers=headers)

            data = response.content

        except Exception as e:
            _LOGGER.error("Error occurred for Azure TTS: %s", e)
            return (None, None)
        return ("mp3", data)