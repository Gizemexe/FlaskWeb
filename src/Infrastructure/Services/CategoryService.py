from typing import List
from src.Application.DTOs.CategoryDto import CategoryDTO
from src.Application.Features.Category.Queries.GetCategoriesQuery import GetCategoriesQuery
from src.Infrastructure.Repositories.CategoryRepository import  CategoriesRepositoryImpl


class CategoryService:
    def __init__(self, categories_repository: CategoriesRepositoryImpl):
        self.categories_repository = categories_repository

    def get_all_categories(self, query: GetCategoriesQuery) -> List[CategoryDTO]:
        return query.execute()
