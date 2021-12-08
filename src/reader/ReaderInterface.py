from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterable
import dateutil.parser as DateParser


def date_from_str(string):
    return DateParser.parse(string, parserinfo=DateParser.parserinfo(yearfirst=True))


RECORD_TYPE_CONVERTERS = (str, str, date_from_str, int, int, int)

def convert_to_record(string):
    """ Convert a string to a record, returning list of the records's values. Raises an Exception if the conversion is not possible.
        :param string: The record in string format
    """
    values = string.strip('\n').split(',')
    converted_values = []

    if len(values) != len(RECORD_TYPE_CONVERTERS):
        raise Exception('Invalid number of record values')

    error = False
    error_msg = ''
    for i, value in enumerate(values):
        if value == '':
            error = True
            error_msg += f'\tEmpty value at index {i}\n'
            continue

        Type = RECORD_TYPE_CONVERTERS[i]
        try: converted_values.append(Type(value))
        except:
            error_msg += f'\tCan not convert "{value}" with {Type.__name__}\n'
            converted_values.append(None)
            error = True

    if error:
        line = string.strip("\n")
        error_line = error_msg.strip("\n")
        raise Exception(f'Conversion error in line: {line}\n{error_line}'.strip("\n"))
    else:
        return converted_values


class InputReaderInterface(ABC):
    @abstractmethod
    def get_producer_records():
        """ Yields records.
        """

    def __iter__(self):
        get_producer_records_result = self.get_producer_records()
        if isinstance(get_producer_records_result, Iterable):
            return get_producer_records_result

