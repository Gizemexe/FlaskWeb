from src.Domain.Entities.Favorites import Favorites
from src.Application.DTOs.FavoriteDto import FavoriteDTO

class FavoriteMapper:
    @staticmethod
    def to_dto(favorite: Favorites) -> FavoriteDTO:
        return FavoriteDTO(
            id=favorite.Id,
            user_id=favorite.UserId,
            product_id=favorite.ProductId,
            created_at=favorite.created_at,
            updated_at=favorite.updated_at
        )

    @staticmethod
    def from_dto(favorite_dto: FavoriteDTO) -> Favorites:
        return Favorites(
            Id=favorite_dto.id,
            UserId=favorite_dto.user_id,
            ProductId=favorite_dto.product_id,
            created_at=favorite_dto.created_at,
            updated_at=favorite_dto.updated_at
        )

    @staticmethod
    def to_response(favorite_dto: FavoriteDTO) -> dict:
        return {
            "id": favorite_dto.id,
            "user_id": favorite_dto.user_id,
            "product_id": favorite_dto.product_id,
            #"created_at": favorite_dto.created_at.isoformat() if favorite_dto.created_at else None,
            #"updated_at": favorite_dto.updated_at.isoformat() if favorite_dto.updated_at else None
        }
