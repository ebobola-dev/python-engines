from sys import argv

from utils.numbers import NumbersUtil
from services.console import ConsoleService, ConsoleColors

class ArgsUtil:
	@staticmethod
	def try_read():
		failed_result = (None, None, None)
		failed_message = "Обнаружены непоходящие параметры запуска:"
		args = argv[1:]
		if len(args) < 3:
			if len(args) > 0:
				ConsoleService.console.print(f"{failed_message} необходимо три значения типа float (Получено {len(args)} значения)\n", style=ConsoleColors.ERROR)
			return failed_result
		args = args[:3]
		try:
			float_argv = tuple(map(lambda str_arg: float(str_arg), args))
		except ValueError:
			bad_values = {arg for arg in args if not NumbersUtil.is_float(arg)}
			ConsoleService.console.print(f"{failed_message} необходимы значения типа float ({bad_values} не удалось преобразовать в float)\n", style=ConsoleColors.ERROR)
			return failed_result
		return float_argv