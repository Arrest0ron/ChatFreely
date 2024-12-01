import os
env = os.getenv('ENV', 'default')


async def main():
    await connect()
    await create_tables_if_not_exist()
    await start_bot()
    
if __name__ == "__main__":    
    if env == 'default':
        from .database import connect, create_tables_if_not_exist
        import asyncio
        from .bot import start_bot
        asyncio.run(main())
    if env == 'test':
        import pytest
        pytest.main()
        
