from flask_restful import Resource, reqparse
from db import db
from models.accounts import AccountModel, auth
from models.book import BookModel
from models.review import ReviewModel

class ReviewListUser(Resource):

    def get(self, user_id):
        user = AccountModel.find_by_id(user_id)
        if not user:
            return {'message': "User with ['id': {}] not found".format(user_id)}, 404
        return {'reviews': [i.json()['review'] for i in ReviewModel.find_by_user(user_id)]}, 200


class ReviewListBook(Resource):

    def get(self, book_id):
        book = BookModel.find_by_id(book_id)
        if not book:
            return {'message': "Book with ['id': {}] not found".format(book_id)}, 404
        return {'reviews': [i.json()['review'] for i in ReviewModel.find_by_book(book_id)]}, 200


class ReviewList(Resource):

    def get(self):
        return {'reviews': [i.json()['review'] for i in db.session.query(ReviewModel).all()]}, 200


class Review(Resource):

    def get(self, idd):
        review = ReviewModel.find_by_id(idd)
        if review:
            return review.json(), 200
        return {'message': "Review with ['id': {}] not found".format(idd)}, 404

    @auth.login_required
    def post(self):
        data = self.__parse_request__()
        user = AccountModel.find_by_id(data.get('user_id'))
        book = BookModel.find_by_id(data.get('book_id'))
        if not user or not book:
            if not user:
                return {'message': "There is no account with ['id': {}]".format(data.get('user_id'))}, 404
            if not book:
                return {'message': "There is no book with ['id': {}]".format(data.get('book_id'))}, 404
        new_review = ReviewModel(data.get('title'), data.get('user_id'), data.get('book_id'), data.get('date'),
                                 data.get('valuation'), data.get('comment'))
        new_review.save_to_db()
        user.reviews.append(new_review)
        book.reviews.append(new_review)
        return new_review.json(), 201

    @auth.login_required(role = 'stock_manager')
    def put(self, idd):
        data = self.__parse_request__()
        review = ReviewModel.find_by_id(idd)
        if not review:
            return {'message': "There is no review with ['id': {}]".format(idd)}, 404
        review.delete_from_db()
        user = AccountModel.find_by_id(data.get('user_id'))
        book = BookModel.find_by_id(data.get('book_id'))
        if not user or not book:
            if not user:
                return {'message': "There is no account with ['id': {}]".format(data.get('user_id'))}, 404
            if not book:
                return {'message': "There is no book with ['id': {}]".format(data.get('book_id'))}, 404
        new_review = ReviewModel(data.get('title'), data.get('user_id'), data.get('book_id'), data.get('date'),
                                 data.get('valuation'), data.get('comment'))
        new_review.save_to_db()
        user.reviews.append(new_review)
        book.reviews.append(new_review)
        return new_review.json(), 200

    @auth.login_required(role = 'stock_manager')
    def delete(self, idd):
        exists = ReviewModel.find_by_id(idd)
        if not exists:
            return {'message': "There is no review with ['id': {}], therefore it cannot be deleted".format(idd)}, 404
        user = AccountModel.find_by_id(exists.user_id)
        book = BookModel.find_by_id(exists.book_id)
        exists.delete_from_db()
        return {'message': "Review with ['id': {}] has successfully been deleted".format(idd)}, 200

    def __parse_request__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help="Operation not valid: 'title' not provided")
        parser.add_argument('user_id', type=int, required=True, help="Operation not valid: 'user_id' not provided")
        parser.add_argument('book_id', type=int, required=True, help="Operation not valid: 'book_id' not provided")
        parser.add_argument('date', type=str, required=True, help="Operation not valid: 'date' not provided")
        parser.add_argument('valuation', type=str, required=True, help="Operation not valid: 'valuation' not provided")
        parser.add_argument('comment', type=str, required=True, help="Operation not valid: 'comment' not provided")
        return parser.parse_args()
