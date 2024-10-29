import sqlite3

class DataBase:
    def __init__(self,db_file) -> None:
        self.conn = sqlite3.connect(db_file,check_same_thread=False)#Инициализация класса

    def search(self,searchid):#Проверка находится ли человек в базе
        self.cursor = self.conn.cursor()
        result = self.cursor.execute("SELECT id FROM users Where tg_id =?",(searchid,))
        if len(result.fetchall())>0:#Проверяем больше ли 0 длина массива, если да то человек в базе
            return True
        else:#Иначе
            return False

    def isblock(self,searchid):#Проверка находится ли человек в базе
        self.cursor = self.conn.cursor()
        result = self.cursor.execute("SELECT block FROM users Where tg_id =?",(searchid,)).fetchall()
        if result[0][0] == 1:
            return True
        else:#Иначе
            return False

    def isquery(self,searchid):#Проверка находится ли человек в базе
        self.cursor = self.conn.cursor()
        result = self.cursor.execute("SELECT query_unban FROM users Where tg_id =?",(searchid,)).fetchall()
        if result[0][0] == 1:
            return True
        else:#Иначе
            return False        

    def unban(self,searchid):
        self.cursor = self.conn.cursor()
        FIO = self.cursor.execute("UPDATE users set block = ?,query_unban = ? WHERE tg_id = ?",(0,0,searchid,)).fetchall()
        self.conn.commit()

    def insert_unban(self,id):
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE users set query_unban = ? where tg_id = ?",(1,id,)).fetchall()
        self.conn.commit()

    def block(self,userid):
        self.cursor = self.conn.cursor()
        result = self.cursor.execute("UPDATE users set block = 1 where tg_id = ?",(userid,)).fetchall()
        self.conn.commit()


    def isadmin(self,userid):#Проверяем администратор ли пользователь
        self.cursor = self.conn.cursor()
        result = self.cursor.execute("SELECT Role from user where tgid =?",(userid,))
        results = result.fetchall()
        if len(results)>0:
            for row in results:
                if row[0] == "Администратор":#Если участник администратор
                    return True
        else:
             return False

    def select_fio(self,id):
        self.cursor = self.conn.cursor()
        FIO = self.cursor.execute("Select fio from users where tg_id = ?",(id,)).fetchall()
        if str(FIO[0][0]) != "None":
            return True
        else:
            return False

    def select_group(self,id):
        self.cursor = self.conn.cursor()
        Group = self.cursor.execute("Select Group_col from users where tg_id = ?",(id,)).fetchall()
        if str(Group[0][0]) != "None":
            return True
        else:
            return False
    
    def select_collage(self,id):
        self.cursor = self.conn.cursor()
        Collage = self.cursor.execute("Select Collage from users where tg_id = ?",(id,)).fetchall()
        if str(Collage[0][0]) != "None":
            return True
        else:
            return False
    
    def fio_user(self,fio,id):
        self.cursor = self.conn.cursor()
        FIO = self.cursor.execute("UPDATE users set FIO = ? WHERE tg_id = ?",(fio,id,)).fetchall()
        self.conn.commit()

    def collage_user(self,fio,id):
        self.cursor = self.conn.cursor()
        FIO = self.cursor.execute("UPDATE users set collage = ? WHERE tg_id = ?",(fio,id,)).fetchall()
        self.conn.commit()

    def group_user(self,fio,id):
        self.cursor = self.conn.cursor()
        FIO = self.cursor.execute("UPDATE users set Group_col = ? WHERE tg_id = ?",(fio,id,)).fetchall()
        self.conn.commit()
        
    def newuser(self, userid):#Добавление пользователя
        self.cursor = self.conn.cursor()
        result = self.cursor.execute("INSERT INTO users ('tg_id',block,query_unban) VALUES(?,?,?)", (userid,0,0,))
        self.conn.commit()
    
    def get_fio(self, id):
        self.cursor = self.conn.cursor()
        fio = self.cursor.execute("Select fio from users where tg_id = ?",(id,)).fetchall()
        if str(fio[0][0]) != "None":
            return fio[0][0]
    
    def get_collage(self, id):
        self.cursor = self.conn.cursor()
        Collage = self.cursor.execute("Select collage from users where tg_id = ?",(id,)).fetchall()
        if str(Collage[0][0]) != "None":
            return Collage[0][0]
        else:
            return False
    
    def get_group(self,id):
        self.cursor = self.conn.cursor()
        Group = self.cursor.execute("Select Group_col from users where tg_id = ?",(id,)).fetchall()
        if str(Group[0][0]) != "None":
            return Group[0][0]
        else:
            return False
    
    