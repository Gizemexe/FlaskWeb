from src.Domain.Schemas.baseSchema import BaseSchema

# Category schema
class OrderSchema(BaseSchema):
    class Meta:
        fields = ('Id', 'UserId', 'OrderNumber', "Address", "Total", 'created_at', 'updated_at')

schema = OrderSchema(many=True)