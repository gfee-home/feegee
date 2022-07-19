import subprocess

from pytest import fixture

from feegee.models.entity import StandardEntity


ALL_MODELS = [
    StandardEntity
]


@fixture(scope="session")
def dynamodb(request):
    proc = subprocess.Popen(
        ["java", "-Djava.library.path=./DynamoDBLocal_lib", "-jar", "DynamoDBLocal.jar"],
        cwd="./bin"
    )

    request.addfinalizer(lambda: proc.kill())

    for model in ALL_MODELS:
        model.create_table(wait=True)

    yield None
