from oarepo_vocabularies.datastreams.excel import ExcelReader
import json
import os
TEST_FILE = os.path.join(os.path.dirname(__file__), 'data/slovnik.xlsx')

def test_excel_reader():
    rdr = ExcelReader(
        vocabulary_type='countries', origin=TEST_FILE)
    data = list(rdr.read())
    assert data == [
        {'level': '1', 'id': 'SK', 'title': {'cs': 'Slovensko', 'en': 'Slovakia'}, 'alpha3Code': 'SVK', 'type': 'countries'},
        {'level': '1', 'id': 'MR', 'title': {'cs': 'Morava', 'en': 'Moravia'}, 'alpha3Code': 'MRV', 'type': 'countries'},
        {'level': '1', 'id': 'CZ', 'title': {'cs': 'Česko', 'en': 'Czechia'}, 'alpha3Code': 'CZE', 'type': 'countries'}
    ]