import aiomysql
import UserManager
from aiogram.types import Message
from user import SearchUser, User
import warnings

async def create_database_async_pool():
    credentials = UserManager.get_credentials("ChatFreelyAdmin")
    if not credentials:
        print("Incorrect credentials")
        return None
    try: 
        global pool
        pool = await aiomysql.create_pool(
            user=credentials["username"],
            db=credentials["database"],
            password=credentials["password"],
            host=credentials["host"],
            minsize=1,
            maxsize=10,
            autocommit = True,
            port=3306
        )
    except aiomysql.Error as err:
        print("Error:", err.args)
        return None
    
async def connect():
    await create_database_async_pool()
    global pool
    if pool is None:
        raise BaseException("Could not resolve mysql database connection. Maybe check credentials/start db.")

async def create_tables_if_not_exist():
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    telegram_uid BIGINT PRIMARY KEY NOT NULL,
                    user_status ENUM('normal', 'connected', 'search', 'banned') DEFAULT 'normal',
                    INDEX (user_status),
                    rating INT DEFAULT 0,
                    registration TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_connections INT DEFAULT 0,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    last_connected BIGINT NULL DEFAULT NULL,
                    reports INT DEFAULT 0
                );
                """)
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS search (
                    telegram_uid BIGINT PRIMARY KEY NOT NULL,
                    rating INT DEFAULT 0,
                    FOREIGN KEY (telegram_uid) REFERENCES users(telegram_uid) ON DELETE CASCADE
                );
                """)
            
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS connections (
                    telegram_uid_1 BIGINT PRIMARY KEY NOT NULL,
                    FOREIGN KEY (telegram_uid_1) REFERENCES users(telegram_uid) ON DELETE CASCADE, 
                    telegram_uid_2 BIGINT NOT NULL,
                    FOREIGN KEY (telegram_uid_2) REFERENCES users(telegram_uid) ON DELETE CASCADE, 
                    UNIQUE INDEX T_UID_2(telegram_uid_2)
                );
                """)
            
async def log_message(message : Message):
    # print(f"Message {context} logged.")   
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                INSERT INTO users 
                (
                    telegram_uid
                )
                VALUES (%s)
                ON DUPLICATE KEY UPDATE
                last_update = CURRENT_TIMESTAMP
                """, (message.from_user.id,))
            await conn.commit()
         
async def add_to_search(user : User):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                REPLACE INTO search
                (
                    telegram_uid,
                    rating
                )
                VALUES (%s,%s);
                """, (user.telegram_uid, user.rating))
            await conn.commit()
            print("User added!")
                      
async def drop_from_search(telegram_uid):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor

            await cursor.execute(
                """
                DELETE FROM search
                WHERE telegram_uid = %s
                """, (telegram_uid, ))
            await conn.commit()

async def add_to_connections(recipient, counterpart):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                REPLACE INTO connections
                (
                    telegram_uid_1,
                    telegram_uid_2
                )
                VALUES (%s,%s)
                ;
                """, (recipient, counterpart))
            await conn.commit()
                      
async def drop_from_connections(telegram_uid):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                DELETE FROM connections
                WHERE telegram_uid_1 = %s
                OR telegram_uid_2 = %s
                """, (telegram_uid, telegram_uid))
            await conn.commit()

async def update_status(uid : str, status : str):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                UPDATE users
                SET user_status = %s
                WHERE telegram_uid = %s
                """, (status,uid))
            await conn.commit()
         
async def after_dialogue(uid : str, uid2 : str):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                UPDATE users
                SET user_status = 'normal', total_connections = total_connections + 1, last_connected = %s
                WHERE telegram_uid = %s;
                """, (uid, uid2))
            await cursor.execute(
                """
                UPDATE users
                SET user_status = 'normal', total_connections = total_connections + 1, last_connected = %s
                WHERE telegram_uid = %s;
                """, (uid2, uid))
            await conn.commit()
        
async def fetch_user(user_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                SELECT * FROM users WHERE telegram_uid = %s
                """, (user_id,))
            if cursor.rowcount==0:
                warnings.warn(f"An attempt to fetch unknown user: {user_id}")
                return None
            data = await cursor.fetchone()
            return User(data)
    
async def get_connected_user(telegram_uid : str):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM connections WHERE telegram_uid_1 = %s OR telegram_uid_2 = %s;
                """, (telegram_uid, telegram_uid))
            if cursor.rowcount > 0:
                data = await cursor.fetchone()
                if data[0]==telegram_uid:
                    return data[1]
                return data[0]
            else:
                print(f"No user {telegram_uid} in connections.")
                return None

async def is_in_search(telegram_uid):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            
            cursor: aiomysql.Cursor
            
            await cursor.execute(
                """
                SELECT * FROM search
                WHERE telegram_uid = %s
                """, (telegram_uid,))
            
            # await conn.commit()
            if cursor.rowcount > 0:
                res = True
            else:
                res = False
            # await conn.commit()
                
            return res

async def get_counterpart(telegram_uid : str):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            
            cursor: aiomysql.Cursor
            user = await fetch_user(telegram_uid)
            user : User
            await cursor.execute(
                """
                SELECT * FROM search
                WHERE telegram_uid != %s
                ORDER BY ABS(rating-%s);
                """, (user.telegram_uid, user.rating ))
            if cursor.rowcount > 0:
                data = await cursor.fetchone()
                return SearchUser(data)
            else:
                print(f"Match for {user.telegram_uid, user.rating } Not Found.")
                return None
            
async def add_rating(telegram_uid, voter_uid):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor : aiomysql.Cursor
            await cursor.execute("""
                           UPDATE users
                           SET rating = rating + 1
                           WHERE telegram_uid = %s;
                           """, (telegram_uid,))
            await cursor.execute("""
                           UPDATE users
                           SET last_connected = NULL
                           WHERE telegram_uid = %s;
                           """, (voter_uid,))
            await conn.commit()
            
async def sub_rating(telegram_uid, voter_uid):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor : aiomysql.Cursor
            await cursor.execute("""
                           UPDATE users
                           SET rating = rating - 1
                           WHERE telegram_uid = %s;
                           """, (telegram_uid,))
            await cursor.execute("""
                           UPDATE users
                           SET last_connected = NULL
                           WHERE telegram_uid = %s;
                           """, (voter_uid,))
            await conn.commit()
            
async def add_report(telegram_uid, voter_uid):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor : aiomysql.Cursor
            await cursor.execute("""
                           UPDATE users
                           SET reports = reports + 1
                           WHERE telegram_uid = %s;
                           """, (telegram_uid,))
            await cursor.execute("""
                           UPDATE users
                           SET last_connected = NULL
                           WHERE telegram_uid = %s;
                           """, (voter_uid,))
            await conn.commit()



