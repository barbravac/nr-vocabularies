import pytest
from invenio_vocabularies.records.models import VocabularyType
from flask_principal import Identity, Need, UserNeed
from flask_security import login_user
from flask_security.utils import hash_password
from nr_vocabularies.records.api import NRVocabulary
from invenio_access.permissions import ActionUsers, any_user, system_process
from invenio_app.factory import create_api as _create_api
from oarepo_vocabularies.datastreams.excel import ExcelReader
from oarepo_vocabularies.datastreams.hierarchy import HierarchyTransformer
from nr_vocabularies.proxies import current_service as nr_service
@pytest.fixture(scope="module")
def extra_entry_points():
    """Extra entry points to load the mock_module features."""
    return {

    }


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_api
@pytest.fixture()
def lang_type(db):
    """Get a language vocabulary type."""
    v = VocabularyType.create(id="languages", pid_type="lng")
    db.session.commit()
    return v

@pytest.fixture(scope="function")
def lang_data():
    """Example data."""
    return {
        "id": "eng",
        "title": {"en": "English", "cs": "Angličtina"},
        "description": {"en": "English description", "cs": "Anglický popis"},
        "icon": "file-o",
        "type": "languages",
    }
@pytest.fixture(scope="module")
def app_config(app_config):
    """Mimic an instance's configuration."""
    app_config["JSONSCHEMAS_HOST"] = "localhost"
    app_config["BABEL_DEFAULT_LOCALE"] = "en"
    app_config["I18N_LANGUAGES"] = [("cs", "Czech")]
    app_config[
        "RECORDS_REFRESOLVER_CLS"
    ] = "invenio_records.resolver.InvenioRefResolver"
    app_config[
        "RECORDS_REFRESOLVER_STORE"
    ] = "invenio_jsonschemas.proxies.current_refresolver_store"
    app_config['VOCABULARIES_DATASTREAM_READERS'] = {
        "excel": ExcelReader,
    }
    app_config['VOCABULARIES_DATASTREAM_TRANSFORMERS'] = {
        "hierarchy": HierarchyTransformer,
    }
    app_config['OAREPO_VOCABULARIES_DEFAULT_SERVICE'] = nr_service

    return app_config

@pytest.fixture(scope="module")
def identity():
    """Simple identity to interact with the service."""
    i = Identity(1)
    i.provides.add(UserNeed(1))
    i.provides.add(any_user)
    i.provides.add(system_process)
    return i

@pytest.fixture(scope="module")
def nrvoc_service(app):
    """Vocabularies service object."""
    return app.extensions["nr-vocabularies"].service

@pytest.fixture(scope="function")
def clean_es(app, nrvoc_service, identity):
    try:
        NRVocabulary.index.refresh()
        for rec in NRVocabulary.index.search().scan():
            uuid = rec['uuid']
            try:
                NRVocabulary.index.connection.delete(
                    NRVocabulary.index._name,
                    uuid
                )
            except:
                pass
    except:
        pass