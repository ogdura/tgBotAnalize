import sqlite3

class DataBase:
    def __init__(self,dbFile):
        self.con=sqlite3.connect(dbFile)
        self.cursor=self.con.cursor()
    def get_spending(self,spend_id,user_id):
        self.cursor.execute(f"SELECT * FROM `spending` WHERE id = {spend_id} AND user_id = {user_id}")
        result = self.cursor.fetchall()
        return result
    def get_types(self,user_id):
        self.cursor.execute(f"SELECT * FROM `type_spend` WHERE user_id={user_id}")
        result = self.cursor.fetchall()
        return result
    def get_type_id(self,name, user_id):
        self.cursor.execute(f"SELECT id_type FROM `type_spend` WHERE user_id='{user_id}' AND name='{name}'")
        result = self.cursor.fetchall()
        return result
    def get_type_name(self,id,user_id):
        self.cursor.execute(f"SELECT name FROM `type_spend` WHERE id='{id}' AND user_id = '{user_id}'")
    def get_spend_type(self,id_type,user_id):
        self.cursor.execute(f"SELECT * FROM `spending` WHERE `id_type` = '{id_type}' AND `user_id` = '{user_id}'")
        result = self.cursor.fetchall()
        return result
    def get_user(self, user_id):
        self.cursor.execute(f"SELECT * FROM `users` WHERE id = {user_id}")
        result = self.cursor.fetchall()
        return result
    def add_user(self,user_id):
        self.cursor.execute(f"INSERT INTO `users` (`id`) VALUES ({user_id})")
        self.con.commit()
    def add_type(self,name,user_id):
        self.cursor.execute(f"INSERT INTO `type_spend` (`name`,`user_id`) VALUES ('{name}','{user_id}')")
        self.con.commit()
    def add_spend(self,name,price, user_id,type_id):
        self.cursor.execute(f"INSERT INTO `spending` (`name`, `price`, `user_id`, `id_type`) VALUES ('{name}', '{price}', '{user_id}', '{type_id}')")
        self.con.commit()
    def del_type(self,type_id,user_id):
        self.cursor.execute(f"DELETE FROM spending WHERE id_type = '{type_id}' AND user_id = '{user_id}'")
        self.cursor.execute(f"DELETE FROM `type_spend` WHERE id_type = '{type_id}' AND user_id = '{user_id}'")
        self.con.commit()
    def del_spend_choise(self, type_id,spend_id, user_id):
        self.cursor.execute(f"DELETE FROM spending WHERE id_type = '{type_id}' AND id = '{spend_id}' AND user_id = '{user_id}'")
        self.con.commit()
