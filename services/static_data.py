from utils.json_rw import JsonUtil
from models.engine import Engine
from models.engine_list import EngineList

class StaticData:
	engine_list: EngineList | None = None
	CDP_data: dict | None = None
	GR_data: dict | None = None

	@staticmethod
	def initialize(
			scheme_data_filepath: str,
			engine_list_filepath: str,
			engine_constant_values_filepath: str,
		):
		StaticData.engine_list = EngineList(
		engines_source_filepath=engine_list_filepath,
		constant_values_filepath=engine_constant_values_filepath,
		)
		scheme_10_data: dict | None = JsonUtil.read(filepath=scheme_data_filepath)
		StaticData.CDP_data = scheme_10_data.get('CPD')
		StaticData.GR_data = scheme_10_data.get('GR')