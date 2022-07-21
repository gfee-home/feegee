
from fixtures import dynamodb, client


def test_definition_set_single(dynamodb) -> None:
    response_set = client.post(
        "/api/v1/definitions/set_single",
        json={
            "entity_name": "i_be_testing",
            "features": [
                {
                    "feature_name": "first feature ever",
                    "feature_data_type": "string",
                }
            ]
        }
    )

    assert response_set.status_code == 200

    response_get = client.get("/api/v1/definitions/get_single/i_be_testing")
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert response_get_json["entity_name"] == "i_be_testing"
    assert len(response_get_json["features"]) == 1
