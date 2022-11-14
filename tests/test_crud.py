from nr_vocabularies.records.api import NRVocabulary

def test_create(lang_type, lang_data, nrvoc_service, identity):
    item = nrvoc_service.create(identity, lang_data)
    assert item.id == lang_data["id"]
    for k, v in lang_data.items():
        assert item.data[k] == v

    # Read it
    read_item = nrvoc_service.read(identity, ("languages", "eng"))

    assert item.id == read_item.id
    assert item.data == read_item.data
    assert read_item.data["type"] == "languages"
