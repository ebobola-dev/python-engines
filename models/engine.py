class Engine:
	def __init__(
		self,
		title: str,
		power: float,
		rotation_freq: int,
		shaft_rotation_freq: int,
		delta_t: float,
	):
		self.title = title
		self.power = power
		self.rotation_freq = rotation_freq
		self.shift_rotation_freq = shaft_rotation_freq
		self.delta_t = delta_t

	def __repr__(self):
		return f'{self.title}: {self.power}, {self.rotation_freq}, {self.delta_t}, ({self.shift_rotation_freq})'