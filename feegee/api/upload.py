from typing import List

from pydantic import BaseModel

from feegee import APP
from feegee.models.point_data import PointData
from feegee.models.entity import StandardEntity


class FeatureValue(BaseModel):
    feature_name: str
    feature_value: str


class UploadSingle(BaseModel):
    entity_name: str
    entity_id: str
    features: List[FeatureValue]


def _valid(data: UploadSingle) -> bool:
    definition = StandardEntity.lookup(
        org_id="fake_org_id",
        entity_name=data.entity_name,
    )

    if definition is None:
        print("no def")
        return False

    definition_feature_names = [feature["feature_name"] for feature in definition.features]
    print(("def features = {}".format(definition_feature_names)))
    return all(feature.feature_name in definition_feature_names for feature in data.features)


@APP.post("/api/v1/upload/single")
def upload_single(data: UploadSingle):
    if not _valid(data):
        raise ValueError("Invalid data")

    point_data = PointData.new(
        org_id="fake_org_id",
        entity_name=data.entity_name,
        entity_id=data.entity_id,
        values={feature.feature_name: feature.feature_value for feature in data.features},
    )

    point_data.save()
