import io
from pathlib import Path
from src.reader.CsvReader import CsvReader
from src.reader.ReaderInterface import convert_to_record
import dateutil

def test_convert_string_to_record_invalid_num_of_values():
    try:
        convert_to_record('7c71fb42,sale,2018-12-03T23:57:40Z,')
        raise Exception('Should not be able to convert to record')
    except Exception as e:
        assert str(e) == 'Invalid number of record values'


def test_convert_string_to_record():
    record = convert_to_record('7c71fb42,sale,2018-12-03T23:57:40Z,9,8,116')
    assert record == ['7c71fb42','sale', dateutil.parser.parse('2018-12-03T23:57:40Z'), 9,8,116]


def test_convert_string_to_record_other_date_format():
    record = convert_to_record('7c71fb42,sale,18 12 03 MON 23:57:40,9,8,116')
    assert record == ['7c71fb42','sale', dateutil.parser.parse('2018-12-03T23:57:40'), 9,8,116]


def test_fail_to_convert_string_to_record():
    try:
        convert_to_record('7c71fb42,sale,2018-12-03T23:57:40Z,9,8,sakd')
        raise Exception('Should not be able to convert to record')
    except Exception as e:
        assert str(e) == 'Conversion error in line: 7c71fb42,sale,2018-12-03T23:57:40Z,9,8,sakd\n' + \
                         '\tCan not convert "sakd" with int'
        pass


def test_records_from_file():
    lines = ['transaction_id,event_type,date,store_number,item_number,value\n',
             '7c71fb42,sale,2018-12-03T23:57:40Z,9,8,116\n',]

    f = io.StringIO()
    f.writelines(lines)
    f.seek(0)

    assert len(list(CsvReader._records_from_file(f))) == 1
    f.seek(0)

    record = next(CsvReader._records_from_file(f))
    assert record == ['7c71fb42', 'sale', dateutil.parser.parse('2018-12-03T23:57:40Z'), 9, 8, 116]
    

def test_records_from_directory():
    results = [ ['7c71fb42-1f5e-45e1-be16-7d4d772d1aab','sale',dateutil.parser.parse('2018-12-03T23:57:40Z'),9,8,116],
                ['a64eaefa-16cc-4dda-a081-7b468d1bcfcc','incoming',dateutil.parser.parse('2018-10-17T05:00:05Z'),4,2,151]]
    test_dir = Path(__file__).parent.joinpath('dummy_data')
    csv_reader = CsvReader(test_dir)

    for i, record in enumerate(csv_reader):
        assert record == results[i]
