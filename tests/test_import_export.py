import tempfile

from invenio_vocabularies.records.api import Vocabulary
from oarepo_runtime.datastreams.fixtures import dump_fixtures, load_fixtures
from oarepo_runtime.uow import BulkUnitOfWork


def test_complex_import_export(app, db, cache, search_clear, vocab_cf):
    result = load_fixtures(batch_size=100, uow_class=BulkUnitOfWork)
    assert result.failed_count == 0
    assert result.skipped_count == 0
    assert len(result.results) == 10
    Vocabulary.index.refresh()
    with tempfile.TemporaryDirectory() as d:
        dump_result = dump_fixtures(d)
        assert dump_result.failed_count == 0
        assert dump_result.skipped_count == 0
        assert dump_result.ok_count == result.ok_count
