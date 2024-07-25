from src.Infrastructure.Repositories.CategoryRepository  import CategoriesRepositoryImpl
from src.Application.DTOs.CategoryDto import CategoryDTO
from src.Application.Features.Category.Mapping.CategoryMapper import CategoryMapper

class GetCategoriesQuery:
    def __init__(self, categories_repository: CategoriesRepositoryImpl):
        self.categories_repository = categories_repository

    def execute(self):
        categories = self.categories_repository.get_all()
        return [CategoryMapper.to_dto(category) for category in categories]
