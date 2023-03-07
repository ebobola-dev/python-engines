import json

class JsonUtil:
	@staticmethod
	def read(filepath: str):
		with open(filepath, 'r', encoding='utf-8') as json_file:
			return json.load(json_file)

	@staticmethod
	def write(filepath: str, data: dict | list | tuple):
		with open(filepath, 'w', encoding='utf-8') as json_file:
			json.dump(data, json_file, indent=4, ensure_ascii=False)