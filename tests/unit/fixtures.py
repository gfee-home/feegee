import subprocess
import os
import time

from pytest import fixture
from fastapi.testclient import TestClient

from feegee import APP
import feegee.loader  # noqa
from feegee.models.entity import StandardEntity
from feegee.models.point_data import PointData


client = TestClient(APP)


ALL_MODELS = [
    StandardEntity,
    PointData
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

    time.sleep(2)

    request.addfinalizer(lambda: proc.kill())

    os.environ["AWS_ACCESS_KEY_ID"] = "dummy_access_key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "dummy_secret_key"

    for model in ALL_MODELS:
        model.create_table(wait=True)

    yield None
