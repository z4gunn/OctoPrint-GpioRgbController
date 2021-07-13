# OctoPrint-GpioRgbController

This is a lightweight plugin dedicated to the control of an external RGB LED strip via Raspberry Pi GPIO pins.  This plugin has the following features:

* Convenient sidebar control
* Adjustable RGB color picker
* Pin selection via settings
* Optional on/off trigger via input pin
* M150 GCODE support
* Independent GCODE control using optional RGB index


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/z4gunn/OctoPrint-GpioRgbController/archive/master.zip


## IMPORTANT - LED Strip Compatibility

This plugin is only intended to drive discrete or strip RGB LED's via independent GPIO control.  This plugin will not work with LED strips that have coontrolers or digital interface such as SPI.  

A MOSFET must also be used to drive each LED channel since the PI is not capable of providing adequate current to the LED's.  This is a great [tutorial](https://learn.adafruit.com/rgb-led-strips) that explains on how to connect an analog RGB LED strip to an Arduino, however the same concept applies to interfacing to a PI.