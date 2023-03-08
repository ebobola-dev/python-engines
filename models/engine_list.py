from models.engine import Engine
from utils.json_rw import JsonUtil

class EngineList:
	def __init__(self, engines_source_filepath: str, constant_values_filepath: str):
		json_engine_list: dict = JsonUtil.read(engines_source_filepath)
		constant_values: dict = JsonUtil.read(constant_values_filepath)
		self._engine_list = tuple(map(
			lambda json_engine: Engine(**json_engine),
			json_engine_list,
		))
		self._constant_shaft_freqs = tuple(constant_values.get('shaft_freqs'))
		self._constant_power_list = tuple(constant_values.get('powers'))


	#* ------------- GETTERS -------------
	def get_constant_shaft_freqs(self):
		return self._constant_shaft_freqs

	def get_constant_power_list(self):
		return self._constant_power_list

	def get_engine_list(self):
		return self._engine_list[:]
	#* -----------------------------------