
from tests.unit.fixtures import dynamodb

from feegee.models.entity import FeatureType, StandardEntity

def test_standard_entity(dynamodb):
    StandardEntity.upsert(
        org_id="test1234",
        entity_name="ThisIsOnlyATest",
        features={'foo': FeatureType.String}
    )

    StandardEntity.get(hash_key=)
