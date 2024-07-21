from src.Domain.Entities.OrderDetail import OrderDetails
from src.Domain.Entities.Product import Products
from src.Domain.Entities.Category import Categories
from src.Domain.Entities.Order import Orders
from src.Infrastructure.Database.database import db

class OrderService:
    def __init__(self):
        pass

    async def get_all_order_items(self, user_id):
        if user_id:
            # Kullanıcının sepetindeki tüm ürünleri ve ilgili bilgileri al
            order_items = db.session.query(Orders).filter_by(UserId=user_id).all()

            # Siparişlerin detaylarını saklamak için bir liste oluştur
            result = []

            for order_item in order_items:
                # Her bir siparişin detaylarını al
                order_details = []
                details = OrderDetails.query.filter_by(OrderId=order_item.Id).all()
                order = Orders.query.filter_by(Id=order_item.Id).first()  # İlgili siparişi getir
                if order:
                    for detail in details:
                        # Ürün bilgisine productId üzerinden eriş
                        product = Products.query.filter_by(Id=detail.ProductId).first()
                        if product:
                            order_details.append({
                                "productId": detail.ProductId,
                                "productName": product.Name,
                                "productCode": product.Code,
                                "quantity": detail.Quantity,
                                "unitPrice": detail.UnitPrice,
                                "total": order.Total,  # Siparişin toplam tutarını kullan
                                # Diğer alanları buraya ekleyebilirsiniz
                            })
                        else:
                            # Ürün bilgisi bulunamazsa, productId ile eşleşen bir ürün yok demektir
                            # Bu duruma göre bir işlem yapabilirsiniz, örneğin hata mesajı ekleyebilirsiniz
                            pass
                else:
                    # Sipariş bulunamazsa, uygun bir hata işlemi gerçekleştirebilirsiniz
                    pass

                # Her bir sipariş için gerekli bilgileri al
                order_id = order_item.Id
                order_number = order_item.OrderNumber
                total = order_item.Total
                address = order_item.Address
                status = order_item.Status
                created_date = order_item.created_at

                # Sonuç listesine siparişi ve detaylarını ekleyin
                result.append({
                    "id": order_id,
                    "orderNumber": order_number,
                    "userId": user_id,
                    "total": total,
                    "address": address,
                    "status": status,
                    "createdDate": created_date,
                    "orderDetails": order_details  # Sipariş detaylarını ekleyin
                })

            return {"success": True, "orderItems": result}
        else:
            return {"success": False, "message": "Unauthorized"}, 401


order_service = OrderService()