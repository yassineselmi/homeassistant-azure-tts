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

SUPPORTED_LANGUAGES = [
    "af-ZA",
    "af-ZA",
    "am-ET",
    "am-ET",
    "ar-AE",
    "ar-AE",
    "ar-BH",
    "ar-BH",
    "ar-DZ",
    "ar-DZ",
    "ar-EG",
    "ar-EG",
    "ar-IQ",
    "ar-IQ",
    "ar-JO",
    "ar-JO",
    "ar-KW",
    "ar-KW",
    "ar-LY",
    "ar-LY",
    "ar-MA",
    "ar-MA",
    "ar-QA",
    "ar-QA",
    "ar-SA",
    "ar-SA",
    "ar-SY",
    "ar-SY",
    "ar-TN",
    "ar-TN",
    "ar-YE",
    "ar-YE",
    "bg-BG",
    "bg-BG",
    "bn-BD",
    "bn-BD",
    "ca-ES",
    "ca-ES",
    "ca-ES",
    "cs-CZ",
    "cs-CZ",
    "cy-GB",
    "cy-GB",
    "da-DK",
    "da-DK",
    "de-AT",
    "de-AT",
    "de-CH",
    "de-CH",
    "de-DE",
    "de-DE",
    "el-GR",
    "el-GR",
    "en-AU",
    "en-AU",
    "en-CA",
    "en-CA",
    "en-GB",
    "en-GB",
    "en-GB",
    "en-GB",
    "en-HK",
    "en-HK",
    "en-IE",
    "en-IE",
    "en-IN",
    "en-IN",
    "en-KE",
    "en-KE",
    "en-NG",
    "en-NG",
    "en-NZ",
    "en-NZ",
    "en-PH",
    "en-PH",
    "en-SG",
    "en-SG",
    "en-TZ",
    "en-TZ",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-US",
    "en-ZA",
    "en-ZA",
    "es-AR",
    "es-AR",
    "es-BO",
    "es-BO",
    "es-CL",
    "es-CL",
    "es-CO",
    "es-CO",
    "es-CR",
    "es-CR",
    "es-CU",
    "es-CU",
    "es-DO",
    "es-DO",
    "es-EC",
    "es-EC",
    "es-ES",
    "es-ES",
    "es-GQ",
    "es-GQ",
    "es-GT",
    "es-GT",
    "es-HN",
    "es-HN",
    "es-MX",
    "es-MX",
    "es-NI",
    "es-NI",
    "es-PA",
    "es-PA",
    "es-PE",
    "es-PE",
    "es-PR",
    "es-PR",
    "es-PY",
    "es-PY",
    "es-SV",
    "es-SV",
    "es-US",
    "es-US",
    "es-UY",
    "es-UY",
    "es-VE",
    "es-VE",
    "et-EE",
    "et-EE",
    "fa-IR",
    "fa-IR",
    "fi-FI",
    "fi-FI",
    "fi-FI",
    "fil-PH",
    "fil-PH",
    "fr-BE",
    "fr-BE",
    "fr-CA",
    "fr-CA",
    "fr-CA",
    "fr-CH",
    "fr-CH",
    "fr-FR",
    "fr-FR",
    "ga-IE",
    "ga-IE",
    "gl-ES",
    "gl-ES",
    "gu-IN",
    "gu-IN",
    "he-IL",
    "he-IL",
    "hi-IN",
    "hi-IN",
    "hr-HR",
    "hr-HR",
    "hu-HU",
    "hu-HU",
    "id-ID",
    "id-ID",
    "it-IT",
    "it-IT",
    "it-IT",
    "ja-JP",
    "ja-JP",
    "jv-ID",
    "jv-ID",
    "km-KH",
    "km-KH",
    "ko-KR",
    "ko-KR",
    "lt-LT",
    "lt-LT",
    "lv-LV",
    "lv-LV",
    "mr-IN",
    "mr-IN",
    "ms-MY",
    "ms-MY",
    "mt-MT",
    "mt-MT",
    "my-MM",
    "my-MM",
    "nb-NO",
    "nb-NO",
    "nb-NO",
    "nl-BE",
    "nl-BE",
    "nl-NL",
    "nl-NL",
    "nl-NL",
    "pl-PL",
    "pl-PL",
    "pl-PL",
    "pt-BR",
    "pt-BR",
    "pt-PT",
    "pt-PT",
    "pt-PT",
    "ro-RO",
    "ro-RO",
    "ru-RU",
    "ru-RU",
    "ru-RU",
    "sk-SK",
    "sk-SK",
    "sl-SI",
    "sl-SI",
    "so-SO",
    "so-SO",
    "su-ID",
    "su-ID",
    "sv-SE",
    "sv-SE",
    "sv-SE",
    "sw-KE",
    "sw-KE",
    "sw-TZ",
    "sw-TZ",
    "ta-IN",
    "ta-IN",
    "ta-LK",
    "ta-LK",
    "ta-SG",
    "ta-SG",
    "te-IN",
    "te-IN",
    "th-TH",
    "th-TH",
    "th-TH",
    "tr-TR",
    "tr-TR",
    "uk-UA",
    "uk-UA",
    "ur-IN",
    "ur-IN",
    "ur-PK",
    "ur-PK",
    "uz-UZ",
    "uz-UZ",
    "vi-VN",
    "vi-VN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-CN",
    "zh-HK",
    "zh-HK",
    "zh-HK",
    "zh-TW",
    "zh-TW",
    "zh-TW",
    "zu-ZA",
    "zu-ZA"
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

            _LOGGER.debug(ElementTree.tostring(body))

            response = requests.post(endpoint, ElementTree.tostring(body), headers=headers)

            data = response.content

        except Exception as e:
            _LOGGER.error("Error occurred for Azure TTS: %s", e)
            return (None, None)
        return ("mp3", data)
