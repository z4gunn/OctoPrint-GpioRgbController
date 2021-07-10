# OctoPrint-GpioRgbController

This is a plugin to control an external RGB LED strip via Raspberry Pi GPIO pins.  This plugin allows you to set the pin numbers in the settings and control the LED color and on/off state via sidebar control.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/z4gunn/OctoPrint-GpioRgbController/archive/master.zip


## LED Strip Compatibility

This plugin is only intended to drive discrete or strip RGB LED's via independent GPIO control.  This plugin will not work with LED strips that have coontrols or digital interface such as SPI.  A MOSFET must also be used for each LED channel since the PI is not capable of driving adequate current into the LED's.  This is a great [tutorial](https://learn.adafruit.com/rgb-led-strips) that explains on how to connect an analog RGB LED strip to an Arduino, however the same concepts apply to connecting to a PI.