from src.Infrastructure.Repositories.ProductRepository import ProductsRepositoryImpl
from src.Application.DTOs.ProductDto import ProductDTO
from src.Application.Features.Product.Mapping.ProductMapper import ProductMapper

class GetProductsQuery:
    def __init__(self, products_repository: ProductsRepositoryImpl):
        self.products_repository = products_repository

    def execute(self):
        products = self.products_repository.get_all()
        return [ProductMapper.to_dto(product) for product in products]
