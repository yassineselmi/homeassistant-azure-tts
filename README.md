[![hacs_badge](https://img.shields.io/badge/HACS-Default-green.svg)](https://github.com/custom-components/hacs)
# Azure Text-to-speech service for Home Assistant
The Azure text-to-speech platform uses online Azure Text-to-Speech cognitive service to read a text with natural sounding voice.

## Features
* Supports multi language. You can find the full list of languages [here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech).
* Supports SSML.

## Configuration Variables

```yaml
# Text to speech
tts:
  - platform: azure_tts
    service_name: azure_say
    api_key: <your_api_key>
    language: en-US
    type: JeanNeural # Optional
    region: eastus # Optional. Default: eastus

```

**`api_key`** string *REQUIRED*

