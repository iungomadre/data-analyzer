import dateparser
import numpy as np
from typing import List


class InvalidDataException(ValueError):
    def __init__(self):
        pass


class DataRetriever:
    """
    Class retrieving data from raw matrix. Prepares it for further use
    """

    def __init__(self, data: List[List[str]]):
        self._data = data
        self._validate_data()

    def _validate_data(self):
        """
        Checks wether data is corrupted and cannot be analyzed properly
        """
        if not self._data or not self._data[0]:
            raise InvalidDataException

        for row in self._data:
            if len(row) != len(self._data[0]):
                raise InvalidDataException

    def get_concatenated_fields(self, indexes: List[int], delimiter: str = ''):
        """
        Concatenates fields at given indexes. Can be used to retrieve data from
        certain 'column' if only one index is being passed
        :param indexes: Row indexes to concatenate
        :param delimiter: String to be placed between words. Default = ''
        :return: Concatenated words (or one data column)
        """
        result = []
        for row in self._data:
            concatenated = ''
            for index in indexes:
                concatenated += row[index]
                if index != indexes[-1]:
                    concatenated += delimiter
            result.append(concatenated)
        return result

    def get_unique_fields(self, index):
        """
        :param index: Index of data 'column' to be analyzed
        :return: Unique fields from certain column
        """
        unique_fields = list()  # do not use set - it does not keep order of elements
        for row in self._data:
            if row[index] not in unique_fields:
                unique_fields.append(row[index])
        return unique_fields

    def get_chosen_date_rows(self, date_index: int, choosing_func, language: str = 'es'):
        """
        Get data rows that contain date fulfilling certain criteria.
        :param date_index: Index of 'column' where dates are stored
        :param choosing_func: Function returning accepted date. Takes all possible
                              dates as an argument
        :param language: Language code that for date format, e.g. [‘en’, ‘es’, ‘zh-Hant’]
        :return: Row(s) containing accepted date
        """
        dates_str = self.get_concatenated_fields([date_index])
        dates_datetime = []

        for date in dates_str:
            dates_datetime.append(dateparser.parse(date, languages=[language]))
        filtered_date = choosing_func(dates_datetime)
        indexes = np.where(np.array(dates_datetime) == filtered_date)[0]

        results = []
        for index in list(indexes):
            results.append(self._data[index])

        return results
