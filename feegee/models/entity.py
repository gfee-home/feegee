from enum import Enum
from typing import Dict
import json

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class FeatureType(Enum):
    STRING = 0
    INTEGER = 1
    FLOAT = 2


class StandardEntity(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "StandardEntity"
        host = "http://localhost:8000"

    org_id_entity_name = UnicodeAttribute(hash_key=True)
    features = UnicodeAttribute()

    @staticmethod
    def _hash_key(org_id: str, entity_name: str) -> str:
        return "{}|{}".format(org_id, entity_name)

    @staticmethod
    def lookup(org_id: str, entity_name: str) -> 'StandardEntity':
        return StandardEntity.get(StandardEntity._hash_key(org_id, entity_name))

    @staticmethod
    def upsert(org_id: str, entity_name: str, features: Dict[str, FeatureType]) -> None:
        full_id = StandardEntity._hash_key(org_id, entity_name)
        existing_entity = StandardEntity.get(full_id)
        if existing_entity is None:
            new_entity = StandardEntity()
            new_entity.org_id_entity_name = full_id
            new_entity.features = json.dumps(features)
            new_entity.save()
        else:
            existing_entity.features = features
            existing_entity.save()

    

