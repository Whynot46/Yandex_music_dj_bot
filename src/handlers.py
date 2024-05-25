from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.keyboards as kb
import src.db as db
from src.config import ADMIN_ID



router = Router()


class Track(StatesGroup):
    name = State()


@router.message(F.text, Command("start"))
async def start_loop(message: Message, bot: Bot):
    await message.answer(text=f"Привет, @{message.from_user.username}!\n"
        "Я бот-диджей🧑🏻‍💻, который поможет тебе быстро, просто и бесплатно находить треки любимых исполнителей \n"
        "и скачивать их прямиком с Яндекс Музыки🎧", reply_markup=kb.main_keyboard)
    if not db.is_old(message.from_user.id):
        db.add_new_user(message.from_user.id, message.from_user.username)


@router.message(F.text == "/playlist")  
async def get_db(message: Message, bot: Bot): 
    playlist = db.get_playlist(message.from_user.id)
    if len(playlist) > 0:
        user_playlist = ""
        for track in playlist:
            user_playlist+=f"{track}\n"
        await message.answer(f"Ваш плейлист:\n{user_playlist}", reply_markup=kb.playlist_keyboard) 
    else:
        await message.answer("Ваш плейлист пуст", reply_markup=kb.main_keyboard)
        
        
@router.message(F.text == "Ваш плейлист🔉")  
async def get_db(message: Message, bot: Bot): 
    playlist = db.get_playlist(message.from_user.id)
    if len(playlist) > 0:
        user_playlist = ""
        for track in playlist:
            user_playlist+=f"{track}\n"
        await message.answer(f"Ваш плейлист:\n{user_playlist}", reply_markup=kb.playlist_keyboard) 
    else:
        await message.answer("Ваш плейлист пуст", reply_markup=kb.main_keyboard)
            
        
@router.message(F.text == "/find")  
async def find_track(message: Message, bot: Bot, state = FSMContext):  
    await state.set_state(Track.name)
    await message.answer(text="Введите название трека🎵") 
    

@router.message(F.text == "Найти трек🔎")  
async def find_track(message: Message, bot: Bot, state = FSMContext):  
    await state.set_state(Track.name)
    await message.answer(text="Введите название трека🎵") 
    
    
@router.message(Track.name)
async def get_name(message: Message,state = FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    await message.answer(text="По твоему запросу я нашёл следующие треки:", reply_markup=kb.generate_tracks_keyboard(str(data["name"])))
    
        
@router.message(F.text == "/users")  
async def get_db(message: Message, bot: Bot):  
    if str(message.from_user.id) in ADMIN_ID:  
        db.get_xlsx()
        await message.answer_document(document=FSInputFile("./db/data.xlsx")) 
        # os.remove(f"data.xlsx") 
        

@router.callback_query(F.data)
async def track_callback(callback: CallbackQuery, bot: Bot):
    if str(callback.data)[:8]=="download":
        await callback.message.edit_text(f"{callback.message.text}\nЗагрузка трека...")
        await callback.message.edit_reply_markup(reply_markup=kb.download_keyboard)
        kb.yandex.download_track(f"{callback.message.text}")
        await callback.message.answer_audio(audio=FSInputFile(f"./music/{callback.message.text}.mp3"))
        await callback.message.edit_text(f"{callback.message.text}")
    elif str(callback.data)[:3]=="add":
        await callback.message.edit_text(f"{callback.message.text}\nТрек успешно добавлен в Ваш плейлист")
        db.put_track_to_playlist(callback.from_user.id ,f"{callback.message.text}")
        await callback.message.edit_reply_markup(reply_markup=kb.add_keyboard)
        await callback.message.edit_text(f"{callback.message.text}")
    elif str(callback.data)[:3]=="was":
        if str(callback.data)[:12]=="was_download":
            callback.answer("Трек уже скачен", show_alert=True, reply_markup=kb.main_keyboard)
        elif str(callback.data)[:7]=="was_add":
            callback.answer("Трек уже был добавлен в Ваш плейлист", show_alert=True, reply_markup=kb.main_keyboard)
    elif str(callback.data)=="playlist":
        user_playlist = db.get_playlist(callback.from_user.id)
        for track in user_playlist:
            kb.yandex.download_track(track)
            await callback.message.answer_audio(audio=FSInputFile(f"./music/{track}.mp3"), reply_markup=kb.main_keyboard)
    else:
        await callback.message.answer(f"{callback.data}", reply_markup=kb.generate_track_keyboard(callback.data))


