from .ReaderInterface import InputReaderInterface, convert_to_record
from pathlib import Path


class ConversionError():
    def __init__(self, error_msg):
        self.error_msg = error_msg


class CsvReader(InputReaderInterface):
    def __init__(self, path):
        """ Reads records from a CSV file.
            :param path: Path to the CSV file or a directory with csv files in it.
        """
        path = Path(path)
        self.files = []
        if path.is_dir():
            for csv_file in path.glob('**/*.csv'):
                self.files.append(csv_file)
        elif path.is_file() and path.suffix == '.csv':
            self.files.append(path)
        else:
            raise Exception("Invalid path for CsvReader")

    @staticmethod
    def _records_from_file(file_handle):
        """ Yields records(list of record values) from file like object.
            :param file_handle: File handle
        """
        columns = file_handle.readline()
        for line in file_handle:
            try:
                converted_values = convert_to_record(line)
                yield converted_values
            except Exception as e:
                yield ConversionError(str(e))

    
    def get_producer_records(self):
        """ Yields records.
        """
        for file in self.files:
            for record in self._records_from_file(open(file, 'r')):
                yield record