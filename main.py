import psycopg2


try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='admin',
        dbname='balhash_bank'
    )
    conn.autocommit = True
    print('Connection is success!')
except Exception as e:
    print(e)
    print("[ERROR] CONNECTION ERROR!")

with conn.cursor() as cur:
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(200) NOT NULL,
            last_name VARCHAR(200) NOT NULL,
            date_of_birth DATE NOT NULL,
            iin VARCHAR(12) UNIQUE NOT NULL CHECK(LENGTH(iin)=12),
            phone_number 
                VARCHAR(10) 
                UNIQUE 
                NOT NULL 
                CHECK(LENGTH(phone_number)=10)
        );
        CREATE TABLE IF NOT EXISTS accounts(
            id SERIAL PRIMARY KEY,
            number 
                VARCHAR(20) 
                UNIQUE 
                NOT NULL 
                CHECK(LENGTH(number)=20),
            owner_id
                INTEGER
                NOT NULL
                UNIQUE
                REFERENCES users(id),
            balance
                DECIMAL
                CHECK(balance > -3000)
                DEFAULT(0),
            type
                VARCHAR(4)
        );
        CREATE TABLE IF NOT EXISTS cards(
            id SERIAL PRIMARY KEY,
            number 
                VARCHAR(16) 
                UNIQUE 
                NOT NULL 
                CHECK(LENGTH(number)=16),
            account_id
                INTEGER
                NOT NULL
                REFERENCES accounts(id),
            cvv
                VARCHAR(3) 
                UNIQUE 
                NOT NULL 
                CHECK(LENGTH(cvv)=3),
            date_end 
                DATE 
                DEFAULT(NOW() + INTERVAL '3 YEAR'),
            is_active
                BOOLEAN
                DEFAULT('true'),
            pin
                VARCHAR(4)
                NOT NULL 
                CHECK(LENGTH(pin)=4)
        );
        CREATE TABLE IF NOT EXISTS organization(
            id SERIAL PRIMARY KEY,
            name 
                VARCHAR(100) 
                NOT NULL 
                UNIQUE,
            phone_numbers
                VARCHAR(16) ARRAY 
                NOT NULL
        );
        '''
    )
