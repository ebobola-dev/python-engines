from services.libraries import LibrariesService

if not LibrariesService.all_required_libraries_is_installed():
	exit()

from rich.console import Console
from rich.theme import Theme

from config.filepaths import FILEPATHS
from config.console import ConsoleColors
from services.static_data import StaticData
from services.calculations import Calculations


console = Console(theme=Theme({
	'repr.number': 'yellow',
	'repr.repr.number_complex': 'yellow',
}))

def main():
	console.print("\n------- Программа запущена только для 10 схемы -------\n", style=ConsoleColors.WARNING)
	StaticData.initialize(
		scheme_data_filepath=FILEPATHS.SCHEME_DATA,
		engine_list_filepath=FILEPATHS.ENGINE_LIST,
		engine_constant_values_filepath=FILEPATHS.ENGINES_CONSTANT_VALUES,
		default_gear_ratios=FILEPATHS.DEFAULT_GEAR_RATIOS,
	)
	print()
	d, f, v = map(float, input("Введите диаметр звёздочки, тяговое усиление на цепи и скорость: ").split())
	print()
	calculations = Calculations(d, f, v)
	calculations.find_required_engine()
	calculations.kinematic_drive()

if __name__ == '__main__':
	main()



