class Engine:
	def __init__(
		self,
		title: str,
		power: float,
		rotation_freq: int,
		shift_freq: int,
		delta_t: float,
	):
		self.title = title						#* ENGINE NAME
		self.power = power						#* ENGINE POWER
		self.rotation_freq = rotation_freq		#* ENGINE ROTATION FREQ
		self.shift_freq = shift_freq			#* SHIFT ROTATION FREQ
		self.delta_t = delta_t					#* Tmax / Tmin

	def __repr__(self):
		return f'[{self.title}] POWER: {self.power}, ROTATION FREQ: {self.rotation_freq}, Tmax/Tmin: {self.delta_t}, SHIFT ROTATION FREQ: ({self.shift_freq})'