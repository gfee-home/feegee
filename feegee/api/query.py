from typing import List

from pydantic import BaseModel

from feegee import APP
from feegee.models.point_data import PointData


class FeatureValue(BaseModel):
    feature_name: str
    feature_value: str


class QuerySingle(BaseModel):
    features: List[FeatureValue]


@APP.get("/api/v1/query/single/{entity_name}/{entity_id}", response_model=QuerySingle)
def query_single(entity_name: str, entity_id: str):
    point_data = PointData.lookup(
        org_id="fake_org_id",
        entity_name=entity_name,
        entity_id=entity_id,
    )

    return {
        "features": [
            {
                "feature_name": feature_name,
                "feature_value": feature_value,
            }
        for feature_name, feature_value in point_data.values.items()]
    }
