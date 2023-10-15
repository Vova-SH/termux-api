<p align="right">
  <a href="./README.md">English</a>
  |
  <a href="./README.ru-RU.md">Русский</a>
</p>

# Termux API Integration Component for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![release version](https://img.shields.io/github/release/Vova-SH/termux-api/all.svg)](https://github.com/Vova-SH/termux-api/releases)
[![maintainer](https://img.shields.io/badge/maintainer-%40Vova--SH-green)](https://github.com/Vova-SH)

This component allows, when running Home Assistant on Android via [Termux](https://termux.dev), to display various metrics through [Termux:API](https://wiki.termux.com/wiki/Termux:API).

## Minimum requirements for the component to work

* Home Assistant running inside Termux
* Termux:API package installed (`pkg install termux-api`)

## What's supported in the integration

**termux-battery-status**

* Health
* Percentage
* Plug
* Status
* Temperature


**termux-brightness**

* Adjusting the range from 0 to 255
* Auto-brightness on/off (Selected through turning the light source on/off)


**termux-volume**

Adjusting the following volumes:

* alarm
* music
* notification
* ring
* system
* call


**termux-camera-info/termux-camera-photo**

* Taking photos with the available front/back smartphone camera
* Stream on/off

Implemented photo retrieval with updates every [10 seconds](https://github.com/Vova-SH/termux-api/blob/main/custom_components/termux_api/cam/entity.py#L38). When turned off, the photo is replaced by a placeholder, which if necessary, can be set to replace at [custom_components/termux_api/cam/placeholder.jpg](https://github.com/Vova-SH/termux-api/blob/main/custom_components/termux_api/cam/placeholder.jpg)

## Ссылки
* [Usage example (RUS)](https://habr.com/ru/companies/domclick/articles/675770/)
* [Partial control based on basic HA components](https://github.com/Vova-SH/HomeAssistanceConfiguration/tree/main)