from src.Domain.Entities.Product import Products
from src.Application.DTOs.ProductDto import ProductDTO

class ProductMapper:
    @staticmethod
    def to_dto(product: Products) -> ProductDTO:
        return ProductDTO(
            id=product.Id,
            name=product.Name,
            code=product.Code,
            description=product.Description,
            price=product.Price,
            image=product.Image,
            stock=product.Stock,
            category_id=product.CategoryId,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

    @staticmethod
    def from_dto(product_dto: ProductDTO) -> Products:
        return Products(
            Id=product_dto.id,
            Name=product_dto.name,
            Code=product_dto.code,
            Description=product_dto.description,
            Price=product_dto.price,
            Image=product_dto.image,
            Stock=product_dto.stock,
            CategoryId=product_dto.category_id,
            created_at=product_dto.created_at,
            updated_at=product_dto.updated_at
        )

    @staticmethod
    def to_response(product_dto: ProductDTO) -> dict:
        return {
            "id": product_dto.id,
            "name": product_dto.name,
            "code": product_dto.code,
            "description": product_dto.description,
            "price": product_dto.price,
            "imagePath": product_dto.image,
            "stock": product_dto.stock,
        }