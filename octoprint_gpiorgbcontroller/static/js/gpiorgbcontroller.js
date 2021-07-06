/*
 * View model for OctoPrint-GpioRgbController
 *
 * Author: Erik Gundersen
 * License: AGPLv3
 */
$(function() {
    function GpiorgbcontrollerViewModel(parameters) {
        var self = this;
        self.settings = parameters[0]
        self.color = ko.observable()
        self.isOn = ko.observable(false)

        self.updateColor = function(picker, event) {
            var newColor = event.currentTarget.jscolor.toHEXString()
            if(newColor) {
                self.color(newColor)
                OctoPrint.simpleApiCommand('gpiorgbcontroller', 'update_color', {'color': newColor})
            }
        }

        self.saveColor = function(picker, event) {
            var newColor = event.currentTarget.jscolor.toHEXString()
            if(newColor) {
                self.color(newColor)
                OctoPrint.simpleApiCommand('gpiorgbcontroller', 'update_color', {'color': newColor})
                OctoPrint.settings.savePluginSettings('gpiorgbcontroller', {'color': newColor})
            }
        }

        self.turnOn = function(){
            self.isOn(true)
            OctoPrint.simpleApiCommand('gpiorgbcontroller', 'turn_on')
            OctoPrint.settings.savePluginSettings('gpiorgbcontroller', {'is_on': true})
        }

        self.turnOff = function() {
            self.isOn(false)
            OctoPrint.simpleApiCommand('gpiorgbcontroller', 'turn_off')
            OctoPrint.settings.savePluginSettings('gpiorgbcontroller', {'is_on': false})
        }

        self.onBeforeBinding = function() {
            self.color(self.settings.settings.plugins.gpiorgbcontroller.color())
            self.isOn(self.settings.settings.plugins.gpiorgbcontroller.is_on()) 
            document.querySelector('#color-picker-control').jscolor.fromString(self.color())
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: GpiorgbcontrollerViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#sidebar_plugin_gpiorgbcontroller"]
    });
});
