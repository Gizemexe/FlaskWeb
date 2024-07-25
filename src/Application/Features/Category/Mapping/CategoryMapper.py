from src.Domain.Entities.Category import Categories
from src.Application.DTOs.CategoryDto import CategoryDTO

class CategoryMapper:
    @staticmethod
    def to_dto(category: Categories) -> CategoryDTO:
        return CategoryDTO(
            id=category.Id,
            name=category.Name,
            image=category.Image,
            created_at=category.created_at,
            updated_at=category.updated_at
        )

    @staticmethod
    def from_dto(category_dto: CategoryDTO) -> Categories:
        return Categories(
            Id=category_dto.id,
            Name=category_dto.name,
            Image=category_dto.image,
            created_at=category_dto.created_at,
            updated_at=category_dto.updated_at
        )

    @staticmethod
    def to_response(category_dto: CategoryDTO) -> dict:
        return {
            "id": category_dto.id,
            "name": category_dto.name,
            "image": category_dto.image,

        }