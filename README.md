[![hacs_badge](https://img.shields.io/badge/HACS-Default-green.svg)](https://github.com/custom-components/hacs)
# Azure Text-to-speech service for Home Assistant
The Azure text-to-speech platform uses online Azure Text-to-Speech cognitive service to read a text with natural sounding voice.

The main reason behind this custom integration is to decouple the Microsoft TTS service from the python library  `pycsspeechtts` used by the ["official" integration](https://www.home-assistant.io/integrations/microsoft/).

This integration uses the native Azure Cognitive Speech Service Text-to-speech REST API (I know.. it is too long for a service name).

## Features
* Supports multi language. You can find the full list of languages [here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech).
* Supports SSML.

## Basic Configuration

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

## Configuration variables

This integration accepts the same configuration variables as the out-of-the-box [Microsoft TTS](https://www.home-assistant.io/integrations/microsoft/#configuration-variables)].

