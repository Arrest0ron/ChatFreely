##
**ChatFreely** - это анонимный чат бот, написанный на python с применением асинхронного подхода
-
В разработке применялись:
- aiogram   ![aiogram 3+ ](https://img.shields.io/badge/-3%2B-red)
- aiomysql
- pytest_asyncio (для тестов)

Начало работы
-


Для начала работы необходимо скопировать репозиторий:

```
git clone https://github.com/Arrest0ron/ChatFreely.git
```
И установить все зависимости:
```
pip install -r requirements.txt
```
Установить mysql (в любой совместимой с оригиналом вариации) на вашу систему. Соглашайтесь на создание sudo юзера.
```
sudo apt get mysql 
```
В данном туториале будет использоваться mariadb.

```
sudo dnf install mariadb
```
Запустите ее, например, с помощью:
```
systemctl start mariadb
```
Создать юзера в установленной mysql можно только зайдя непосредственно в консоль, сделаем же это:
```
sudo mysql root -p
```
После этого введите пароль, заданный при установке для root юзера (либо стандартный)
Теперь можно инициировать бд:
```
CREATE DATABASE ChatFreely;
QUIT;
``` 
Добавим пользователя в config.json при помощи конфигуратора:

```python
python -m ChatFreely.configure
```
Вас попросит ввести имя (любой пользователь с правами на созданную бд), хост (ставьте localhost), пароль от пользователя и название бд - ChatFreely.
В том же меню добавьте токен вашего телеграм бота.
 Запустим:
```
python -m ChatFreely.main
```

