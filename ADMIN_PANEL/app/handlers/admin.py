import os
import asyncio

from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

from app.database.models import SessionLocal, User, Broadcast
from app.keyb.inl_keyb import admin_main_menu, back_menu


ADMIN_ID = 6042448553

router = Router()

class BroadcastStates(StatesGroup):
    message = State()
    
    




@router.message(Command("admin"))
async def admin_start(message: Message, bot: Bot):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет доступа к этой команде.")
        return
    await message.answer("Вы в админ-меню", reply_markup=admin_main_menu())
    
    
@router.callback_query(F.data == "back")
async def back_to_main_menu(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_text("Вы в админ-меню", reply_markup=admin_main_menu())
    await callback.answer()
    

@router.callback_query(F.data == "stats")
async def stats(callback: CallbackQuery, bot: Bot):
    db = SessionLocal()
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.active == True).count()
    db.close()
    
    text = f"Cтатистика:\nВсего пользователей: {total_users}\nАктивных пользователей: {active_users}"
    await callback.message.edit_text(text, reply_markup=back_menu())
    await callback.answer() 
    
    
@router.callback_query(F.data == "broadcast")
async def broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text("Введите сообщение для рассылки:", reply_markup=back_menu())
    await state.set_state(BroadcastStates.message)
    await callback.answer()


@router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery, bot: Bot):
    await callback.message.edit_text("Настройки:", reply_markup=back_menu())
    await callback.answer()
    
    
@router.message(BroadcastStates.message)
async def broadcast_message(message: Message, state: FSMContext, bot: Bot):
    broadcast_text = message.text
    db = SessionLocal()
    users = db.query(User).filter(User.active == True).all()
    count = 0
    for user in users:
        try:
            await bot.send_message(user.tglegram_id, broadcast_text)
            count += 1
        except Exception as e:
            print(f"Error sending message to {user.tglegram_id}: {e}")
            
            
    new_broadcast = Broadcast(message=broadcast_text)
    db.add(new_broadcast)
    db.commit()
    db.close()
    await message.answer(f"Рассылка завершена. Сообщение отправлено {count} пользователям.")
    await state.clear()



# @router.message()
# async def unknown_message(message: Message):
#     await message.copy_to(chat_id=ADMIN_ID, reply=True)