from typing import Dict, Any, Optional
from datetime import datetime
import json

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute


class PointData(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = "StandardEntity"
        host = "http://localhost:8000"

    org_id_entity_name_entity_id = UnicodeAttribute(hash_key=True)
    values_str = UnicodeAttribute()
    last_updated = UTCDateTimeAttribute()

    @staticmethod
    def new(
        org_id: str,
        entity_name: str,
        entity_id: str,
        values: Dict[str, Any],
        last_updated: Optional[datetime] = None,
    ) -> 'PointData':
        return PointData(
            hash_key=PointData._hash_key(org_id, entity_name, entity_id),
            values_str=json.dumps(values),
            last_updated=last_updated if last_updated else datetime.utcnow()
        )

    @staticmethod
    def _hash_key(org_id: str, entity_name: str, entity_id: str) -> str:
        return "|".join([org_id, entity_name, entity_id])

    @property
    def org_id(self) -> str:
        return self.org_id_entity_name_entity_id.split("|")[0]

    @property
    def entity_name(self) -> str:
        return self.org_id_entity_name_entity_id.split("|")[1]

    @property
    def entity_id(self) -> str:
        return self.org_id_entity_name_entity_id.split("|")[2]

    @property
    def values(self) -> Dict[str, Any]:
        return json.loads(self.values_str)

    @staticmethod
    def lookup(org_id: str, entity_name: str, entity_id: str) -> Optional['PointData']:
        try:
            return PointData.get(PointData._hash_key(org_id, entity_name, entity_id))
        except PointData.DoesNotExist:
            return None
