from src.Domain.Schemas.baseSchema import BaseSchema

# Product schema
class ProductSchema(BaseSchema):
    class Meta:
        fields = ('Id', 'Name', 'Code', 'Description', 'Price', 'Image', 'Stock', 'created_at', 'updated_at')

schema = ProductSchema(many=True)