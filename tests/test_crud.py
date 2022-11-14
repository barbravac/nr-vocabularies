import pytest
from invenio_pidstore.errors import PIDDeletedError

from nr_vocabularies.records.api import NRVocabulary

def test_crud(clean_es ,lang_type, lang_data, nrvoc_service, identity):
    item = nrvoc_service.create(identity, lang_data)

    assert item.id == lang_data["id"]

    for k, v in lang_data.items():
        assert item.data[k] == v

    read_item = nrvoc_service.read(identity, ("languages", "eng"))

    assert item.id == read_item.id
    assert item.data == read_item.data
    assert read_item.data["type"] == "languages"

    data = {'id': 'eng', 'title': {'en': 'English', 'cs': 'Angličtina'}, 'description': {'en': 'new', 'cs': 'Anglický popis'}, 'icon': 'file-o', 'type': 'languages'}
    updated_record = nrvoc_service.update(identity, ("languages", "eng"), data)

    assert updated_record.data['revision_id'] == 2

    nrvoc_service.delete(identity, ("languages", "eng"))

    with pytest.raises(PIDDeletedError):
        nrvoc_service.read(identity, ("languages", "eng"))