from flask_restful import Resource, reqparse
from db import db
from models.book import BookModel
from models.interface import InterfaceModel


class InterfaceList(Resource):

    def get(self):
        return {'interfaces': [i.json() for i in db.session.query(InterfaceModel).all()]}, 200


class InterfaceListBooks(Resource):

    def get(self, id_interface):
        interface = InterfaceModel.find_by_id(id_interface)
        if not interface:
            return {'message': "Interface with ['id': {}] not found".format(id_interface)}, 404
        return {'books': [i.json() for i in interface.books]}, 200

    def post(self, id_interface, id_book):
        interface = InterfaceModel.find_by_id(id_interface)
        if not interface:
            return {'message': "Interface with ['id': {}] not found".format(id_interface)}, 404
        book = BookModel.find_by_id(id_book)
        if not book:
            return {'message': "Book with ['id': {}] not found".format(id_book)}, 404
        interface.books.append(book)
        interface.save_to_db()
        return {'message': "Book with ['id': {}] has successfully been added".format(id_book)}, 200

    def delete(self, id_interface, id_book):
        interface = InterfaceModel.find_by_id(id_interface)
        if not interface:
            return {'message': "Interface with ['id': {}] not found".format(id_interface)}, 404
        book = BookModel.find_by_id(id_book)
        if not book:
            return {'message': "Book with ['id': {}] not found".format(id_book)}, 404
        interface.books.remove(book)
        interface.save_to_db()
        return {'message': "Book with ['id': {}] has successfully been deleted".format(id_book)}, 200


class Interface(Resource):

    def get(self, idd):
        interface = InterfaceModel.find_by_id(idd)
        if interface:
            return interface.json(), 200
        return {'message': "Interface with ['id': {}] not found".format(idd)}, 404

    def post(self):
        data = self.__parse_request__()
        interface = InterfaceModel(data.get('front_type'), data.get('t2BookMode'), data.get('t1BackgndURL'),
                                   data.get('t1BackgndCOL'), data.get('t1LinkTo'), data.get('t1Tit'),
                                   data.get('t1Separator'), data.get('t1Sub'), data.get('t1Small'),
                                   data.get('t2RowTitle'), data.get('t2RowNumber'), data.get('t1TxtColor'))
        interface.save_to_db()
        return interface.json(), 200

    def put(self, idd):
        data = self.__parse_request__()
        exists = InterfaceModel.find_by_id(idd)
        if not exists:
            return {'message': "Interface with ['id': {}] not found".format(idd)}, 404

        exists.front_type = data.get('front_type')
        exists.t2BookMode = data.get('t2BookMode')
        exists.t1BackgndURL = data.get('t1BackgndURL')
        exists.t1BackgndCOL = data.get('t1BackgndCOL')
        exists.t1LinkTo = data.get('t1LinkTo')
        exists.t1Tit = data.get('t1Tit')
        exists.t1Separator = data.get('t1Separator')
        exists.t1Sub = data.get('t1Sub')
        exists.t1Small = data.get('t1Small')
        exists.t2RowTitle = data.get('t2RowTitle')
        exists.t2RowNumber = data.get('t2RowNumber')
        exists.t1TxtColor = data.get('t1TxtColor')

        exists.save_to_db()
        return exists.json(), 200

    def delete(self, idd):
        exists = InterfaceModel.find_by_id(idd)
        if not exists:
            return {'message': "Interface with ['id': {}] not found".format(idd)}, 404
        exists.delete_from_db()
        return {'message': "Interface with ['id': {}] has successfully been deleted".format(idd)}, 200

    def __parse_request__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('front_type', type=int, required=True,
                            help="Operation not valid: 'front_type' not provided")
        parser.add_argument('t2BookMode', type=int, required=True,
                            help="Operation not valid: 't2BookMode' not provided")
        parser.add_argument('t1BackgndURL', type=str, required=True,
                            help="Operation not valid: 't1BackgndURL' not provided")
        parser.add_argument('t1BackgndCOL', type=str, required=True,
                            help="Operation not valid: 't1BackgndCOL' not provided")
        parser.add_argument('t1LinkTo', type=str, required=True,
                            help="Operation not valid: 't1LinkTo' not provided")
        parser.add_argument('t1Tit', type=str, required=True, help="Operation not valid: 't1Tit' not provided")
        parser.add_argument('t1Separator', type=str, required=True,
                            help="Operation not valid: 't1Separator' not provided")
        parser.add_argument('t1Sub', type=str, required=True, help="Operation not valid: 't1Sub' not provided")
        parser.add_argument('t1Small', type=str, required=True, help="Operation not valid: 't1Small' not provided")
        parser.add_argument('t2RowTitle', type=str, required=True,
                            help="Operation not valid: 't2RowTitle' not provided")
        parser.add_argument('t2RowNumber', type=int, required=True,
                            help="Operation not valid: 't2RowNumber' not provided")
        parser.add_argument('t1TxtColor', type=str, required=True,
                            help="Operation not valid: 't1TxtColor' not provided")

        return parser.parse_args()


class ChangePositionBanner(Resource):

    def post(self, id_1, id_2):
        banner_top = InterfaceModel.find_by_id(id_1)
        banner_down = InterfaceModel.find_by_id(id_2)
        if not banner_top:
            return {'message': "Banner with ['id': {}] not found".format(id_1)}, 404
        if not banner_down:
            return {'message': "Banner with ['id': {}] not found".format(id_2)}, 404
        len_banners = len([a.json() for a in InterfaceModel.query.all()])
        id_aux = len_banners + 1
        banner_top.id = id_aux
        banner_top.save_to_db()
        banner_down.id = id_1
        banner_down.save_to_db()
        banner_top.id = id_2
        banner_top.save_to_db()
        return {'message': "Banners ID changed"}, 200