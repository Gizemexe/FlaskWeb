from datetime import datetime
from wsgiref import validate
from flask_marshmallow import Marshmallow

ma = Marshmallow()

# Base schema class
class BaseSchema(ma.Schema):
    created_at = ma.DateTime(dump_only=True, default=datetime.now)
    updated_at = ma.DateTime(dump_only=True, default=datetime.now)
