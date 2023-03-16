from services.libraries import LibrariesService

if not LibrariesService.all_required_libraries_is_installed():
	exit()


from config.filepaths import FILEPATHS
from config.console import ConsoleColors
from services.args import ArgsService
from services.static_data import StaticData
from services.calculations import Calculations
from services.console import ConsoleService

def main():
	ConsoleService.initialize()
	ConsoleService.console.print("\n------- Программа запущена только для 10 схемы -------\n", style=ConsoleColors.WARNING)
	StaticData.initialize(
		scheme_data_filepath=FILEPATHS.SCHEME_DATA,
		engine_list_filepath=FILEPATHS.ENGINE_LIST,
		engine_constant_values_filepath=FILEPATHS.ENGINES_CONSTANT_VALUES,
		default_gear_ratios=FILEPATHS.DEFAULT_GEAR_RATIOS,
	)
	print()
	d, f, v = ArgsService.try_read()
	if d is not None:
		ConsoleService.console.print(f"Обнаружены значения из параметров запуска: {d} kH, {f} м/с, {v} м", style=ConsoleColors.SUCCESS)
	else:
		d, f, v = map(float, input("Введите диаметр звёздочки, тяговое усиление на цепи и скорость: ").split())
	print()
	calculations = Calculations(d, f, v)
	calculations.find_required_engine()
	calculations.kinematic_drive()

if __name__ == '__main__':
	main()



