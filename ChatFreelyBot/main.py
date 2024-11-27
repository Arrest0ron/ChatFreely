from .database import connect, create_tables_if_not_exist
import asyncio
import warnings
from .bot import start_bot
import pytest

import os
env = os.getenv('ENV', 'default')

async def main():
    await connect()
    await create_tables_if_not_exist()
    await start_bot()
    
if __name__ == "__main__":
    if env=='default':
        asyncio.run(main())


    