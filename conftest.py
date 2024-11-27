# import asyncio
# import pytest
import pytest_asyncio
import warnings
# from ChatFreelyBot.configure import get_credentials
# from ChatFreelyBot.database import drop_tables, create_database_async_pool, create_tables_if_not_exist, connect


@pytest_asyncio.fixture
async def module_setup_teardown():
    # warnings.filterwarnings("ignore", message="*_call_connection_lost*")
    
#     """
#     Example fixture with async setup and teardown logic.
#     """
#     # Setup
#     await connect("TestUser")
#     await create_tables_if_not_exist()

    yield True
#     await drop_tables()

#     # Teardown

