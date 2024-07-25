from src.Domain.Entities.Category import Categories

class CategoriesRepositoryImpl:
    def get_all(self):
        return Categories.query.all()
