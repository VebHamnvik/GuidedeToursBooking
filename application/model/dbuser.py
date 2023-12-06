
from application.model.user import User


# Testet
def get_id_by_username(cur, username):
    sql = 'SELECT id FROM users WHERE username = ?'
    cur.execute(sql, (username,))

    user_object_id = cur.fetchone()

    if user_object_id:
        return user_object_id[0]

    # Returnerer None hvis den ikke finner noe i databasen
    return None

# Testet
def get_username_by_id(cur, id):
    sql = '''SELECT username FROM users WHERE id = ?'''
    cur.execute(sql, id)

    username = cur.fetchone()
    if username:
        return username[0]
    return None


# Testet
def get_rows_users(cur):

    sql = '''SELECT COUNT(id) FROM users'''
    cur.execute(sql)
    result = cur.fetchone()
    number_users = result[0]


    return number_users

# Testet
def get_user_by_id(cur, user_id):

    sql = 'SELECT * FROM users WHERE id = ?'
    cur.execute(sql, (user_id,))

    user_object = cur.fetchone()


    # Denne sjekker om brukeren finnes i databasen
    if user_object:
        # Henter ut informasjonen i databasen og lagrer den i variabel
        user_id, username, password, email, description, birthdate, gender, picture = user_object
        # Oppretter et user objekt med den infoen
        user = User(user_id, username, password, email, description, birthdate, gender, picture)

        return user
    # Returnerer None hvis den ikke finner noe i databasen
    return None

# Testet
def get_username_from_db(cur, username):
    sql = "SELECT username FROM users WHERE username = ?"
    cur.execute(sql, (username,))
    user_row = cur.fetchone()

    return user_row


# Testet
def get_password_from_db(cur, username):
    sql = "SELECT password FROM users WHERE username = ?"
    cur.execute(sql, (username,))
    user_row = cur.fetchone()
    return user_row

#Testet
def insert_user_info_to_db(
    conn, cur, username, password, email, description=None, birthdate=None, gender=None):
    sql = """ INSERT INTO users(username,password,email, description, birthdate, gender)
                                                              VALUES(?,?,?, ?, ?, ?) """
    sql_user = (username, password, email, description, birthdate, gender)
    # Legges inn i databasen med brukernavn, passord, email. ID blir automatisk opprettet
    cur.execute(sql, sql_user)
    conn.commit()

#Testet
def get_row_from_users(cur):
    sql = '''SELECT * FROM users'''
    cur.execute(sql)
    row = cur.fetchone()

    return row

