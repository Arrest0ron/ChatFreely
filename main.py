from database import connect, create_tables_if_not_exist
import asyncio
import warnings
from bot import start_bot

DEBUG = False

async def main():
    await connect()
    await create_tables_if_not_exist()
    await start_bot()
    
if __name__ == "__main__":
    if not DEBUG:
        warnings.filterwarnings("ignore", message="Table '.*' already exists")
    asyncio.run(main())