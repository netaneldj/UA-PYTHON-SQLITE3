import sqlite3
import hashlib

# Conexion a la base de datos
conn = sqlite3.connect(':memory:')

# Cursor
cursor = conn.cursor()

# Creo la tabla
cursor.execute("""CREATE TABLE currency
                    (ID integer primary key, name text, symbol text)""")

# Guardo los cambios
conn.commit()

# Inserto datos de monedas
cursor.execute("INSERT INTO currency VALUES(1, 'Peso (ARG)', '$')")
cursor.execute("INSERT INTO currency VALUES(2, 'Dólar', 'U$S')")

# Revierto los cambios
#conn.rollback()

# Guardo los cambios
conn.commit()

# Consulto todas las monedas
query = "SELECT * FROM currency"

# Busco el resultado
currency = cursor.execute(query).fetchone()
print(currency)

print(cursor.fetchone())
print(cursor.fetchone())

# Busco el resultado
currencies = cursor.execute(query).fetchall()
print(currencies)

# Cierro la conexion con la base de datos
conn.close()

# Crear función
'''def md5sum(t):
    return hashlib.md5(t).hexdigest()


conn = sqlite3.connect(':memory:')
conn.create_function("md5", 1, md5sum)
cursor = conn.cursor()
cursor.execute("select md5(?)", (b"foo",))
print(cursor.fetchone()[0])
conn.close()

class MySum:
    def __init__(self):
        self.count = 0

    def step(self, value):
        self.count += value
    
    def finalize(self):
        return self.count


conn = sqlite3.connect(':memory:')
conn.create_function("mysum", 1, MySum)
# sqlite3.enable_callback_tracebacks(True) 
cursor = conn.cursor()
cursor.execute("create table test(i)")
cursor.execute("insert into test(i) values (1)")
cursor.execute("insert into test(i) values (2)")
cursor.execute("select mysum(i) from test")
print(cursor.fetchone()[0])
conn.close()'''