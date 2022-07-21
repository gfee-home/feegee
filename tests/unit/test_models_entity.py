from feegee.models.entity import StandardEntity, FeatureDataType
from fixtures import dynamodb  # noqa


def test_standard_entity(dynamodb):  # noqa
    StandardEntity.upsert(
        org_id="test1234",
        entity_name="ThisIsOnlyATest",
        features={'foo': FeatureDataType.STRING}
    )

    entity = StandardEntity.lookup("test1234", "ThisIsOnlyATest")

    assert entity.entity_name == "ThisIsOnlyATest"
    assert entity.org_id == "test1234"
