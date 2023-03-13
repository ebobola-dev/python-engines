from utils.json_rw import JsonUtil
from models.engine_list import EngineList

class DefaultGearRatios:
	def __init__(
		self,
		json_view: dict,
	):
		self.SSC_1_ROW: tuple = tuple(json_view.get('ssc'))[0]
		self.SSC_2_ROW: tuple = tuple(json_view.get('ssc'))[1]
class StaticData:
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
		StaticData.engine_list = EngineList(
		engines_source_filepath=engine_list_filepath,
		constant_values_filepath=engine_constant_values_filepath,
		)
		scheme_10_data: dict | None = JsonUtil.read(filepath=scheme_data_filepath)
		StaticData.CDP = scheme_10_data.get('CPD')
		StaticData.GR = scheme_10_data.get('GR')
		StaticData.DGR = DefaultGearRatios(json_view=JsonUtil.read(filepath=default_gear_ratios))
