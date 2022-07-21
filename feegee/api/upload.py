from typing import List

from pydantic import BaseModel

from feegee import APP
from feegee.models.point_data import PointData


class FeatureValue(BaseModel):
    feature_name: str
    feature_value: str


class UploadSingle(BaseModel):
    entity_name: str
    entity_id: str
    features: List[FeatureValue]


def _valid(data: UploadSingle) -> bool:
    return True


@APP.post("/api/v1/upload/single")
def upload_single(data: UploadSingle):
    if not _valid(data):
        raise ValueError("Invalid data")

    point_data = PointData.new(
        org_id="test1234",
        entity_name=data.entity_name,
        entity_id=data.entity_id,
        values={feature.feature_name: feature.feature_value for feature in data.features},
    )

    point_data.save()
