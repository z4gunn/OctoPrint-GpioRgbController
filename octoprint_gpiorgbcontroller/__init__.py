# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero import RGBLED, Button


class GpiorgbcontrollerPlugin(octoprint.plugin.StartupPlugin,
							  octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin,
							  octoprint.plugin.SimpleApiPlugin):

	def __init__(self):
		self.led = None
		self.color = '#FFFFFF'
		self.is_on = False
		self.btn = None
		self.is_btn_en = False
		self.gcode_command_enable = False
		self.gcode_index_enable = False
		self.gcode_rgb_index = 1
		self.pin_factory = RPiGPIOFactory()
	

	def init_rgb(self, red_pin, grn_pin, blu_pin):
		try:
			self.deinit_rgb()
			self.led = RGBLED(red=red_pin, green=grn_pin, blue=blu_pin, active_high=True, pin_factory=self.pin_factory)
			self._logger.info("LEDs initialized with pin factory: " + str(self.led.pin_factory))
		except:
			self._logger.error("Error occurred while initializing LEDs")


	def deinit_rgb(self):
		try:
			if(self.led is not None):
				self.led.close()
				self.led = None
				self._logger.info("LEDs deinitialized")
		except:
			self._logger.error("Error occurred while deinitializing LEDs")


	def init_btn(self, pin):
		try:
			self.deinit_btn()
			self.btn = Button(pin, pin_factory=self.pin_factory)
			self.btn.when_pressed = self.on_btn_press
			self.btn.when_released = self.on_btn_release
			self._logger.info("Button initialized with pin factory: " + str(self.btn.pin_factory) )
		except:
			self._logger.error("Error occurred while initializing button")


	def deinit_btn(self):
		try:
			if(self.btn is not None):
				self.btn.close()
				self.btn = None
				self._logger.info("Button deinitialized")
		except:
			self._logger.error("Error occurred while deinitializing button")


	def read_btn(self):
		if(self.btn is not None and self.is_btn_en):
			if(self.btn.is_pressed):
				self.on_btn_press()
			else:
				self.on_btn_release()


	def on_btn_press(self):
		if(self.is_btn_en):
			self.is_on = True
			self.update_rgb(self.color, self.is_on)


	def on_btn_release(self):
		if(self.is_btn_en):
			self.is_on = False
			self.update_rgb(self.color, self.is_on)
			

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
			self._logger.error("Error occurred while updating RGB state")


	def on_after_startup(self):
		red_pin = self._settings.get_int(["red_pin"])
		grn_pin = self._settings.get_int(["grn_pin"])
		blu_pin = self._settings.get_int(["blu_pin"])
		color = self._settings.get(["color"])
		is_on = self._settings.get_boolean(["is_on"])
		if red_pin is not None and grn_pin is not None and blu_pin is not None:
			self.init_rgb(red_pin, grn_pin, blu_pin)
			if(is_on is not None and color is not None):
				self.color = color
				self.is_on = is_on
				self.update_rgb(self.color, self.is_on)
		btn_pin = self._settings.get_int(["btn_pin"])
		is_btn_en = self._settings.get_boolean(["is_btn_en"])
		if btn_pin is not None and is_btn_en is not None:
			self.init_btn(btn_pin)
			self.is_btn_en = is_btn_en
			self.read_btn()
		gcode_command_enable = self._settings.get_boolean(["gcode_command_enable"])
		if gcode_command_enable is not None:
			self.gcode_command_enable = gcode_command_enable
		gcode_index_enable = self._settings.get_boolean(["gcode_index_enable"])
		if gcode_index_enable is not None:
			self.gcode_index_enable = gcode_index_enable
		gcode_rgb_index = self._settings.get_int(["gcode_rgb_index"])
		if gcode_rgb_index is not None:
			self.gcode_rgb_index = gcode_rgb_index
		self._plugin_manager.send_plugin_message(self._identifier, dict(is_on=self.is_on, color=self.color))
		

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		if 'red_pin' in data or 'grn_pin' in data or 'blu_pin' in data:
			red_pin = self._settings.get_int(["red_pin"])
			grn_pin = self._settings.get_int(["grn_pin"])
			blu_pin = self._settings.get_int(["blu_pin"])
			if(red_pin is not None and grn_pin is not None and blu_pin is not None):
				self.init_rgb(red_pin, grn_pin, blu_pin)
		color = self._settings.get(["color"])
		is_on = self._settings.get_boolean(["is_on"])
		if is_on is not None and color is not None:
			self.color = color
			self.is_on = is_on
			self.update_rgb(self.color, self.is_on)
		if 'btn_pin' in data or 'is_btn_en' in data:
			btn_pin = self._settings.get_int(["btn_pin"])
			is_btn_en = self._settings.get_boolean(["is_btn_en"])
			if(btn_pin is not None and is_btn_en is not None):
				self.init_btn(btn_pin)
				self.is_btn_en = is_btn_en
				self.read_btn()
		gcode_command_enable = self._settings.get_boolean(["gcode_command_enable"])
		if gcode_command_enable is not None:
			self.gcode_command_enable = gcode_command_enable
		gcode_index_enable = self._settings.get_boolean(["gcode_index_enable"])
		if gcode_index_enable is not None:
			self.gcode_index_enable = gcode_index_enable
		gcode_rgb_index = self._settings.get_int(["gcode_rgb_index"])
		if gcode_rgb_index is not None:
			self.gcode_rgb_index = gcode_rgb_index
		
	def get_settings_defaults(self):
		return dict(
			red_pin=20,
			grn_pin=25,
			blu_pin=5,
			color='#FFFFFF',
			is_on = False,
			btn_pin=21,
			is_btn_en=False,
			gcode_command_enable=False,
			gcode_index_enable=False,
			gcode_rgb_index=1,
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
		

	def gcode_parse_index(self, cmd):
		params = cmd.split("I")
		if len(params) != 2:
			return None
		else:
			try:
				index = int(params[1].split()[0])
				if index > 0:
					return index
				else:
					return None
			except:
				return None


	def gcode_parse_rgb_component(self, cmd, comp):
		try:
			comp_type = comp.upper()
			if comp_type != "R" and comp_type != "G" and comp_type != "B":
				return None
			delim = ""
			if comp_type == "R":
				delim = "R"
			elif comp_type == "G":
				delim = "U"
			elif comp_type == "B":
				delim = "B"
			params = cmd.split(delim)
			if len(params) != 2:
				return None
			else:
				color_int = int(params[1].split()[0])
				if color_int < 0 or color_int > 255:
					return None
				else:
					color_hex = "%02X" % color_int
					if len(color_hex) != 2:
						return None
					else:
						return color_hex
		except:
			return None


	def replace_color_component(self, color, value, comp):
		if len(color) != 7 or value is None:
			return color
		comp_type = comp.upper()
		if comp_type != "R" and comp_type != "G" and comp_type != "B":
			return color
		if len(value) != 2:
			return color
		old_r = color[1:3]
		old_g = color[3:5]
		old_b = color[5:7]
		new_color = color
		if comp_type == "R":
			new_color = "#" + value + old_g + old_b
		elif comp_type == "G":
			new_color = "#" + old_r + value + old_b
		elif comp_type == "B":
			new_color = "#" +old_r + old_g + value
		return new_color


	def on_gcode_command(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if not self.gcode_command_enable:
			return 
		if gcode and gcode.startswith("M150"):
			color = "#000000"
			red = self.gcode_parse_rgb_component(cmd, "R")
			color = self.replace_color_component(color, red, "R")
			grn = self.gcode_parse_rgb_component(cmd, "G")
			color = self.replace_color_component(color, grn, "G")
			blu = self.gcode_parse_rgb_component(cmd, "B")
			color = self.replace_color_component(color, blu, "B")
			if self.gcode_index_enable:
				index = self.gcode_parse_index(cmd)
				if index is not None and index == self.gcode_rgb_index and color is not None and len(color) == 7:
					self.color = color
					self.is_on = True
					self.update_rgb(self.color, self.is_on)
					self._plugin_manager.send_plugin_message(self._identifier, dict(is_on=self.is_on, color=self.color))
			else:
				if color is not None and len(color) == 7:
					self.color = color
					self.is_on = True
					self.update_rgb(self.color, self.is_on)
					self._plugin_manager.send_plugin_message(self._identifier, dict(is_on=self.is_on, color=self.color))
		

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
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.sent": __plugin_implementation__.on_gcode_command,
	}

