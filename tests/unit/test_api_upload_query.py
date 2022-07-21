
from fixtures import dynamodb  # noqa
from fixtures import client


def test_single_upload_query(dynamodb) -> None:  # noqa
    response_set = client.post(
        "/api/v1/upload/single",
        json={
            "entity_name": "i_be_testing",
            "entity_id": "1234",
            "features": [
                {
                    "feature_name": "first feature ever",
                    "feature_value": "this should work",
                }
            ]
        }
    )

    assert response_set.status_code == 200

    response_get = client.get("/api/v1/query/single/i_be_testing/1234")
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json["features"]) == 1
    feature_value = response_get_json["features"][0]
    assert feature_value["feature_name"] == "first feature ever"
    assert feature_value["feature_value"] == "this should work"
