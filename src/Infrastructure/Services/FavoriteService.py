from typing import List
from src.Application.DTOs.FavoriteDto import FavoriteDTO
from src.Application.Features.Favorite.Commands.AddFavoriteCommand import AddFavoriteCommand
from src.Application.Features.Favorite.Commands.RemoveFavoriteCommand import RemoveFavoriteCommand
from src.Application.Features.Favorite.Queries.GetFavoritesQuery import GetFavoritesQuery
from src.Infrastructure.Repositories.FavoriteRepository import FavoritesRepositoryImpl
from src.Application.Features.Favorite.Mapping.FavoriteMapper import FavoriteMapper
from src.Domain.Entities.Favorites import Favorites

class FavoriteService:
    def __init__(self, favorites_repository: FavoritesRepositoryImpl):
        self.favorites_repository = favorites_repository

    def add_favorite(self, command: AddFavoriteCommand) -> FavoriteDTO:
        existing_favorite = self.favorites_repository.get_favorite_by_user_and_product(command.user_id, command.product_id)
        if existing_favorite:
            raise Exception('Product already in favorites')

        favorite = Favorites(UserId=command.user_id, ProductId=command.product_id)
        new_favorite = self.favorites_repository.add_favorite(favorite)
        return FavoriteMapper.to_dto(new_favorite)

    def get_favorites_by_user(self, query: GetFavoritesQuery) -> List[FavoriteDTO]:
        favorites = self.favorites_repository.get_favorites_by_user(query.user_id)
        return [FavoriteMapper.to_dto(favorite) for favorite in favorites]

    def remove_favorite(self, command: RemoveFavoriteCommand) -> bool:
        favorite = self.favorites_repository.get_favorite_by_user_and_product(command.user_id, command.product_id)
        if not favorite:
            raise Exception('Product is not in favorites')

        self.favorites_repository.remove_favorite(favorite)
        return True
