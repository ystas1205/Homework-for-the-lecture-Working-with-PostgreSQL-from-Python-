import psycopg2


def table_deletion(cursor):
    cur.execute("""
                DROP TABLE phone;
                DROP TABLE clients;
                """)


def create_db(cursor):
    # Создание таблиц
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(45) NOT NULL,
            last_name VARCHAR(45) NOT NULL,
            email VARCHAR(100) UNIQUE           
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            phone_number VARCHAR(20) UNIQUE NOT NULL,
            clients_id INTEGER NOT NULL REFERENCES clients(id)		
        );
        """)


def add_client(cursor, first_name, last_name, email, phones=None):
    # Добавление клиентов
    cur.execute("""
        INSERT INTO clients(first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING id,first_name, last_name, email;
        """, (first_name, last_name, email))
    return cur.fetchone()


def phone_extension(cursor, phone_number, clients_id):
    # Добавление номера телефона
    cur.execute("""
        INSERT INTO phone(phone_number,clients_id)
        VALUES (%s, %s) RETURNING id,phone_number,clients_id;  
            """, (phone_number, clients_id))
    return cur.fetchone()


def customer_update(cursor, client_id, last_name=None,
                    first_name=None, email=None, phone=None):
    # Обновление данных клиента
    cur.execute("""       
                SELECT * FROM clients WHERE id=%s;
                """, (client_id))
    data_clients = cur.fetchone()
    if first_name is None:
        first_name = data_clients[1]
    if last_name is None:
        last_name = data_clients[2]
    if email is None:
        email = data_clients[3]
    cur.execute("""
        UPDATE clients SET first_name=%s,last_name=%s,email=%s
        WHERE id=%s
        """, (first_name, last_name, email, client_id))
    return True


def deleting_a_phone(cursor, client_id, phone_number):
    # Удаление телефона клиента
    cur.execute("""       
                SELECT * FROM clients WHERE id=%s         
                """, (client_id))
    data_clients = cur.fetchone()
    cur.execute("""       
                SELECT * FROM phone       
                """)
    data_phone = cur.fetchall()
    for data_phones in data_phone:
        if data_clients[0] == data_phones[2] \
                and phone_number == data_phones[1]:
            cur.execute("""
                        DELETE FROM phone WHERE id=%s;
                        """, (data_phones[0],))
            print(f"Номер телефона {phone_number} клиента {data_clients[1]}"
                  f" {data_clients[2]} удален. ")
    return data_clients


def deleting_a_client(cursor, client_id):
    # Удаление клиента
    cur.execute("""       
                SELECT * FROM clients WHERE id=%s           
                """, (client_id))
    data_clients = cur.fetchone()
    cur.execute("""       
                SELECT * FROM phone       
                """)
    data_phone = cur.fetchall()
    for data_phones in data_phone:
        if data_clients[0] == data_phones[2]:
            cur.execute("""
                        DELETE FROM phone WHERE id=%s;
                        """, (data_phones[0],))
    cur.execute("""
                DELETE FROM clients WHERE id=%s;
                """, (data_clients[0],))
    print(f"Клиент {data_clients[1]} {data_clients[2]} удален")
    return data_clients


def client_search(cur, first_name=None, last_name=None, email=None,
                  phone=None):
    # Поиск клиента
    cur.execute("""
                SELECT * FROM clients 
                """)
    data_clients = cur.fetchall()
    cur.execute("""
                SELECT * FROM phone 
                """)
    data_phone = cur.fetchall()
    list_clients = []
    for data_client in data_clients:
        if first_name == data_client[1] or last_name == data_client[2] \
                or email == data_client[3]:
            cur.execute("""
                        SELECT * FROM clients  WHERE id=%s;
                        """, (data_client[0],))
            data = cur.fetchone()
            list_clients.append(data)
    for data_phones in data_phone:
        if phone == data_phones[1]:
            cur.execute("""
                        SELECT * FROM clients  WHERE id=%s;
                        """, (data_phones[2],))
            data = cur.fetchone()
            list_clients.append(data)
    return list_clients


if __name__ == '__main__':
    with psycopg2.connect(database="client_information",
                          user="postgres", password="8490866") as conn:
        with conn.cursor() as cur:
            # Удаление базы данных
            table_deletion(cur)

            # Создание таблиц
            # create_db(cur)

            # Добавление клиентов
            # add_client(cur, 'Sergei', 'Ivanov', 'vganesh@mail.ru')
            # add_client(cur, 'Alexander', 'Petrov', 'alex@mail.ru')
            # add_client(cur, 'Dmitriy', 'Losev', 'sch@mail.ru')

            # Добавление телефона
            # phone_extension(cur, '89186542398', '1')
            # phone_extension(cur, '89222653326', '1')
            # phone_extension(cur, '89222443333', '3')

            # Обновление данных о клиенте
            # customer_update(cur,'2',email='avanil@mail.ru')

            # Удаление телефона клиента
            # deleting_a_phone(cur, '1', '89222653326')

            # Удаление клиента
            # deleting_a_client(cur, '3')

            # Поиск клиента
            # print(client_search(cur,phone='89186542398'))
