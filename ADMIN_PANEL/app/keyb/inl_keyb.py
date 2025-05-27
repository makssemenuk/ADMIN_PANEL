from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




def admin_main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Статистика", callback_data="stats")],
            [InlineKeyboardButton(text="Рассылка", callback_data="broadcast")],
            [InlineKeyboardButton(text="Доп.настройки", callback_data="settings")],
        ]
    )
    return keyboard 
    
    
def back_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back")],
        ]
    )
    return keyboard