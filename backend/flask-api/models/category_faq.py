from db import db



class CategoryModel(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    type = db.Column(db.String(30), unique=False, nullable=False)
    num_faq = db.Column(db.Integer)
    def __init__(self, type_category):
        self.type = type_category
        self.num_faq = 0
    def json(self):
        return {
            "id": self.id,
            "type": self.type,
            "num_faq": self.num_faq
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def add_faq(self):
        self.num_faq+=1
    @classmethod
    def find_by_id(cls, idd):
        return CategoryModel.query.filter_by(id=idd).first()

    @classmethod
    def type_exist(cls, type_category):
        return bool(CategoryModel.query.filter_by(type=type_category).first())

    @classmethod
    def find_by_type(cls, type_category):
        return CategoryModel.query.filter_by(type=type_category).first()

    @classmethod
    def get_categories(cls):
        category_list = [category.json() for category in CategoryModel.query.all()]
        dicc = {"Categories": category_list}
        return dicc
