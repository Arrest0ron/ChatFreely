# test_module_1.py
import pytest
import warnings
from ChatFreelyBot.database import (
    log_user, fetch_user, 
    drop_user, get_two_unique,
    has_data, add_to_search, 
    add_to_connections, drop_tables,
    drop_from_search, get_counterpart)


@pytest.mark.usefixtures("module_setup_teardown")
class TestClass:
    @pytest.mark.asyncio
    async def test_add_drop_user(module_setup_teardown):   # тест добавления и удаления пользователя
        test_uids = await get_two_unique()
        test_uid = test_uids[0]
        await log_user(test_uid)
        usr = await fetch_user(test_uid)
        assert usr.telegram_uid == test_uid \
            and usr.reports == 0 \
            and usr.total_connections == 0 \
            and usr.rating == 0 \
            and usr.user_status == 'normal'    # пользователь создается нормальным
        await drop_user(test_uid)
        usr = await fetch_user(test_uid)
        assert usr is None    # пользователь действительно удаляется

    @pytest.mark.asyncio      # продвинутый тест множественного добавления и удаления
    async def test_add_drop_user_two(module_setup_teardown):
        test_uids = await get_two_unique()
        test_uid = test_uids[0]
        await log_user(test_uid)
        await log_user(test_uid)
        usr = await fetch_user(test_uid)
        assert usr is not None                             # идентичное создание
        usr1 = await fetch_user(test_uid)
        usr2 = await fetch_user(test_uid)
        assert (usr1.registration == usr2.registration)    # идентичное получение
        await drop_user(test_uid)
        usr = await fetch_user(test_uid)
        assert usr is None                                 # нет двух записей
        
    @pytest.mark.asyncio
    async def test_is_empty(module_setup_teardown):
        res = await has_data()
        for value in res.values():
            assert not value
        test_uids = await get_two_unique()
        for uid in test_uids:
            await log_user(uid)
            await add_to_search(await fetch_user(uid))
        await add_to_connections(test_uids[0], test_uids[1])
        res = await has_data()
        for value in res.values():
            assert value

    @pytest.mark.asyncio
    async def test_drop_tables(module_setup_teardown):          # тест очистки таблиц
        warnings.filterwarnings(message="Dropping tables from the empty database", action='ignore')
        code = await drop_tables()
        assert code

    @pytest.mark.asyncio
    async def test_add_drop_user_multiple(module_setup_teardown):          # нагрузочный тест
        for entry in range(125):
            await log_user(entry)
            await drop_user(entry)
        res = await has_data()
        for value in res.values():
            assert not value
            
    @pytest.mark.asyncio
    async def test_add_drop_search(module_setup_teardown):          # тест корретного соединения
        test_uids = await get_two_unique()
        for uid in test_uids:
            await log_user(uid)
            usr = await fetch_user(uid)
            await add_to_search(usr)

        uid1_counterpart = await get_counterpart(test_uids[0])
        assert (uid1_counterpart.telegram_uid == test_uids[1])

        uid2_counterpart = await get_counterpart(test_uids[1])
        assert (uid2_counterpart.telegram_uid == test_uids[0])    # верное соединение
        for uid in test_uids:
            await drop_from_search(uid)
            await drop_user(uid)     # убираем из бд
        res = await has_data()
        for value in res.values():
            assert not value         # очищение работает верно
