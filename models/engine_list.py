from string import ascii_lowercase
from openpyxl import load_workbook
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from models.engine import Engine


class EngineList:
    def __init__(self, source_filename: str):
        self._init_from_file(source_filename)
        self._init_shift_rot_freqs_list()
        self._init_power_list()
        self._init_engine_list()

    def _init_from_file(self, filename: str):
        self._engine_book: Workbook = load_workbook(filename)
        self._sheet: Worksheet = self._engine_book.active

    def _init_shift_rot_freqs_list(self):
        self._shift_rot_freqs = tuple(sorted(set(
            col[0] for col in self._sheet.iter_cols(values_only=True) if isinstance(col[0], float)
        )))

    def _init_power_list(self):
        self._power_list = tuple(sorted(
            row[0] for row in self._sheet.iter_rows(values_only=True) if isinstance(row[0], float)
        ))

    def _init_engine_list(self):
        engine_columns = tuple(
            col_num for col_num, col in enumerate(self._sheet.iter_cols(values_only=True)) if col[1] == 'Тип двигателя'
        )
        self._engine_list: list[Engine] = []
        for eng_col in engine_columns:
            for row_num in range(2, self._sheet.max_row):
                engine_title = self._sheet[ascii_lowercase[eng_col] + str(row_num + 1)].value
                if engine_title is not None:
                    self._engine_list.append(Engine(
                        title=engine_title,
                        power=self._sheet['a' + str(row_num + 1)].value,
                        rotation_freq=self._sheet[ascii_lowercase[eng_col + 1] + str(
                            row_num + 1)].value,
                        shaft_rotation_freq=self._sheet[ascii_lowercase[eng_col] + str(
                            1)].value,
                        delta_t=self._sheet[ascii_lowercase[eng_col +
                                                            2] + str(row_num + 1)].value,
                    ))

    def get_shift_rot_freqs(self):
        return self._shift_rot_freqs

    def get_power_list(self):
        return self._power_list

    def get_engine_list(self):
        return self._engine_list[:]

    def get_required_engine(self, req_freq: float, req_power: float):
        closest_freq = min(
            shift_rot_freq for shift_rot_freq in self.get_shift_rot_freqs() if (shift_rot_freq - req_freq >= 0)
        )

        closest_power = min(
            power for power in self.get_power_list() if (power - req_power >= 0)
        )
        return tuple(filter(
            lambda engine: engine.shift_rotation_freq == closest_freq and engine.power == closest_power,
            self._engine_list,
        ))[0]
