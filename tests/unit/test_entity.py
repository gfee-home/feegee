import subprocess
import os

from pytest import fixture

from feegee.models.entity import StandardEntity, FeatureDataType


ALL_MODELS = [
    StandardEntity
]


@fixture(scope="session")
def dynamodb(request):
    proc = subprocess.Popen(
        ["java", "-Djava.library.path=./DynamoDBLocal_lib", "-jar", "DynamoDBLocal.jar", "-inMemory"],
        shell=False,
        stdin=None,
        stdout=None,
        stderr=None,
        close_fds=True,
        cwd="./bin"
    )

    request.addfinalizer(lambda: proc.kill())

    os.environ["AWS_ACCESS_KEY_ID"] = "dymmy_access_key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "dymmy_secret_key"

    for model in ALL_MODELS:
        model.create_table(wait=True)

    yield None


def test_standard_entity(dynamodb):
    StandardEntity.upsert(
        org_id="test1234",
        entity_name="ThisIsOnlyATest",
        features={'foo': FeatureDataType.STRING}
    )

    entity = StandardEntity.lookup("test1234", "ThisIsOnlyATest")

    assert entity.entity_name == "ThisIsOnlyATest"
    assert entity.org_id == "test1234"
