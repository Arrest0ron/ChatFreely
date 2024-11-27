from aiogram.types import InlineKeyboardButton

inline_to_menu_buttons_list = [
    InlineKeyboardButton(text="Перейти в меню", callback_data="menu")
    ]
inline_dialogue_end_buttons_list = [
    InlineKeyboardButton(text="Перейти в меню", callback_data="menu"),
    InlineKeyboardButton(text="Найти собеседника", callback_data="search")
    ]
inline_search_buttons_list = [
    InlineKeyboardButton(text="Прекратить поиск", callback_data="stop")
]
inline_connected_buttons_list = [
    InlineKeyboardButton(text="Прекратить диалог", callback_data="quit")
]

inline_regular_buttons_list = [
     
    InlineKeyboardButton(text="Найти собеседника", callback_data="search"), 
    InlineKeyboardButton(text="Мой профиль", callback_data="profile"),
    InlineKeyboardButton(text="О боте", callback_data="about")
]
inline_banned_buttons_list = [
    InlineKeyboardButton(text="Подать апелляцию", callback_data="appeal")
]

inline_rate_buttons_list = [
    InlineKeyboardButton(text="👍", callback_data="increase_rating"),
    InlineKeyboardButton(text="👎", callback_data="decrease_rating"),  
    InlineKeyboardButton(text="Пожаловаться", callback_data="report")        
]