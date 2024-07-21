from src.Domain.Schemas.baseSchema import BaseSchema

# Category schema
class CartSchema(BaseSchema):
    class Meta:
        fields = ('Id', 'UserId', 'ProductId', "Quantity", 'created_at', 'updated_at')

schema = CartSchema(many=True)