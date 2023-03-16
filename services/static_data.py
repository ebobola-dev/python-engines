from enum import Enum
from time import sleep
from rich.progress import *
from rich.table import Table
from traceback import format_exc

from config.console import ConsoleColors, ProgressSleepTimes
from utils.json_rw import JsonUtil
from models.engine_list import EngineList
from models.scheme_data import Scheme
from models.default_gear_ratios import DefaultGearRatios

from services.console import ConsoleService


class InitializationStatus(Enum):
	NotInitialized = 1
	InitializedWithMinorProblem = 2
	InitializedWithCriticalProblem = 3
	SuccessfullyInitialized = 4

class StaticData:
	initialization_status: InitializationStatus = InitializationStatus.NotInitialized
	engine_list: EngineList | None = None
	schemes: tuple[Scheme] | None = None
	DGRS: DefaultGearRatios | None = None

	@staticmethod
	def initialize(
			scheme_data_filepath: str,
			engine_list_filepath: str,
			engine_constant_values_filepath: str,
			default_gear_ratios_filepath: str,
		):
		ConsoleService.console.print(" ---------------- Инициализация ---------------- ", style=ConsoleColors.MAIN)
		with Progress(
			TextColumn("[blue]{task.percentage:>3.0f}%"),
			BarColumn(),
			TextColumn("[blue]{task.description}"),
			refresh_per_second=60,
			console=ConsoleService.console,
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
				f"Чтение таблиц ({default_gear_ratios_filepath})",
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
				ConsoleService.console.print(f'Произошла ошибка при чтении двигателей из файла: {engine_init_error}', style=ConsoleColors.ERROR)
				StaticData.initialization_status = InitializationStatus.InitializedWithCriticalProblem
				return
			for _ in range(50):
				progress.update(read_engines_task, advance=1)
				sleep(ProgressSleepTimes.ENGINE)
			ConsoleService.console.print(f'Успешно прочитано {StaticData.engine_list.get_engine_list_len()} двигатель(ей)', style=ConsoleColors.SUCCESS)

			#* -------------------------------------------------------
			#? Чтение данных схем
			for _ in range(50):
				progress.update(read_scheme_data_task, advance=1)
				sleep(ProgressSleepTimes.SCHEME)
			try:
				schemes_json_list: tuple[dict] | None = tuple(JsonUtil.read(filepath=scheme_data_filepath))
				StaticData.schemes = tuple(
					Scheme.from_json(scheme_data_json) for scheme_data_json in schemes_json_list
				)
			except Exception as scheme_init_error:
				ConsoleService.console.print(f'Произошла ошибка при чтении данных схем из файла: {scheme_init_error}', style=ConsoleColors.ERROR)
				StaticData.initialization_status = InitializationStatus.InitializedWithCriticalProblem
				return
			for _ in range(50):
				progress.update(read_scheme_data_task, advance=1)
				sleep(ProgressSleepTimes.SCHEME)
			ConsoleService.console.print(f'Успешно прочитаны данные {len(StaticData.schemes)} схем(ы)', style=ConsoleColors.SUCCESS)

			scheme_table = Table(title="Данных схем")
			scheme_table.add_column('№ cхемы', justify='center')
			scheme_table.add_column('η з.п', justify='center')
			scheme_table.add_column('η о.п', justify='center')
			scheme_table.add_column('η м.п', justify='center')
			scheme_table.add_column('η п.п', justify='center')
			scheme_table.add_column('u з.п', justify='center')
			scheme_table.add_column('u о.п', justify='center')

			for scheme in StaticData.schemes:
				scheme_table.add_row(
					str(scheme.number),
					str(scheme.CPD.CSG),
					str(scheme.CPD.OCD),
					str(scheme.CPD.bearing),
					str(scheme.CPD.couplings),
					str(scheme.GR.CSG),
					str(scheme.GR.OCD),
				)
			ConsoleService.console.print(scheme_table)

			#* -------------------------------------------------------
			#? Чтение стандартных передаточных чисел
			for _ in range(50):
				progress.update(read_dgr_task, advance=1)
				sleep(0.01)
			try:
				StaticData.DGRS = DefaultGearRatios.from_json(JsonUtil.read(filepath=default_gear_ratios_filepath))
			except Exception as dgr_init_error:
				ConsoleService.console.print(f'Произошла ошибка при чтении стандартных передаточных чисел: {dgr_init_error}', style=ConsoleColors.ERROR)
				StaticData.initialization_status = InitializationStatus.InitializedWithCriticalProblem
				return
			for _ in range(50):
				progress.update(read_dgr_task, advance=1)
				sleep(ProgressSleepTimes.DGR)
			ConsoleService.console.print(f'Стандартные передаточные числа успешно прочитаны:', style=ConsoleColors.SUCCESS)

			ConsoleService.print_dgr(StaticData.DGRS.cylindrical)
			ConsoleService.print_dgr(StaticData.DGRS.conical)
			ConsoleService.print_dgr(StaticData.DGRS.worm)

			#* -------------------------------------------------------

			ConsoleService.console.print(" ----------- Инициализация завершена ----------- ", style=ConsoleColors.MAIN)

