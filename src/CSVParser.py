import csv
import logging

from typing import List


class CSVParser:
    """ Generic CSV parser """

    def __init__(self, file_name: str, mandatory_fields: List[str] = []):
        """
        :param file_name: csv file name
        :param mandatory_fields: fields required from rows to be accepted as not corrupted
        """
        self._fname = file_name
        self._mandatory_fields = mandatory_fields

    def parse_file(self):
        """
        Parse CSV file. Omit rows that don't contain reuired data or are of wrong length.

        :return: csv header and data read from file
        """
        data = []
        with open(self._fname, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            mandatory_ids = [header.index(field) for field in self._mandatory_fields]

            for row in reader:
                if len(row) != len(header):
                    logging.warning(f'Corrupted row skipped - wrong fields number\n{row}')
                    continue

                required_fields = [False if row[required_id] == '' else True for required_id in mandatory_ids]
                if not all(required_fields):
                    logging.warning(f'Corrupted row skipped - lacks required field(s)\n{row}')
                    continue

                data.append(row)

        if not header:
            raise Exception('No header found in CSV file')

        return header, data
