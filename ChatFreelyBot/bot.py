from .configure import get_key
from aiogram.utils.keyboard import  InlineKeyboardBuilder
from aiogram import Router, Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.methods import *
from aiogram.types import Message, CallbackQuery
from .keyboards import *
from .database import *


API_TOKEN = get_key()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)
async def start_bot():
    await dp.start_polling(bot)

@router.callback_query(F.data == 'profile')
@router.message(Command("profile"))
async def profile(call):
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    data = await fetch_user(call.from_user.id)
    answer = f"""
Давай рассмотрим твой профиль:
Ваш рейтинг: {data.rating}
Всего диалогов: {data.total_connections}
Регистрация: {data.registration}
    """
    builder = InlineKeyboardBuilder()
    builder.add(*inline_to_menu_buttons_list)
    markup = builder.as_markup()
    await bot.send_message(chat_id = call.from_user.id, text= answer, reply_markup=markup)
   
@router.message(Command("start"))
async def start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(*inline_to_menu_buttons_list)
    markup = builder.as_markup()
    await log_user(message.from_user.id)
    await message.answer(f"Привет, {message.from_user.username}! Используй /menu, чтобы попасть в основное меню.", reply_markup=markup)

@router.callback_query(F.data == 'stop')
@router.message(Command("stop"))
async def stop_search(call):
    print("Stop called.")
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    is_searching = await is_in_search(call.from_user.id)
    if not is_searching:
        print(is_searching)
        return await menu(call)
    
    await drop_from_search(call.from_user.id)
    await bot.send_message(chat_id = call.from_user.id, text= f"Вы остановили поиск собеседника!")
    await update_status(call.from_user.id, "normal")
    return await menu(call)

@router.callback_query(F.data == 'quit')
@router.message(Command("quit"))
async def quit_dialogue(call):
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    builder = InlineKeyboardBuilder()
    builder.add(*inline_dialogue_end_buttons_list)
    markup = builder.as_markup()
    counterpart = await get_connected_user(call.from_user.id)
    if counterpart is None:
        return await bot.send_message(chat_id = call.from_user.id, text= f"Вы не находитесь в диалоге. Используйте /menu, чтобы попасть в меню, или /search, чтобы найти собеседника.", reply_markup=markup)
    await bot.send_message(chat_id = call.from_user.id, text= f"Вы остановили диалог с вашим собеседником. Используйте /search, чтобы найти нового собеседника, или /menu для возврата в меню.", reply_markup=markup)
    await drop_from_connections(call.from_user.id)
    await bot.send_message(chat_id = counterpart, text= f"Ваш собеседник остановил диалог. Используйте /search, чтобы найти нового собеседника, или /menu для возврата в меню.", reply_markup=markup)
    await after_dialogue(call.from_user.id,counterpart)
    builder = InlineKeyboardBuilder()
    builder.add(*inline_rate_buttons_list)
    builder.adjust(*[2,1])
    markup = builder.as_markup()
    await bot.send_message(chat_id=counterpart, text="Как вы оцените вашего последнего собеседника?",reply_markup=markup)
    await bot.send_message(chat_id=call.from_user.id, text="Как вы оцените вашего последнего собеседника?",reply_markup=markup)

@router.callback_query(F.data == 'decrease_rating')
async def decrease_rating(call: CallbackQuery):
    usr = await fetch_user(call.from_user.id)
    if usr.last_connected is not None:
        await call.message.edit_text(text="Спасибо за отзыв!")
        await sub_rating(usr.last_connected, usr.telegram_uid)
    else:
        await call.message.edit_text(text="Устаревший отзыв.")
    
@router.callback_query(F.data == 'increase_rating')
async def increase_rating(call: CallbackQuery):
    usr = await fetch_user(call.from_user.id)
    if usr.last_connected is not None:
        await call.message.edit_text(text="Спасибо за отзыв!")
        await add_rating(usr.last_connected, usr.telegram_uid)
    else:
        await call.message.edit_text(text="Устаревший отзыв.")

@router.callback_query(F.data == 'report')
async def report(call: CallbackQuery):
    usr = await fetch_user(call.from_user.id)
    
    if usr.last_connected is not None:
        await call.message.edit_text(text="Спасибо за отзыв!")
        await add_report(usr.last_connected, usr.telegram_uid)
    else:
        await call.message.edit_text(text="Устаревший отзыв.")
    
@router.callback_query(F.data == 'appeal')
async def report(call: CallbackQuery): 
    await call.message.edit_text(text="Отправьте заказным письмом заявку на разблокировку с полной информацией о себе по данному адресу:")
    await bot.send_location(call.from_user.id, latitude=55.766321, longitude=37.686584)
    

