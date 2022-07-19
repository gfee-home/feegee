from typing import Dict, Optional
import json

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class FeatureDataType():
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"


class StandardEntity(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "StandardEntity"
        host = "http://localhost:8000"

    org_id_entity_name = UnicodeAttribute(hash_key=True)
    features_str = UnicodeAttribute()

    @staticmethod
    def _hash_key(org_id: str, entity_name: str) -> str:
        return "{}|{}".format(org_id, entity_name)

    @property
    def org_id(self) -> str:
        return self.org_id_entity_name.split('|')[0]

    @property
    def entity_name(self) -> str:
        return self.org_id_entity_name.split('|')[1]

    @property
    def features(self) -> Dict[str, str]:
        return json.loads(self.features_str)

    @staticmethod
    def lookup(org_id: str, entity_name: str) -> Optional['StandardEntity']:
        try:
            return StandardEntity.get(StandardEntity._hash_key(org_id, entity_name))
        except StandardEntity.DoesNotExist:
            return None

    @staticmethod
    def upsert(org_id: str, entity_name: str, features: Dict[str, str]) -> None:
        full_id = StandardEntity._hash_key(org_id, entity_name)
        try:
            existing_entity = StandardEntity.get(full_id)
            existing_entity.features_str = json.dumps(features)
            existing_entity.save()
        except StandardEntity.DoesNotExist:
            new_entity = StandardEntity()
            new_entity.org_id_entity_name = full_id
            new_entity.features_str = json.dumps(features)
            new_entity.save()
