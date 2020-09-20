# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from gpiozero import RGBLED

class GpiorgbcontrollerPlugin(octoprint.plugin.StartupPlugin,
							  octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin):

	def __init__(self):
		self.led = None
	

	def init_leds(self, red_pin, grn_pin, blu_pin):
		try:
			self.led = RGBLED(red=red_pin, green=grn_pin, blue=blu_pin, active_high=True)
			self._logger.info("LEDS Initialized")
		except:
			self._logger.error("Error occured while initializing LED's")


	def on_after_startup(self):
		red_pin = self._settings.get_int(["red_pin"])
		grn_pin = self._settings.get_int(["grn_pin"])
		blu_pin = self._settings.get_int(["blu_pin"])
		color = self._settings.get(["color"])
		is_on = self._settings.get_boolean(["is_on"])
		self._logger.info("RED Pin: %s" % red_pin)
		self._logger.info("GRN Pin: %s" % grn_pin)
		self._logger.info("BLU Pin: %s" % blu_pin)
		self._logger.info("Color:   %s" % color)
		self._logger.info("Is On:  %s" % is_on)
		if(red_pin is not None and grn_pin is not None and blu_pin is not None):
			self.init_leds(red_pin, grn_pin, blu_pin)


	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		color_hex = self._settings.get(["color"])
		rgb = int(color_hex[1:], 16)
		is_on = self._settings.get_boolean(["is_on"])
		self._logger.info("Settings Saved")
		self._logger.info("Color : " + color_hex)
		self._logger.info("Is On: " + str(is_on))
		self.update_pins(rgb, is_on, is_wht_on)


	def update_pins(self, rgb, is_on):
		red = ((rgb & 0xFF0000) >> 16) / 255
		grn = ((rgb & 0x00FF00) >> 8) / 255
		blu = ((rgb & 0x0000FF)) / 255
		if is_on:
			self.led.color = (red, grn, blu)
		else:
			self.led.color = (0, 0, 0)


	def get_settings_defaults(self):
		return dict(
			red_pin=20,
			grn_pin=25,
			blu_pin=5,
			color='#FFFFFF',
			is_on = False,
		)


	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/gpiorgbcontroller.js"],
			css=["css/gpiorgbcontroller.css"],
			less=["less/gpiorgbcontroller.less"]
		)


	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]


	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			gpiorgbcontroller=dict(
				displayName="Gpiorgbcontroller Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="z4gunn",
				repo="OctoPrint-GpioRgbController",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/z4gunn/OctoPrint-GpioRgbController/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "GPIO RGB Controller"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = GpiorgbcontrollerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

