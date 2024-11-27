# import asyncio
import pytest
import pytest_asyncio
import warnings
# from ChatFreelyBot.configure import get_credentials
from ChatFreelyBot.database import grace_close,drop_tables, create_database_async_pool, create_tables_if_not_exist, connect, get_two_unique



@pytest_asyncio.fixture(loop_scope="function")
async def module_setup_teardown():
    
    
    
    
    await connect("TestUser")
    await drop_tables()
    await create_tables_if_not_exist()
    yield True
    await drop_tables()
    await grace_close()
    
    


