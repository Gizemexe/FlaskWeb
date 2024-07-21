from src.Domain.Entities.Product import Products
from src.Domain.Entities.Category import Categories
from src.Domain.Entities.Cart import Carts
from src.Infrastructure.Database.database import db


class CartService:
    def __init__(self):
        pass

    async def get_all_cart_items(self, user_id):
        if user_id:
            # Kullanıcının sepetindeki tüm ürünleri ve ilgili bilgileri al
            cart_items = db.session.query(Carts).filter_by(UserId=user_id).all()

            # Cart items'ları dictionary formatında saklamak için bir liste oluştur
            result = []

            for cart_item in cart_items:
                # Her bir cart item için gerekli bilgileri al
                product_id = cart_item.ProductId
                quantity = cart_item.Quantity
                cart_id = cart_item.Id

                # Product tablosundan ilgili ürünün adını ve kategorisini al
                product = db.session.query(Products).filter_by(Id=product_id).first()
                product_name = product.Name if product else None
                price = product.Price if product else None

                category_id = product.CategoryId if product else None
                category = db.session.query(Categories).filter_by(Id=category_id).first()
                category_name = category.Name if category else None

                # Sonuç listesine cart öğesini ekleyin
                result.append({
                    "id": cart_id,
                    "productId": product_id,
                    "productName": product_name,
                    "categoryName": category_name,
                    "quantity": quantity,
                    "price": price
                })

            return {"success": True, "cartItems": result}
        else:
            return {"success": False, "message": "Unauthorized"}, 401

    async def add_item_to_cart(self, user_id, cart_data):
        # Sepete ürün ekleme işlemi
        if user_id:
            product_id = cart_data.get("productId")
            quantity = cart_data.get("quantity")

            # Kullanıcının sepetinde aynı üründen var mı kontrol et
            existing_cart_item = db.session.query(Carts).filter_by(UserId=user_id, ProductId=product_id).first()
            if existing_cart_item:
                # Ürün sepette zaten var, miktarı güncelle
                existing_cart_item.Quantity += quantity
                db.session.commit()
                return {"success": True, "message": "Item quantity updated successfully"}
            else:
                # Ürün sepette yok, yeni ürün olarak ekle
                new_cart_item = Carts(UserId=user_id, ProductId=product_id, Quantity=quantity)
                db.session.add(new_cart_item)
                db.session.commit()
                return {"success": True, "message": "Item added to cart successfully"}
        else:
            return {"success": False, "message": "Unauthorized"}, 401


    async def update_cart_item(self,cart_id, cart_data):
        # Sepetteki ürünü güncelleme işlemi
            new_quantity = cart_data.get("quantity")

            # Kullanıcının sepetinde ilgili ürünü bul
            cart_item = db.session.query(Carts).filter_by(Id=cart_id).first()

            if cart_item:
                # Ürün varsa, miktarı güncelle
                cart_item.Quantity = new_quantity
                db.session.commit()
                return {"success": True, "message": "Item updated successfully"}
            else:
                return {"success": False, "message": "Item not found in the cart"}

    async def remove_cart(self,cart_id, user_id):
        # Sepetteki ürünü silme işlemi
        try:
            # Kullanıcının sepetinde ilgili ürünü bul
            cart_item = db.session.query(Carts).filter_by(Id=cart_id, UserId=user_id).first()

            if cart_item:
                # Ürün varsa, sepetten kaldır
                db.session.delete(cart_item)
                db.session.commit()
                return {"success": True, "message": "Item removed successfully"}
            else:
                return {"success": False, "message": "Item not found in the cart"}
        except Exception as e:
            return {"success": False, "message": str(e)}

cart_service = CartService()