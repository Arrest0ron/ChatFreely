# test_module_1.py
import pytest
from ChatFreelyBot.database import log_user, fetch_user, drop_user
from ChatFreelyBot.user import User
import pytest_asyncio
from ChatFreelyBot.configure import get_credentials
from ChatFreelyBot.database import drop_tables, create_database_async_pool, create_tables_if_not_exist, connect, grace_close
import asyncio

# @pytest.mark.asyncio
# async def test_add_drop_user():
#     await connect("TestUser")
#     await create_tables_if_not_exist()
#     await log_user(12345)
#     usr = await fetch_user(12345)
#     assert usr.telegram_uid == 12345 and usr.reports == 0 and usr.total_connections == 0 and usr.rating == 0 and usr.user_status == 'normal'
#     await drop_user(12345)
#     usr = await fetch_user(12345)
#     assert usr is None
#     await drop_tables()
    


@pytest.mark.asyncio
async def test_add_drop_user_next(module_setup_teardown):
    
    await connect("TestUser")
    await asyncio.sleep(1)
    await grace_close()
    


@pytest.mark.asyncio
async def test_add_drop_user_next_2(module_setup_teardown):
    await connect("TestUser")
    await asyncio.sleep(1)
    await grace_close()
    
@pytest.mark.asyncio
async def test_add_drop_user_next_3(module_setup_teardown):
    await connect("TestUser")
    await asyncio.sleep(1)