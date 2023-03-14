from time import sleep
from enum import Enum

from config.console import ConsoleColors, ProgressSleepTimes
from utils.json_rw import JsonUtil
from models.engine_list import EngineList
from rich.console import Console
from rich.progress import *
from rich.table import Table, box

console = Console()

class InitializationStatus(Enum):
	NotInitialized = 1
	InitializedWithMinorProblem = 2
	InitializedWithCriticalProblem = 3
	SuccessfullyInitialized = 4

class DefaultGearRatios:
	def __init__(
		self,
		json_view: dict,
	):
		self.SSC_1_ROW: tuple = tuple(json_view.get('ssc'))[0]
		self.SSC_2_ROW: tuple = tuple(json_view.get('ssc'))[1]

class StaticData:
	initialization_status: InitializationStatus = InitializationStatus.NotInitialized
	engine_list: EngineList | None = None
	CDP: dict | None = None
	GR: dict | None = None
	DGR: DefaultGearRatios | None = None

	@staticmethod
	def initialize(
			scheme_data_filepath: str,
			engine_list_filepath: str,
			engine_constant_values_filepath: str,
			default_gear_ratios: str,
		):
		console.print(" ---------------- Инициализация ---------------- ", style=ConsoleColors.MAIN)
		with Progress(
			TextColumn("[blue]{task.percentage:>3.0f}%"),
			BarColumn(),
			TextColumn("[blue]{task.description}"),
			refresh_per_second=60,
			console=console,
			transient=True,
		) as progress:
			read_engines_task = progress.add_task(
				f"Чтение двигателей ({engine_list_filepath}, {engine_constant_values_filepath})",
				total=100,
			)
			read_scheme_data_task = progress.add_task(
				f"Чтение данных схем ({scheme_data_filepath})",
				total=100,
			)
			read_dgr_task = progress.add_task(
				f"Чтение таблиц ({default_gear_ratios})",
				total=100,
			)

			#* -------------------------------------------------------
			#? Чтение списка двигателей и константых данных двигателей
			for _ in range(50):
				progress.update(read_engines_task, advance=1)
				sleep(ProgressSleepTimes.ENGINE)
			try:
				StaticData.engine_list = EngineList(
					engines_source_filepath=engine_list_filepath,
					constant_values_filepath=engine_constant_values_filepath,
				)
			except Exception as engine_init_error:
				console.print(f'Произошла ошибка при чтении двигателей из файла: {engine_init_error}', style=ConsoleColors.ERROR)
				StaticData.initialization_status = InitializationStatus.InitializedWithCriticalProblem
				return
			for _ in range(50):
				progress.update(read_engines_task, advance=1)
				sleep(ProgressSleepTimes.ENGINE)
			console.print(f'Успешно прочитано {StaticData.engine_list.get_engine_list_len()} двигателей', style=ConsoleColors.SUCCESS)

			#* -------------------------------------------------------
			#? Чтение данных схем
			for _ in range(50):
				progress.update(read_scheme_data_task, advance=1)
				sleep(ProgressSleepTimes.SCHEME)
			try:
				scheme_10_data: dict | None = JsonUtil.read(filepath=scheme_data_filepath)
				StaticData.CDP: dict = scheme_10_data.get('CPD')
				StaticData.GR: dict = scheme_10_data.get('GR')
			except Exception as scheme_init_error:
				console.print(f'Произошла ошибка при чтении данных схем из файла: {scheme_init_error}', style=ConsoleColors.ERROR)
				StaticData.initialization_status = InitializationStatus.InitializedWithCriticalProblem
				return
			for _ in range(50):
				progress.update(read_scheme_data_task, advance=1)
				sleep(ProgressSleepTimes.SCHEME)
			console.print(f'Данные схем успешно прочитаны', style=ConsoleColors.SUCCESS)

			scheme_table = Table(title="Данных схем")
			scheme_table.add_column('№ cхемы', justify='center')
			scheme_table.add_column('η з.п', justify='center')
			scheme_table.add_column('η о.п', justify='center')
			scheme_table.add_column('η м.п', justify='center')
			scheme_table.add_column('η п.п', justify='center')
			scheme_table.add_column('u з.п', justify='center')
			scheme_table.add_column('u о.п', justify='center')
			scheme_table.add_row(
				"10",
				str(StaticData.CDP.get('CSG')),
				str(StaticData.CDP.get('OCD')),
				str(StaticData.CDP.get('bearing')),
				str(StaticData.CDP.get('couplings')),
				str(StaticData.GR.get('CSG')),
				str(StaticData.GR.get('OCD')),
			)
			console.print(scheme_table)

			#* -------------------------------------------------------
			#? Чтение стандартных передаточных чисел
			for _ in range(50):
				progress.update(read_dgr_task, advance=1)
				sleep(0.01)
			try:
				StaticData.DGR = DefaultGearRatios(json_view=JsonUtil.read(filepath=default_gear_ratios))
			except Exception as dgr_init_error:
				console.print(f'Произошла ошибка при чтении данных схем из файла: {dgr_init_error}', style=ConsoleColors.ERROR)
				StaticData.initialization_status = InitializationStatus.InitializedWithCriticalProblem
				return
			for _ in range(50):
				progress.update(read_dgr_task, advance=1)
				sleep(ProgressSleepTimes.DGR)
			console.print(f'Стандартные передаточные числа успешно прочитаны:', style=ConsoleColors.SUCCESS)

			dgr_table_1 = Table(title="Одноступенчатый цилиндрический", box=box.SQUARE)
			dgr_table_1.add_column("1-й ряд", justify='center')
			for dgr_1_row_value in StaticData.DGR.SSC_1_ROW:
				dgr_table_1.add_column(str(dgr_1_row_value), justify='center')
			dgr_table_1.add_row("2-й ряд", *map(lambda value: str(value), StaticData.DGR.SSC_2_ROW))
			console.print(dgr_table_1)

			#* -------------------------------------------------------

			console.print(" ----------- Инициализация завершена ----------- ", style=ConsoleColors.MAIN)

