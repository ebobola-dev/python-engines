from math import pi
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

from models.engine import Engine
from services.static_data import StaticData
from config.console import ConsoleColors

console = Console(theme=Theme({
	'repr.number': 'yellow',
	'repr.repr.number_complex': 'yellow',
}))

class Calculations:
	def __init__(self, d: float, f: float, v: float):
		self._d = d
		self._f = f
		self._v = v

	#? Подбираем электродвигатель
	def find_required_engine(self):
		self._p_rv = self._f * self._v
		ge = StaticData.CDP.get('couplings') * StaticData.CDP.get('OCD') * StaticData.CDP.get('CSG') * (StaticData.CDP.get('bearing') ** 3)
		self._current_power = self._p_rv / ge
		console.print(f'Мощность = {round(self._current_power, 2)}', style=ConsoleColors.MAIN)

		self._w_rv = (2 * self._v) / self._d
		rec_ge = StaticData.GR.get('CSG') * StaticData.GR.get('OCD')
		self._current_freq = (30 * self._w_rv * rec_ge) / pi
		console.print(f'Частота вращения вала = {round(self._current_freq, 2)}', style=ConsoleColors.MAIN)

		closest_constant_freq = min(
			shaft_freq for shaft_freq in StaticData.engine_list.get_constant_shaft_freqs() if (shaft_freq - self._current_freq >= 0)
		)

		closest_constant_power = min(
			power for power in StaticData.engine_list.get_constant_power_list() if (power - self._current_power >= 0)
		)

		self._required_engine: Engine = tuple(filter(
			lambda engine: engine.shaft_freq == closest_constant_freq and engine.power == closest_constant_power,
			StaticData.engine_list.get_engine_list(),
		))[0]

		require_engine_table = Table(title='Необходимый двигатель')
		require_engine_table.add_column("Название", justify='center')
		require_engine_table.add_column("Мощность", style=ConsoleColors.SUCCESS, justify='center')
		require_engine_table.add_column("Частота вращения", justify='center')
		require_engine_table.add_column("Частота вращения вала", style=ConsoleColors.SUCCESS, justify='center')
		require_engine_table.add_column("Tmax / Tmin", justify='center')

		require_engine_table.add_row(
			self._required_engine.title,
			str(self._required_engine.power),
			str(self._required_engine.rotation_freq),
			str(self._required_engine.shaft_freq),
			str(self._required_engine.delta_t),
		)

		console.print(require_engine_table)


	def kinematic_drive(self):
		engine_rotation_freq = self._required_engine.rotation_freq
		w_em = (pi * engine_rotation_freq) / 30
		total_gear_ratio = w_em / self._w_rv
		console.print(f'\nОбщее передаточное число = {round(total_gear_ratio, 2)}', style=ConsoleColors.MAIN)
		closed_gear_ratio = total_gear_ratio / StaticData.GR.get('OCD')
		console.print(f'Какое-то закрытое передаточное число = {round(closed_gear_ratio, 2)}', style=ConsoleColors.MAIN)
		required_dgr: float | None = None
		biggest_default_dgrs_1_row = tuple(filter(lambda dgr: closed_gear_ratio <= dgr, StaticData.DGR.SSC_1_ROW))
		if len(biggest_default_dgrs_1_row) > 0:
			required_dgr = biggest_default_dgrs_1_row[0]
		else:
			required_dgr = tuple(filter(lambda dgr: closed_gear_ratio <= dgr, StaticData.DGR.SSC_2_ROW))[0]
		gear_ratio_OCD = total_gear_ratio / required_dgr
		console.print(f'Открытое чего-то там передаточное число = {round(gear_ratio_OCD, 2)}', style=ConsoleColors.MAIN)
		#* ------------------------------------------------------------------------
		w1 = w_em
		w2 = w1
		w3 = w2 / required_dgr
		w4 = w3 / gear_ratio_OCD
		#* ------------------------------------------------------------------------
		n1 = engine_rotation_freq
		n2 = n1
		n3 = (30 * w3) / pi
		n4 = (30 * w4) / pi
		#* ------------------------------------------------------------------------
		p1 = self._current_power
		p2 = p1 * StaticData.CDP.get("couplings") * StaticData.CDP.get('bearing')
		p3 = p2 * StaticData.CDP.get('bearing') * StaticData.CDP.get('CSG')
		p4 = p3 * StaticData.CDP.get('OCD') * StaticData.CDP.get('bearing')
		#* ------------------------------------------------------------------------
		t1 = p1 / w1
		t2 = p2 / w2
		t3 = p3 / w3
		t4 = p4 / w4
		#* ------------------------------------------------------------------------
		print()
		table = Table(title="Результаты кинематического расчёта привода")
		table.add_column("Валы привода", justify='center')
		table.add_column("w, рад/с", justify='center')
		table.add_column("n, об/мин", justify='center')
		table.add_column("P, кВт", justify='center')
		table.add_column("T, kH * м", justify='center')
		table.add_column("Передаточные числа", justify='center', style=ConsoleColors.MAIN, header_style=ConsoleColors.MAIN)
		table.add_row("1", str(round(w1, 2)), str(round(n1, 2)), str(round(p1, 2)), str(round(t1, 2)), f"u* о.п = {round(gear_ratio_OCD, 2)}")
		table.add_row("2", str(round(w2, 2)), str(round(n2, 2)), str(round(p2, 2)), str(round(t2, 2)))
		table.add_row("3", str(round(w3, 2)), str(round(n3, 2)), str(round(p3, 2)), str(round(t3, 2)), f"u* з.п = {round(required_dgr, 2)}")
		table.add_row("4 (раб.вал)", str(round(w4, 2)), str(round(n4, 2)), str(round(p4, 2)), str(round(t4, 2)))
		console.print(table)