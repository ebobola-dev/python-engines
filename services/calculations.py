from math import pi

from models.engine import Engine
from services.static_data import StaticData

class Calculations:
	def __init__(self, d: float, f: float, v: float):
		self._d = d
		self._f = f
		self._v = v

	#? Try to find the right engine by current [shaft rotation freq] and current [power]
	def find_required_engine(self):
		self._p_rv = self._f * self._v
		ge = StaticData.CDP_data.get('couplings') * StaticData.CDP_data.get('OCD') * StaticData.CDP_data.get('CSG') * (StaticData.CDP_data.get('bearing') ** 3)
		current_power = self._p_rv / ge
		print(f'\n[CALCULATIONS] Required power = {round(current_power, 2)}')

		self._w_rv = (2 * self._v) / self._d
		rec_ge = StaticData.GR_data.get('CSG') * StaticData.GR_data.get('OCD')
		current_freq = (30 * self._w_rv * rec_ge) / pi
		print(f'[CALCULATIONS] Required shaft rotation freq: {round(current_freq, 2)}\n')

		closest_constant_freq = min(
			shaft_freq for shaft_freq in StaticData.engine_list.get_constant_shaft_freqs() if (shaft_freq - current_freq >= 0)
		)

		closest_constant_power = min(
			power for power in StaticData.engine_list.get_constant_power_list() if (power - current_power >= 0)
		)

		self._required_engine = tuple(filter(
			lambda engine: engine.shaft_freq == closest_constant_freq and engine.power == closest_constant_power,
			StaticData.engine_list.get_engine_list(),
		))[0]

		print(f'[CALCULATIONS] Required engine: {self._required_engine}')


	def kinematic_drive(self):
		ang_vel_el_motor_shaft = (pi * self._required_engine.rotation_freq) / 30
		total_gear_ratio = ang_vel_el_motor_shaft / self._w_rv
		print(f'[CALCULATIONS] total_gear_ratio: {total_gear_ratio}')