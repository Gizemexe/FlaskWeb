from src.Domain.Schemas.baseSchema import BaseSchema

# User schema
class UserSchema(BaseSchema):
    class Meta:
        fields = ('Id', 'Username', 'Email', 'Password','BirthDay', 'Phone', 'created_at', 'updated_at')

schema = UserSchema(many=True)