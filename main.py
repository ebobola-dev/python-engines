from math import pi

from config import CONFIG
from models.engine_list import EngineList
from utils.json_rw import JsonUtil

engine_list = EngineList(source_filepath=CONFIG.ENGINE_LIST_FILEPATH)
scheme_8_data: dict | None = JsonUtil.read(filepath=CONFIG.SCHEME_DATA_FILEPATH)
CDP_data = scheme_8_data.get('CPD')
GR_data = scheme_8_data.get('GR')

print("\n------- Программа запущена только для 8 схемы -------\n")

d, f, v = map(float, input("Введите диаметр звёздочки, тяговое усиление на цепи и скорость: ").split())

p_rv = f * v
ge = CDP_data.get('couplings') * CDP_data.get('OCD') * CDP_data.get('CSG') * (CDP_data.get('bearing') ** 3)
cur_power = p_rv / ge
print(f'\nRequired power = {round(cur_power, 2)}')

w = (2 * v) / d
rec_ge = GR_data.get('CSG') * GR_data.get('OCD')
cur_freq = (30 * w * rec_ge) / pi
print(f'Required shift rotation freq: {round(cur_freq, 2)}\n')

required_engine = engine_list.find_required_engine(
    current_freq=cur_freq,
    current_power=cur_power,
)

print(f'Required engine: {required_engine}')




