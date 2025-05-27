from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage




from app.database.models import SessionLocal, User, Broadcast




storage = MemoryStorage()
router= Router()


@router.message(Command("start"))
async def start_command(message: Message):
    db = SessionLocal()
    user = db.query(User).filter(User.tglegram_id == message.from_user.id).first()
    if not user:
        new_user = User(tglegram_id=message.from_user.id, name=message.from_user.full_name)
        db.add(new_user)
        db.commit()
    db.close()
    await message.answer("Welcome to the bot!")