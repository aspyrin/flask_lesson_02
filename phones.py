from db_manager import Db


class Contact:
    def __init__(self):
        self.name = ''
        self.phone = ''
        self.db = Db()

    def __del__(self):
        del self.db

    def create(self, name: str, phone: str):
        try:
            sql = f'''
            INSERT INTO phones (ContactName, Phone)
            VALUES ('{name}', '{phone}');
            '''
            self.db.cur.execute(sql)
            self.db.conn.commit()
        finally:
            del self.db

    def delete(self, phone: str):
        try:
            sql = f'''
            DELETE FROM phones WHERE Phone = '{phone}';
            '''
            self.db.cur.execute(sql)
            self.db.conn.commit()
        finally:
            del self.db

    def update(self, phone: str, new_name: str == 'none', new_phone: str == 'none'):
        try:
            if new_name != 'none' and new_phone != 'none':
                sql = f'''
                UPDATE phones
                SET ContactName = '{new_name}', Phone = '{new_phone}'
                WHERE Phone == '{phone}';
                '''
            elif new_name != 'none' and new_phone == 'none':
                sql = f'''
                UPDATE phones
                SET ContactName = '{new_name}'
                WHERE Phone == '{phone}';
                '''
            elif new_name == 'none' and new_phone != 'none':
                sql = f'''
                UPDATE phones
                SET Phone = '{new_phone}'
                WHERE Phone == '{phone}';
                '''
            self.db.cur.execute(sql)
            self.db.conn.commit()
        finally:
            del self.db

    @staticmethod
    def read(_id: int = 0, _name: str = '', _phone: str = ''):
        sql = ''
        try:
            # if no parameters return all recordset
            if _id == 0 and _name == '' and _phone == '':
                sql = f'''
                SELECT * FROM phones;
                '''
            # if only one parameter return filtered recordset
            elif _id == 0 and _name == '' and _phone != '':
                sql = f'''
                SELECT * FROM phones WHERE Phone Like '%{_phone}%';
                '''
            elif _id == 0 and _name != '' and _phone == '':
                sql = f'''
                SELECT * FROM phones WHERE ContactName Like '%{_name}%';
                '''
            elif _id != 0 and _name == '' and _phone == '':
                sql = f'''
                SELECT * FROM phones WHERE Id == '{_id}';
                '''
            # if two parameters return filtered recordset
            elif _id == 0 and _name != '' and _phone != '':
                sql = f'''
                SELECT * FROM phones 
                WHERE Phone Like '%{_phone}%' AND ContactName Like '%{_name}%';
                '''
            db = Db()
            print(sql)
            db.cur.execute(sql)
            dataset = db.cur.fetchall()
            return dataset
        finally:
            del db

    @staticmethod
    def validate_phone(phone: str) -> dict:
        """
        function validate phone number string
        :phone valid formate: 0676974395
        :return: dictionary {"is_valid": True/False, "msg": "successful/error desc"}
        """

        correct_number_of_characters = 10
        allowed_mobile_operators = (
            '067', '068', '097', '098', '039',
            '050', '066', '095', '099',
            '063', '093', '073', '091', '092', '094',
            '070', '080', '090'
        )

        result = {"is_valid": True, "msg": "successful"}

        operator_code = str(phone[:3])

        if len(phone) != correct_number_of_characters:
            result["is_valid"] = False
            result["msg"] = f"Phone number mast have {correct_number_of_characters} characters (example: 0676974395)!"

        elif not phone.isnumeric():
            result["is_valid"] = False
            result["msg"] = "Phone number mast have only digit symbols!"

        elif operator_code not in allowed_mobile_operators:
            result["is_valid"] = False
            result["msg"] = f"Unknown mobile provider code: {operator_code}, " \
                            f"use one of this codes: {allowed_mobile_operators}"

        return result

    @staticmethod
    def validate_name(name: str) -> dict:
        """
        function validate name of contact
        :return: dictionary {"is_valid": True/False, "msg": "successful/error desc"}
        """

        min_number_of_characters = 3
        max_number_of_characters = 20

        result = {"is_valid": True, "msg": "successful"}

        if len(name) < min_number_of_characters:
            result["is_valid"] = False
            result["msg"] = f"Contact name mast have not less than {min_number_of_characters} characters!"

        elif len(name) > max_number_of_characters:
            result["is_valid"] = False
            result["msg"] = f"Contact name mast have not more than {max_number_of_characters} characters!"

        return result


    @staticmethod
    def phone_is_exists(phone: str) -> bool:
        """
        function check phone in db
        :return: bool value True/False
        """
        result = False
        try:
            sql = f'''
                    SELECT * FROM phones 
                    WHERE Phone == '{phone}';
                '''
            db = Db()
            db.cur.execute(sql)
            if len(db.cur.fetchall()) == 1:
                result = True
            else:
                result = False
        finally:
            del db
            return result
