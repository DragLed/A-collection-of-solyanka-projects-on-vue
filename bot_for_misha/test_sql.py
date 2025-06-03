import sqlite3
i = 0
db = sqlite3.connect('item.db')

c = db.cursor()

c.execute("""CREATE TABLE product (
    marka text,
    name text,
    photo text,
    price integer
    

)""")
c.execute('INSERT INTO product VALUES ("Капот TRX H5",21075)')
c.execute('INSERT INTO product VALUES ("Решётка не стекло + полка/столик. Haval",15780)')
c.execute('INSERT INTO product VALUES ("Защита бампера H5",19715)')
c.execute('INSERT INTO product VALUES ("Видеорегестратор H5",6120)')
c.execute('INSERT INTO product VALUES ("Пороги алюминевый + пластик H5",22000)')
c.execute('INSERT INTO product VALUES ("Электробагажник H5",29500)')
c.execute('INSERT INTO product VALUES ("Накладки на бампер H9",8500)')
c.execute('INSERT INTO product VALUES ("Накладки на решотку+фары+подвестка матовый чёрный. H9",21000)')
c.execute('INSERT INTO product VALUES ("Доводчики задней двери H9",12500)')
c.execute('INSERT INTO product VALUES ("Лебёдка H9",35350)')

a = 1
def s (userPoz):
    c.execute(f"SELECT rowid, * FROM product WHERE rowid == {userPoz}")
    items = c.fetchall()
    return items
while a == 1:
    userPoz = int(input("Введите id:\t"))
    print(s(userPoz))










# while i < 10 :
#
#     print(c.fetchone()[2])
#     i = i + 1



db.commit()
db.close()