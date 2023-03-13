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
		ge = StaticData.CDP.get('couplings') * StaticData.CDP.get('OCD') * StaticData.CDP.get('CSG') * (StaticData.CDP.get('bearing') ** 3)
		self._current_power = self._p_rv / ge
		print(f'\n[CALCULATIONS] Required power = {round(self._current_power, 2)}')

		self._w_rv = (2 * self._v) / self._d
		rec_ge = StaticData.GR.get('CSG') * StaticData.GR.get('OCD')
		self._current_freq = (30 * self._w_rv * rec_ge) / pi
		print(f'[CALCULATIONS] Required shaft rotation freq: {round(self._current_freq, 2)}\n')

		closest_constant_freq = min(
			shaft_freq for shaft_freq in StaticData.engine_list.get_constant_shaft_freqs() if (shaft_freq - self._current_freq >= 0)
		)

		closest_constant_power = min(
			power for power in StaticData.engine_list.get_constant_power_list() if (power - self._current_power >= 0)
		)

		self._required_engine = tuple(filter(
			lambda engine: engine.shaft_freq == closest_constant_freq and engine.power == closest_constant_power,
			StaticData.engine_list.get_engine_list(),
		))[0]

		print(f'[CALCULATIONS] Required engine: {self._required_engine}')


	def kinematic_drive(self):
		engine_rotation_freq = self._required_engine.rotation_freq
		w_em = (pi * engine_rotation_freq) / 30
		total_gear_ratio = w_em / self._w_rv
		print(f'[CALCULATIONS] total gear ratio: {round(total_gear_ratio, 2)}')
		closed_gear_ratio = total_gear_ratio / StaticData.GR.get('OCD')
		print(f'[CALCULATIONS] closed gear ratio: {round(closed_gear_ratio, 2)}')
		required_dgr: float | None = None
		biggest_default_dgrs_1_row = tuple(filter(lambda dgr: closed_gear_ratio <= dgr, StaticData.DGR.SSC_1_ROW))
		if len(biggest_default_dgrs_1_row) > 0:
			required_dgr = biggest_default_dgrs_1_row[0]
		else:
			required_dgr = tuple(filter(lambda dgr: closed_gear_ratio <= dgr, StaticData.DGR.SSC_2_ROW))[0]
		gear_ratio_OCD = total_gear_ratio / required_dgr
		print(f'[CALCULATIONS] gear ratio OCD: {round(gear_ratio_OCD, 2)}')
		w1 = w_em
		w2 = w1
		w3 = w2 / required_dgr
		w4 = w3 / gear_ratio_OCD
		print(f"[CALCULATIONS]:\n\tw1 = {round(w1, 2)}\t|\tw2 = {round(w2, 2)}")
		print(f"\tw3 = {round(w3, 2)}\t|\tw4 = {round(w4, 2)}")
		n1 = engine_rotation_freq
		n2 = n1
		n3 = (30 * w3) / pi
		n4 = (30 * w4) / pi
		print(f"\n\tn1 = {round(n1, 2)}\t|\tn2 = {round(n2, 2)}")
		print(f"\tn3 = {round(n3, 2)}\t|\tn4 = {round(n4, 2)}")
		p1 = self._current_power
		p2 = p1 * StaticData.CDP.get("couplings") * StaticData.CDP.get('bearing')
		p3 = p2 * StaticData.CDP.get('bearing') * StaticData.CDP.get('CSG')
		p4 = p3 * StaticData.CDP.get('OCD') * StaticData.CDP.get('bearing')
		print(f"\n\tp1 = {round(p1, 2)}\t|\tp2 = {round(p2, 2)}")
		print(f"\tp3 = {round(p3, 2)}\t|\tp4 = {round(p4, 2)}")
		t1 = p1 / w1
		t2 = p2 / w2
		t3 = p3 / w3
		t4 = p4 / w4
		print(f"\n\tt1 = {round(t1, 2)}\t|\tt2 = {round(t2, 2)}")
		print(f"\tt3 = {round(t3, 2)}\t|\tt4 = {round(t4, 2)}")