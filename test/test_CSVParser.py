import pytest

from src.CSVParser import CSVParser, CSVHeaderMissingException


class TestCSVParser:

    def test_reads_correct_data_properly(self):
        # given
        required_fields = ['one', 'two', 'three']
        path = 'test/mock_data/test_correct_data.csv'

        # when
        header, data = CSVParser(path, required_fields).parse_file()

        # then
        assert header == ['one', 'two', 'three']
        assert len(data) == 2
        assert data[0] == ['1', '2', '3']
        assert data[1] == ['xx', 'yy', 'zz']

    def test_returns_data_when_no_required_header_fields(self):
        # given
        path = 'test/mock_data/test_correct_data.csv'

        # when
        header, data = CSVParser(path).parse_file()

        # then
        assert header == ['one', 'two', 'three']
        assert len(data) == 2
        assert data[0] == ['1', '2', '3']
        assert data[1] == ['xx', 'yy', 'zz']

    def test_filters_rows_without_required_field(self):
        # given
        required_fields = ['one']
        path = 'test/mock_data/test_filters_rows_without_required_field.csv'

        # when
        header, data = CSVParser(path, required_fields).parse_file()

        # then
        assert header == ['one', 'two', 'three']
        assert len(data) == 1
        assert data[0] == ['xx', 'yy', 'zz']

    def test_filters_wrong_size(self):
        # given
        path = 'test/mock_data/test_filters_wrong_size.csv'

        # when
        header, data = CSVParser(path).parse_file()

        # then
        assert header == ['one', 'two', 'three']
        assert len(data) == 1
        assert data[0] == ['xx', 'yy', 'zz']

    def test_returns_empty_when_none_ok(self):
        # given
        path = 'test/mock_data/test_returns_empty_when_none_ok.csv'

        # when
        header, data = CSVParser(path).parse_file()

        # then
        assert header == ['one', 'two', 'three']
        assert not data

    def test_raises_ioerror_when_no_file(self):
        # given
        path = 'test/mock_data/non_existing_file.csv'

        # then
        with pytest.raises(FileNotFoundError):
            CSVParser(path).parse_file()

    def test_raises_exception_empty_file(self):
        # given
        path = 'test/mock_data/test_raises_exception_empty_file.csv'

        # then
        with pytest.raises(CSVHeaderMissingException):
            CSVParser(path).parse_file()
