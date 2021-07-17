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

A MOSFET must also be used to drive each LED channel since the PI is not capable of providing adequate current to the LED's.  It is a also a good idea to use a separate power supply to drive the LED strip since the PI power supply might not have adequate current to drive the PI + LED strip.  The following diagram is an example of how to interface to an LED strip.


![Wiring Diagram](/docs/imgs/wiring_diagram.png)