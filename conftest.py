import pytest_asyncio
from ChatFreelyBot.database import grace_close, drop_tables, create_tables_if_not_exist, connect

@pytest_asyncio.fixture(loop_scope="function")
async def module_setup_teardown():
    await connect("TestUser")
    await drop_tables()
    await create_tables_if_not_exist()
    yield True
    await drop_tables()
    await grace_close()

