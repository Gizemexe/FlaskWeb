from src.Domain.Entities.Product import Products

class ProductsRepositoryImpl:
    def get_all(self):
        return Products.query.all()

    def get_products_by_category_id(self, category_id):
        return Products.query.filter_by(CategoryId=category_id).all()

    def search(self, query):
        return Products.query.filter(
            (Products.Name.ilike(f'%{query}%')) |
            (Products.Description.ilike(f'%{query}%'))
        ).all()
