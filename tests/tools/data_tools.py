from enum import Enum
from json import load

from tools.exceptions import DataError
from tools.json_tools import extract, update_json

file = 'bso_users.txt'


class Columns(Enum):
    ENV = 0
    USER = 1
    PSWD = 2
    COUNTRY = 4


class DataTools:

    def prepare_test_data(self, filename):
        with open(filename, 'r+') as f:
            data = set()
            reader = f.read().splitlines()
            for row in reader:
                row = row.split(';')
                data.add(row[Columns.ENV.value])

        test_data = dict()
        for env in data:
            test_data[env] = (self.prepare_test_data_per_env(filename=filename, env=env))

        return data

    def prepare_test_data_per_env(self, filename, env):
        with open(filename, 'r+') as f:
            data = []
            reader = f.read().splitlines()
            for row in reader:
                row = row.split(';')
                if env in row:
                    code = True if "Int" in row else False
                    if code:
                        base = self.prepare_base(is_customer=False, is_bso=True)
                    else:
                        base = self.prepare_base(is_crm=True if "crm" in row else False)

                    base = update_json(body=base, values={
                        '$.username': row[Columns.USER.value],
                        '$.password': row[Columns.PSWD.value],
                        '$.country': row[Columns.COUNTRY.value]
                    })
                    data.append(base)

        return data

    def prepare_base(self, is_customer=True, is_crm=False, is_bso=False):
        with open('model/bso_data_model.json', 'r+') as f:
            model = load(f)
        if is_customer:
            if is_crm:
                model = extract(body=model, path='$.customer')
                model = update_json(body=model, values={'IsCRM': True})
            else:
                model = extract(body=model, path='$.customer')
        elif is_bso:
            model = extract(body=model, path='$.bso')
        else:
            raise DataError('Must specify if the required data model is for external or internal user')
        return model

    def prepare_user_credential(self, user, pswd, is_bso=False, legal_entity=None):
        user, pswd, is_bso = ['DS1_AUT_PR_52@mailinator.com', 'TestS1cxg0#', True]

    def save_in_test_data_file(self):
        pass


u = DataTools()
u = u.prepare_test_data(filename=file)
print(file)
