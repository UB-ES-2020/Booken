from flask import Flask
from flask_restful import Resource, Api, reqparse

from models.address import AddressModel
from models.accounts import AccountModel


class Address(Resource):

    def get(self, account_id, id):
        account = AccountModel.find_by_id(account_id)
        address = AddressModel.find_by_id(id)

        if address is not None and account is not None:
            if address in account.addresses:
                return {'address': address.json()}, 200

            return {'message': "This account doesn't have an address with id [{}] ".format(id)}, 409

        elif address is None:
            return {'message': "Address with id [{}] Not found".format(id)}, 404
        else:
            return {'message': "Account with id [{}] Not found".format(id)}, 404

    def post(self, account_id, id=None):
        parser = reqparse.RequestParser()

        account = AccountModel.find_by_id(account_id)
        if (account == None):
            return {'message': "Account with id [{}] Not found".format(account_id)}, 404

        if (len(account.addresses) == 3):
            return {'message': "Account with id [{}] cannot have more addresses".format(account_id)}, 404

        # define the input parameters need and its type
        parser.add_argument('label_name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('surnames', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('street', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('number', type=int, required=True, help="This field cannot be left blanck")
        parser.add_argument('cp', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('city', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('province', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('telf', type=int, required=True, help="This field cannot be left blanck")

        data = parser.parse_args()
        address = AddressModel(data['label_name'], data['name'], data['surnames'], data['street'], data['number'],
                               data['cp'], data['city'], data['province'], data['telf'])

        account.addresses.append(address)

        try:
            account.save_to_db()
            return {"Message": "Address saved correctly"}, 200
        except:
            return {"Message": "Coudln't save changes"}, 500

    def put(self, account_id, id):
        account = AccountModel.find_by_id(account_id)
        address = AddressModel.find_by_id(id)

        if (address != None and account != None):
            if (address not in account.addresses):
                return {'message': "This account doesn't have an address with id [{}] ".format(id)}, 409

        elif (address == None):
            return {'message': "Address with id [{}] Not found".format(id)}, 404

        else:
            return {'message': "Account with id [{}] Not found".format(id)}, 404

        parser = reqparse.RequestParser()
        # define the input parameters need and its type
        parser.add_argument('label_name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('surnames', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('street', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('number', type=int, required=True, help="This field cannot be left blanck")
        parser.add_argument('cp', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('city', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('province', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('telf', type=int, required=True, help="This field cannot be left blanck")

        data = parser.parse_args()

        address.label_name = data['label_name']
        address.name = data['name']
        address.surnames = data['surnames']
        address.street = data['street']
        address.number = data['number']
        address.cp = data['cp']
        address.city = data['city']
        address.province = data['province']
        address.telf = data['telf']

        try:
            address.save_to_db()
            return {"Message": "Address saved correctly"}, 200
        except:
            return {"Message": "Coudln't save changes"}, 500

    def delete(self, account_id, id):
        account = AccountModel.find_by_id(account_id)
        address = AddressModel.find_by_id(id)

        if (address != None and account != None):
            if (address in account.addresses):
                try:
                    address.delete_from_db()
                    return {"Message": "Address deleted correctly"}, 200
                except:
                    return {"Message": "Coudln't save changes"}, 500

            else:
                return {'message': "This account doesn't have an address with id [{}] ".format(id)}, 409

        elif (address == None):
            return {'message': "Address with id [{}] Not found".format(id)}, 404

        else:
            return {'message': "Account with id [{}] Not found".format(id)}, 404


class AddressList(Resource):
    def get(self, account_id):
        account = AccountModel.find_by_id(account_id)
        addresses = []
        for a in account.addresses:
            addresses.append(a.json())
        return {"accounts_addresses": addresses}, 200
