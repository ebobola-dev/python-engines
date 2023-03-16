class CPD:
	def __init__(
			self,
			couplings: float,
			OCD: float,
			CSG: float,
			bearing: float,
		):
		self.couplings = couplings
		self.OCD = OCD
		self.CSG = CSG
		self.bearing = bearing

class GR:
	def __init__(
			self,
			CSG: float,
			OCD: float,
		):
		self.CSG = CSG
		self.OCD = OCD

class Scheme:
	def __init__(
			self,
			number: int,
			CPD: CPD,
			GR: GR,
		):
		self.number = number
		self.CPD = CPD
		self.GR = GR

	@staticmethod
	def from_json(scheme_data_json: dict):
		return Scheme(
			number=scheme_data_json.get('number'),
			CPD=CPD(**scheme_data_json.get("CPD")),
			GR=GR(**scheme_data_json.get("GR")),
		)