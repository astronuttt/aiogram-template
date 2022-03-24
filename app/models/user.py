from app.models.database import TimedBase
from tortoise import fields


class User(TimedBase):
    class Meta:
        table = "users"

    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=200, null=True)
    name = fields.CharField(max_length=200, null=True)
    phone_number = fields.CharField(max_length=14, null=True)
    super_user = fields.BooleanField(default=False)
