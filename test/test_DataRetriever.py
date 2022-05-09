import pytest

from src.DataRetriever import DataRetriever, InvalidDataException

DATA = [
    ['one', 'two', 'three'],
    ['one', 'yy', 'zz'],
    ['x', 'y', 'z']
]

CORRUPTED_DATA = [
    ['one', 'two', 'three'],
    ['four', 'five']
]

EMPTY_DATA = []

PARTIALLY_EMPTY_DATA = [
    [],
    []
]

DATES = [
    ['24/04/2019'],
    ['10/2/2019'],
    ['24/04/2018'],
    ['24/04/2017']
]

DATES_DUPLICATES = [
    ['24/04/2019'],
    ['24/04/2019'],
    ['24/04/2018'],
    ['24/04/2017'],
    ['24/04/2017']
]


class TestDataRetriever:

    def test_throws_invaliddataexception_on_creation_when_data_corrupted(self):
        with pytest.raises(InvalidDataException):
            DataRetriever(CORRUPTED_DATA)

    def test_throws_invaliddataexception_on_creation_when_data_empty(self):
        with pytest.raises(InvalidDataException):
            DataRetriever(EMPTY_DATA)

    def test_throws_invaliddataexception_on_creation_when_first_row_empty(self):
        with pytest.raises(InvalidDataException):
            DataRetriever(EMPTY_DATA)

    def test_object_creates_when_data_not_corrupted(self):
        retriever = DataRetriever(DATA)

    def test_get_concatenated_two_fields(self):
        retriever = DataRetriever(DATA)
        expected = ['one two', 'one yy', 'x y']
        actual = retriever.get_concatenated_fields([0, 1], ' ')
        assert actual == expected

    def test_get_concatenated_returs_column(self):
        retriever = DataRetriever(DATA)
        expected = ['one', 'one', 'x']
        actual = retriever.get_concatenated_fields([0])
        assert actual == expected

    def test_get_concatenated_all_fields(self):
        retriever = DataRetriever(DATA)
        expected = ['one two three', 'one yy zz', 'x y z']
        actual = retriever.get_concatenated_fields([0, 1, 2], ' ')
        assert actual == expected

    def test_get_unique_fields(self):
        retriever = DataRetriever(DATA)
        expected = ['one', 'x']
        actual = retriever.get_unique_fields(0)
        assert actual == expected

    def test_get_earliest_date_row_no_duplicates(self):
        retriever = DataRetriever(DATES)
        expected = [['24/04/2017']]
        actual = retriever.get_chosen_date_rows(0, min)
        assert actual == expected

    def test_get_earliest_date_row_duplicates(self):
        retriever = DataRetriever(DATES_DUPLICATES)
        expected = [['24/04/2017'], ['24/04/2017']]
        actual = retriever.get_chosen_date_rows(0, min)
        assert actual == expected

    def test_get_latest_date_row_no_duplicates(self):
        retriever = DataRetriever(DATES)
        expected = [['24/04/2019']]
        actual = retriever.get_chosen_date_rows(0, max)
        assert actual == expected

    def test_get_oldest_date_row_duplicates(self):
        retriever = DataRetriever(DATES_DUPLICATES)
        expected = [['24/04/2019'], ['24/04/2019']]
        actual = retriever.get_chosen_date_rows(0, max)
        assert actual == expected
