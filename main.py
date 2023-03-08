from math import pi

from config import FILEPATHS
from services.static_data import StaticData
from services.calculations import Calculations


def main():
	StaticData.initialize(
		scheme_data_filepath=FILEPATHS.SCHEME_DATA,
		engine_list_filepath=FILEPATHS.ENGINE_LIST,
		engine_constant_values_filepath=FILEPATHS.ENGINES_CONSTANT_VALUES,
	)
	d, f, v = map(float, input("Введите диаметр звёздочки, тяговое усиление на цепи и скорость: ").split())
	calculations = Calculations(d, f, v)
	calculations.find_required_engine()
	calculations.kinematic_drive()

if __name__ == '__main__':
	print("\n------- Программа запущена только для 10 схемы -------\n")
	main()



