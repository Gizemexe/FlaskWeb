from src.Domain.Schemas.baseSchema import BaseSchema

# Category schema
class CategorySchema(BaseSchema):
    class Meta:
        fields = ('Id', 'Name', 'Image', 'created_at', 'updated_at')

schema = CategorySchema(many=True)