from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Organization(Model):
    org_name = UnicodeAttribute()
    org_id = UnicodeAttribute(hash_key=True)
