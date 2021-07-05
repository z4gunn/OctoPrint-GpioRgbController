# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from gpiozero import RGBLED

class GpiorgbcontrollerPlugin(octoprint.plugin.StartupPlugin,
							  octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin,
							  octoprint.plugin.SimpleApiPlugin):

	def __init__(self):
		self.led = None
		self.color = '#FFFFFF'
		self.is_on = False
	

	def init_rgb(self, red_pin, grn_pin, blu_pin):
		try:
			self.deinit_rgb()
			self.led = RGBLED(red=red_pin, green=grn_pin, blue=blu_pin, active_high=True)
			self._logger.info("RGB initialized")
		except:
			self._logger.error("Error occured while initializing RGB")

	def deinit_rgb(self):
		try:
			if(self.led is not None):
				self.led.close()
				self.led = None
				self._logger.info("RGB deinitialized")
		except:
			self._logger.error("Error occured while deinitializing RGB")


	def update_rgb(self, color, is_on):
		if(self.led is not None):
			rgb = int(color[1:], 16)
			red = ((rgb & 0xFF0000) >> 16) / 255
			grn = ((rgb & 0x00FF00) >> 8) / 255
			blu = ((rgb & 0x0000FF)) / 255
			if is_on:
				self.led.color = (red, grn, blu)
			else:
				self.led.color = (0, 0, 0)
		else:
			self._logger.error("Error occured while updating RGB state")


	def on_after_startup(self):
		red_pin = self._settings.get_int(["red_pin"])
		grn_pin = self._settings.get_int(["grn_pin"])
		blu_pin = self._settings.get_int(["blu_pin"])
		color = self._settings.get(["color"])
		is_on = self._settings.get_boolean(["is_on"])
		if(red_pin is not None and grn_pin is not None and blu_pin is not None):
			self.init_rgb(red_pin, grn_pin, blu_pin)
			if(is_on is not None and color is not None):
				self.color = color
				self.is_on = is_on
				self.update_rgb(self.color, self.is_on)


	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		if ('red_pin' in data or 'grn_pin' in data or 'blu_pin' in data):
			red_pin = self._settings.get_int(["red_pin"])
			grn_pin = self._settings.get_int(["grn_pin"])
			blu_pin = self._settings.get_int(["blu_pin"])
			if(red_pin is not None and grn_pin is not None and blu_pin is not None):
				self.init_rgb(red_pin, grn_pin, blu_pin)
		color = self._settings.get(["color"])
		is_on = self._settings.get_boolean(["is_on"])
		if(is_on is not None and color is not None):
			self.color = color
			self.is_on = is_on
			self.update_rgb(self.color, self.is_on)
		
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
			js=["js/gpiorgbcontroller.js",  "js/jscolor.min.js"],
			css=["css/gpiorgbcontroller.css"],
			less=["less/gpiorgbcontroller.less"]
		)


	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]


	def get_api_commands(self):
		return dict(
			update_color=["color"],
			turn_on=[],
			turn_off=[]
		)


	def on_api_command(self, command, data):
		if command == "update_color":
			color = data.get('color', None)
			if color != None:
				self.color = color
		elif command == "turn_on":
			self.is_on = True
		elif command == "turn_off":
			self.is_on = False
		self.update_rgb(self.color, self.is_on)


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


__plugin_name__ = "GPIO RGB Controller"

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

