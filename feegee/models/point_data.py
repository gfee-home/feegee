from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class PointData(Model):
    org_id_entity_name_feature_name = UnicodeAttribute()
    entity_value = UnicodeAttribute()
