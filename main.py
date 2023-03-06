from math import pi

from models.engine_list import EngineList

xlsx_filename = 'engine_list.xlsx'

class Efficiency:
    couplings = 1.0 	#? м.
    OCD = 0.91 			#? о.п.ц.
    CSG = 0.97 			#? з.п.ц.
    bearing = 0.99  	#? п.п.

class GearRatio:
    CSG = 4.0
    OCD = 3.0

engine_list = EngineList(source_filename=xlsx_filename)

d = float(input('Диаметр звёздочки: '))
f = float(input('Тяговое усилие на цепи: '))
v = float(input('Скорость: '))

p_rv = f * v
ge = Efficiency.couplings * Efficiency.OCD * Efficiency.CSG * (Efficiency.bearing ** 3)
req_power = p_rv / ge
print(f'треб P = {round(req_power, 2)}')

w = (2 * v) / d
rec_ge = GearRatio.CSG * GearRatio.OCD
req_freq = (30 * w * rec_ge) / pi
print(f'треб частота: {round(req_freq, 2)}')

required_engine = engine_list.get_required_engine(
    req_freq=req_freq,
    req_power=req_power,
)
print(f'Required engine: {required_engine}')




