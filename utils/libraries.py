import pkg_resources

from config.filepaths import FILEPATHS

class LibrariesUtil:
	@staticmethod
	def get_required_libraries():
		with open(FILEPATHS.REQUIRED_LIBRARIES, 'r', encoding='utf-8') as required_libraries_file:
			return set(map(lambda str_lib: str_lib[:str_lib.find('=')], required_libraries_file.readlines()))

	@staticmethod
	def all_required_libraries_is_installed():
		required_libraries = LibrariesUtil.get_required_libraries()
		installed_libraries = {pkg.key for pkg in pkg_resources.working_set}
		skipped_libraries = required_libraries - installed_libraries
		if len(skipped_libraries) > 0:
			print(f"\nНе все необходимые библиотеки установлены ({skipped_libraries} не обнаружены)")
			print(f"Используйте 'pip install -r {FILEPATHS.REQUIRED_LIBRARIES}' в своём окружении для установки всех необходимых библиотек\n")
			return False
		return True