@router.callback_query(F.data == 'about')
async def about(call: CallbackQuery): 
    await call.answer(text="", show_alert=False)
    ab = await bot.get_me()
    await bot.send_message(chat_id=call.from_user.id, text=str(ab)+" located at:")
    await bot.send_location(call.from_user.id, latitude=55.766321, longitude=37.686584)
    
@router.callback_query(F.data == 'search')
@router.message(Command("search"))
async def search(call: CallbackQuery):
    usr = await fetch_user(call.from_user.id)
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    if usr.user_status != 'normal':
        return await menu(call)
    await update_status(call.from_user.id, "search")
    await bot.send_dice(chat_id = call.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.add(*inline_search_buttons_list)
    # builder.adjust([1])
    markup = builder.as_markup()
    await bot.send_message(chat_id = call.from_user.id, text= f"Ищем для вас подходящего собеседника...", reply_markup=markup)
    counterpart = await get_counterpart(call.from_user.id)
    if counterpart is None:
        await add_to_search(usr)
    else:
        await drop_from_search(counterpart.telegram_uid)
        await update_status(call.from_user.id, "connected")
        await update_status(counterpart.telegram_uid, "connected")
        print(f"Found match for user {call.from_user.id}(@{call.from_user.username}), {counterpart.telegram_uid}")
        
        builder = InlineKeyboardBuilder()
        builder.add(*inline_connected_buttons_list)
        markup = builder.as_markup()
        counterpart_answer_rating = f"{counterpart.rating} 👍" if counterpart.rating >= 0 else f"{counterpart.rating} 👎"
        my_answer_rating = f"{usr.rating} 👍" if usr.rating >= 0 else f"{usr.rating} 👎"
        await bot.send_message(chat_id = call.from_user.id, text= f"Собеседник найден, рейтинг: {counterpart_answer_rating} \nИспользуйте /quit, чтобы прекратить диалог.", reply_markup=markup)
        await bot.send_message(chat_id = counterpart.telegram_uid, text= f"Собеседник найден, рейтинг: {my_answer_rating} \nИспользуйте /quit, чтобы прекратить диалог.", reply_markup=markup)
        await add_to_connections(call.from_user.id,counterpart.telegram_uid)
             
@router.callback_query(F.data == 'menu')
@router.message(Command("menu"))
async def menu(call):
    
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    await log_user(call.from_user.id)
    user = await fetch_user(call.from_user.id)
    status = user.user_status
    answer = "None"
    if  status == 'normal':
        answer = f"Добро пожаловать в главное меню, {call.from_user.full_name[:50]}!"
        buttons_list = inline_regular_buttons_list
    elif status == 'banned':
        answer = "Вы были заблокированы. Нажмите ниже, если хотите подать апелляцию."
        buttons_list = inline_banned_buttons_list
    elif status == 'search':
        buttons_list = inline_search_buttons_list
        answer = f"Вы в процессе поиска собеседника, {call.from_user.full_name[:50]}. Используйте /stop, чтобы прекратить поиск."
    elif status == 'connected':
        buttons_list = inline_connected_buttons_list
        answer = f"Вы находитесь в диалоге, {call.from_user.full_name[:50]}. Используйте /quit, чтобы прекратить диалог."
    
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(*buttons_list)
    keyboard_builder.adjust(*[1,2])
    menu_markup = keyboard_builder.as_markup()
    await bot.send_message(chat_id = call.from_user.id, text= answer, reply_markup=menu_markup)

@router.message()  
async def send_message(message : Message):
    did_reply = False if message.reply_to_message is None else True
    connected = await get_connected_user(message.from_user.id)
    if connected is not None:
        if not did_reply:
            reply = await message.copy_to(chat_id=connected)
        else:
            new_reply_id = await get_reply_id(message.reply_to_message.message_id, message.from_user.id)
            # print(new_reply_id, "\n\n\n\n")
            reply = await message.copy_to(chat_id=connected,reply_to_message_id=new_reply_id)
            
        pair = [message.message_id, reply.message_id]
        await log_message(message.from_user.id, pair[0], pair[1])
        await log_message(message.from_user.id, pair[1], pair[0])
    else:
        await basic(message)

async def basic(message : Message):
    builder = InlineKeyboardBuilder()
    builder.add(*inline_to_menu_buttons_list)
    markup = builder.as_markup()
    await message.answer(text="Неизвестная команда. Используйте /menu, чтобы попасть в основное меню", reply_markup=markup)



