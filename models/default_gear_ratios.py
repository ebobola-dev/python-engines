class DGR:
	def __init__(
			self,
			ru_name: str,
			row_1: tuple[float],
			row_2: tuple[float] | None = None,
	):
		self.ru_name = ru_name
		self.row_1 = row_1
		self.row_2 = row_2
		if not isinstance(self.row_1, tuple):
			self.row_1 = tuple(self.row_1)
		if not isinstance(self.row_2, tuple) and self.row_2 is not None:
			self.row_2 = tuple(self.row_2)

class DefaultGearRatios:
	def __init__(
			self,
			cylindrical: DGR,
			conical: DGR,
			worm: DGR,
	):
		self.cylindrical = cylindrical
		self.conical = conical
		self.worm = worm

	@staticmethod
	def from_json(dgrs_json: dict):
		return DefaultGearRatios(
			cylindrical=DGR(**dgrs_json.get("cylindrical")),
			conical=DGR(**dgrs_json.get("conical")),
			worm=DGR(**dgrs_json.get("worm")),
		)

	def get_dgr_by_str_type(self, str_type: str):
		match str_type:
			case "cylindrical":
				return self.cylindrical
			case "conical":
				return self.conical
			case "worm":
				return self.worm