import sqlite3
import uuid

DATABASE = 'test.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    print("Initializing..")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS userdata (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                workspace_id TEXT NOT NULL,
                workspace_name TEXT NOT NULL,
                role TEXT NOT NULL,
                login_count INTEGER DEFAULT 0,
                last_login DATETIME,
                isActive TEXT NOT NULL
            )
        ''')
        conn.commit()
        return print("initializing done..")


def insert_user():
    print("inserting users..")
    with get_db_connection() as conn:
        cursor = conn.cursor()

        userdata = [('khushi', '123', 'Outamation', 'admin'),
                    ('keya', 'k345', 'Omni', 'user'),
                    ('jinnie', 'j634t', 'BlackNight', 'user'),
                    ('ziva', 'jiva', 'Outamation', 'user')]

        for username, password, workspace_name, role in userdata:
            user_id = str(uuid.uuid4())
            workspace_id = str(uuid.uuid4())
            try:
                cursor.execute(
                    'INSERT INTO userdata (id, username, password, workspace_name, role, workspace_id,login_count,last_login,isActive) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (user_id, username, password, workspace_name, role,
                     workspace_id, 0, None, None))
            except sqlite3.IntegrityError:
                pass
        conn.commit()
        return print("inssertion done..")


def update_login_details(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE userdata 
            SET login_count = login_count + 1, 
                last_login = CURRENT_TIMESTAMP, 
                isActive = 'Active'
            WHERE username = ?''', (username, ))
        conn.commit()


def mark_user_inactive(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE userdata 
            SET isActive = 'Inactive'
            WHERE username = ?''', (username, ))
        conn.commit()


def dispay_users():
    print("displaying usrs..")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM userdata')

    rows = cursor.fetchall()

    for row in rows:
        print(
            f"Username: {row['username']}, Password: {row['password']}, Workspace: {row['workspace_name']}, Role: {row['role']}, ID: {row['id']}, worspace_id: {row['workspace_id']}, login_count: {row['login_count']},last_login: {row['last_login']},isActive: {row['isActive']}"
        )
    return


def user_exists(username):
    return get_user(username) is not None


# def get_user(username):
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM userdata WHERE username = ?', (username,))
#         return cursor.fetchone()
def get_user(username):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM userdata WHERE username = ?',
                           (username, ))
            user = cursor.fetchone()
            if user is None:
                return None
            return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None


def get_role_admin(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM userdata WHERE username = ? AND role = ?',
            (username, "admin"))
        return cursor.fetchone() is not None


def get_role_user(username):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM userdata WHERE username = ? AND role = ?',
            (username, "user"))
        return cursor.fetchone() is not None


def display_users_for_admin():
    print("displaying users for admin..")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, workspace_name, login_count, last_login, isActive 
            FROM userdata''')
        return cursor.fetchall()


# def change_role() :
#     with get_db_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("UPDATE userdata SET role = 'user' WHERE username = 'jinnie'")
#             conn.commit()

# def delete_table():
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute('DROP TABLE IF EXISTS userdata')
#         conn.commit()

# def add_column():
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute('''ALTER TABLE userdata
#                           ADD workspace_id TEXT;''')
#         cursor.execute('''ALTER TABLE userdata
#                           ADD login_count INTEGER DEFAULT 0;''')
#         cursor.execute('''ALTER TABLE userdata
#                           ADD last_login TEXT;''')
#         cursor.execute('''ALTER TABLE userdata
#                           ADD isActive INTEGER DEFAULT 0;''')
#         conn.commit()

if __name__ == '__main__':
    init_db()
    insert_user()
    # add_column()
    dispay_users()
    display_users_for_admin()
