from src.Domain.Schemas.baseSchema import BaseSchema

# Category schema
class OrderDetailSchema(BaseSchema):
    class Meta:
        fields = ('Id', 'OrderId', 'ProductId', 'ProductName', 'Quantity', 'UnitPrice', 'created_at', 'updated_at')

schema = OrderDetailSchema(many=True)