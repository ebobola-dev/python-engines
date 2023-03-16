from rich.theme import Theme
from rich.console import Console
from rich.table import Table, box

from models.engine import Engine
from config.console import ConsoleColors
from models.default_gear_ratios import DGR

class ConsoleService:
	console: Console | None = None

	@staticmethod
	def initialize():
		ConsoleService.console = Console(
			theme=Theme({
			'repr.number': ConsoleColors.DIGIT,
			'repr.repr.number_complex': ConsoleColors.DIGIT,
			}),
		)

	@staticmethod
	def print_engine(
			engine: Engine,
			table_name: str | None = None,
			table_title_style: str = None,
			title_style: str | None = None,
			power_style: str | None = None,
			rotation_freq_style: str | None = None,
			shaft_freq_style: str | None = None,
			delta_freq_style: str | None = None,
		):
		table = Table(title=table_name, title_style=table_title_style,)
		table.add_column("Название", justify='cetnter', style=title_style)
		table.add_column("Мощность\n(кВт)", justify='center', style=power_style)
		table.add_column("Частота вращения\n(об/мин)", justify='center', style=rotation_freq_style)
		table.add_column("Частота вращения вала\n(об/мин)", justify='center', style=shaft_freq_style)
		table.add_column("Tmax / Tmin", justify='center', style=delta_freq_style)

		table.add_row(
			engine.title,
			str(engine.power),
			str(engine.rotation_freq),
			str(engine.shaft_freq),
			str(engine.delta_t),
		)

		ConsoleService.console.print(table)

	@staticmethod
	def print_dgr(dgr: DGR):
		dgr_table = Table(title=dgr.ru_name, box=box.SQUARE)
		dgr_table.add_column("1-й ряд", justify='center')
		for dgr_1_row_value in dgr.row_1:
			dgr_table.add_column(str(dgr_1_row_value), justify='center')
		if dgr.row_2 is None:
			dgr_table.add_row("2-й ряд", *['-' for _ in dgr.row_1])
		else:
			dgr_table.add_row("2-й ряд", *map(lambda value: str(value), dgr.row_2))
		ConsoleService.console.print(dgr_table)