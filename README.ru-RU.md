<p align="right">
  <a href="./README.md">English</a>
  |
  <a href="./README.ru-RU.md">Русский</a>
</p>

# Компонент Termux API Integration для Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![release version](https://img.shields.io/github/release/Vova-SH/termux-api/all.svg)](https://github.com/Vova-SH/termux-api/releases)
[![maintainer](https://img.shields.io/badge/maintainer-%40Vova--SH-green)](https://github.com/Vova-SH)

Компонент позволяет при запущенном Home Assistant на Android через [Termux](https://termux.dev) - вывести различные показатели через [Termux:API](https://wiki.termux.com/wiki/Termux:API).

## Минимальные требования для работы компонента

* Home Assistant запущен внутри Termux
* установлен пакет Termux:API (`pkg install termux-api`)

## Что поддержано в интеграции

**termux-battery-status**

* Health
* Percentage
* Plug
* Status
* Temperature


**termux-brightness**

* Изменение диапазона от 0 до 255
* Включение/выключение автояркости (Выбирается через включение/выключение источника света)


**termux-volume**

Изменение следующих уровней:

* alarm
* music
* notification
* ring
* system
* call


**termux-camera-info/termux-camera-photo**

* Получение фотографий с доступной передней/задней камеры смартфона
* Выключение/включение потока

Реализовано получение фото с обновлением раз в [10 секунд](https://github.com/Vova-SH/termux-api/blob/main/custom_components/termux_api/cam/entity.py#L38). При выключении фото заменяется на заглушку, при необходимости которую можно настроить заменить по пути [custom_components/termux_api/cam/placeholder.jpg](https://github.com/Vova-SH/termux-api/blob/main/custom_components/termux_api/cam/placeholder.jpg)

## Ссылки
* [Пример использования](https://habr.com/ru/companies/domclick/articles/675770/)
* [Частичное управление на основе базовых компонентов HA](https://github.com/Vova-SH/HomeAssistanceConfiguration/tree/main)
