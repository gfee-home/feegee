from typing import Any, Dict, List

from pydantic import BaseModel


from feegee import APP
from feegee.models.entity import StandardEntity


class FeatureDefinition(BaseModel):
    feature_name: str
    feature_data_type: str


class DefinitionSetSingle(BaseModel):
    entity_name: str
    features: List[FeatureDefinition]


@APP.post("/api/v1/definitions/set_single")
def definition_set_single(definition: DefinitionSetSingle):
    StandardEntity.upsert(
        "fake_org_id",
        definition.entity_name,
        features=[feature_def.dict() for feature_def in definition.features]
    )


@APP.get("/api/v1/definitions/get_single/{entity_name}", response_model=DefinitionSetSingle)
def definition_get_single(entity_name: str) -> Dict[str, Any]:
    entity = StandardEntity.lookup("fake_org_id", entity_name)
    if entity is None:
        raise ValueError("nope")
    return {
        "entity_name": entity_name,
        "features": entity.features,
    }
