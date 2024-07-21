
from typing import List
from src.Application.DTOs.ProductDto import ProductDTO
from src.Application.Features.Product.Queries.GetProductsQuery import GetProductsQuery
from src.Application.Features.Product.Queries.GetProductsByCategoryIdQuery import GetProductsByCategoryIdQuery
from src.Application.Features.Product.Queries.SearchProductsQuery import SearchProductsQuery
from src.Infrastructure.Repositories.ProductRepository import ProductsRepositoryImpl
from src.Application.Features.Product.Mapping.ProductMapper import ProductMapper

class ProductService:
    def __init__(self, products_repository: ProductsRepositoryImpl):
        self.products_repository = products_repository

    def get_all_products(self, query: GetProductsQuery) -> List[ProductDTO]:
        return query.execute()

    def get_products_by_category(self, query):
        return self.products_repository.get_products_by_category_id(query.category_id)

    def search_products(self, query: SearchProductsQuery) -> List[ProductDTO]:
        products = self.products_repository.search(query.query)
        return [ProductMapper.to_dto(product) for product in products]
