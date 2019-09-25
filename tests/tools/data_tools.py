import csv
from copy import deepcopy
from enum import Enum
from json import load

from tools.exceptions import DataError
from tools.json_tools import extract, update_json


# region Colums configuration for test data files.
class ColumnsUser(Enum):
    ENV = 0
    CRM = 1
    USER = 2
    PSWD = 3
    COUNTRY = 5


class ColumnsAddress(Enum):
    COUNTRY = 0
    CRM = 1
    DETAILS = 2
    CITY = 3
    REGION = 4
    BCODE = 5
    CROSS1 = 6
    CROSS2 = 7
    DISTR = 8
    DIFFCITY = 9
    SNAME = 10
    SNUM = 11
    ZIPCODE = 12
    LAT = 13
    LONG = 14
    SDESC = 15


#endregion


class DataTools:

    def __init__(self):
        self.link_users = '../data_test/test_users.csv'
        self._link_address = '../data_test/test_addresses.csv'

    def prepare_test_data(self, filename):
        with open(filename, 'r+') as csvfile:
            data = set()
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                data.add(row[ColumnsUser.ENV.value])

        test_data = dict()
        for env in data:
            test_data[env.lower()] = (self.prepare_test_data_per_env(filename=filename, env=env))

        return test_data

    def prepare_test_data_per_env(self, filename, env):
        with open(filename, 'r+') as csvfile:
            data = []
            reader = csv.reader(csvfile, delimeter=';')
            for row in reader:
                if env in row:
                    code = True if "Int" in row else False
                    if code:
                        base = self.prepare_test_data_base(is_customer=False, is_bso=True)
                    else:
                        base = self.prepare_test_data_base(is_crm=True if "CRM" in row else False)
                        base = update_json(body=base, values={'$.country': row[ColumnsUser.COUNTRY.value]})
                        base = self.prepare_base_data_address(filename=self._link_address, base=base)

                    base = update_json(body=base, values={
                        '$.username': row[ColumnsUser.USER.value],
                        '$.password': row[ColumnsUser.PSWD.value]
                    })
                    data.append(base)

        return data

    def prepare_test_data_base(self, is_customer=True, is_crm=False, is_bso=False):
        with open('model/users.json', 'r+') as f:
            model = load(f)
        if is_customer:
            if is_crm:
                model = deepcopy(extract(body=model, path='$.customer'))
                model = update_json(body=model, values={'IsCRM': True})
            else:
                model = deepcopy(extract(body=model, path='$.customer'))
        elif is_bso:
            model = deepcopy(extract(body=model, path='$.bso'))
        else:
            raise DataError('Must specify if the required data model is for external or internal user')
        return model

    def prepare_base_data_address(self, filename, base):
        is_crm = extract(body=base, path='$.IsCRM')
        country = extract(body=base, path='$.country')

        with open(filename, 'r+', encoding='UTF-8') as f:
            reader = f.read().splitlines()
            for row in reader:
                row = row.split(';')
                try:
                    if is_crm and 'CRM' in row and country in row:
                        data = row
                        break
                    elif country in row and 'CRM' not in row and not is_crm:
                        data = row
                        break
                    else:
                        raise DataError('Could not find proper test data for country')
                except DataError:
                    continue

        base = update_json(body=base, values={
            '$..address..additionalDetails': data[ColumnsAddress.DETAILS.value],
            '$..address..cityDesc': data[ColumnsAddress.CITY.value],
            '$..address..regionId': data[ColumnsAddress.REGION.value],
            '$..address..buildingCode': data[ColumnsAddress.BCODE.value],
            '$..address..crossStreetName1': data[ColumnsAddress.CROSS1.value],
            '$..address..crossStreetName2': data[ColumnsAddress.CROSS2.value],
            '$..address..district': data[ColumnsAddress.DISTR.value],
            '$..address..differentCity': data[ColumnsAddress.DIFFCITY.value],
            '$..address..countryCode': country,
            '$..address..streetName': data[ColumnsAddress.SNAME.value],
            '$..address..domicileNum': data[ColumnsAddress.SNUM.value],
            '$..address..postalCode': data[ColumnsAddress.ZIPCODE.value],
            '$..address..geoPlace.latitude': data[ColumnsAddress.LAT.value],
            '$..address..geoPlace.longitude': data[ColumnsAddress.LONG.value],
            '$..address..settlementDesc': data[ColumnsAddress.SDESC.value]
        })
        return base

    def save_in_test_data_file(self):
        pass