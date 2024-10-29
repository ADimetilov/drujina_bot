from aiogram import Router,F,Bot
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from inline_kbs import *
import db_class
router = Router()
db = db_class.DataBase("drujina.db")
@router.message(Command("start"))
async def start_handler(msg:Message):
    if not db.search(msg.from_user.id):
        db.newuser(msg.from_user.id)
    await msg.answer("Добрый день. Чем я могу вам помочь?👋",reply_markup=get_inline_kb())


class Form(StatesGroup):
    FIO = State()
    Collage = State()
    group = State()
    adres = State()
    typewarn = State()

@router.message(Form.adres)
async def get_type(msg:Message, state:FSMContext):
    await state.update_data(adres=msg.text)
    await msg.answer("Укажите тип нарушения (Наркотики,Оружие,Казино и т.п.):",reply_markup=cancel())
    await state.set_state(Form.typewarn)
    
@router.message(Form.typewarn)
async def commit(msg:Message,state:FSMContext,bot:Bot):
    await state.update_data(typewarn = msg.text)
    id = msg.from_user.id
    data = await state.get_data()
    await bot.send_message(-1002321664383,f"<b>Ссылка:</b> {data['adres']}\n<b>Тип нарушения:</b> {data['typewarn']}\n<b>ФИО отправителя: </b>{db.get_fio(id)}\n<b>Колледж:</b> {db.get_collage(id)}\n<b>Группа:</b> {db.get_group(id)}",reply_markup=ban(msg.from_user.id))
    await msg.answer("Нарушение зафиксировано и отравлено на проверку, спасибо за вашу активную гражданскую позицию❤️",reply_markup=get_inline_kb())
    await state.clear()

async def check(id):
    if db.select_group(id) == True and db.select_fio(id) == True and db.select_collage(id) ==  True:
        return True
    else:
        return False

@router.message(Form.FIO)
async def insert_fio(msg:Message, state: FSMContext):
    db.fio_user(msg.text,msg.from_user.id)
    state.clear()
    if await check(msg.from_user.id):
         await msg.answer("ФИО добавлено, все данные заполнены, доступ к функционалу разрешен✅",reply_markup=get_inline_kb())
         return None
    await msg.answer("ФИО добавлено✅",reply_markup=root_inline_kb(db,msg.from_user.id))

@router.message(Form.Collage)
async def insert_collage(msg:Message, state: FSMContext):
    db.collage_user(msg.text,msg.from_user.id)
    state.clear()
    if await check(msg.from_user.id):
         await msg.answer("Колледж добавлен, все данные заполнены, доступ к функционалу разрешен✅",reply_markup=get_inline_kb())
         return None
    await msg.answer("Колледж добавлен✅",reply_markup=root_inline_kb(db,msg.from_user.id))

@router.message(Form.group)
async def insert_group(msg:Message, state: FSMContext):
    db.group_user(msg.text,msg.from_user.id)
    state.clear()
    if await check(msg.from_user.id):
         await msg.answer("Группа добавлена, все данные заполнены, доступ к функционалу разрешен✅",reply_markup=get_inline_kb())
         return None
    await msg.answer("Группа добавлена✅",reply_markup=root_inline_kb(db,msg.from_user.id))

@router.callback_query() 
async def check_button(call:CallbackQuery,state: FSMContext,bot:Bot): 
    if call.data == "get_warn": 
        id = call.from_user.id
        if db.select_group(id) == False or db.select_fio(id) == False or db.select_collage(id) ==  False:
            print(str(db.select_group(id)))
            print(str(db.select_fio(id)))
            print(str(db.select_collage(id)))
            rules_insert =  "У вас не заполнена информация о: "
            if not db.select_collage(id):
                rules_insert += "<b>Колледже</b> "
            if not db.select_fio(id):
                rules_insert += "<b>ФИО</b> "
            if not db.select_group(id):
                rules_insert += "<b>Группе</b> "
            await call.message.answer(rules_insert, reply_markup=root_inline_kb(db,id))
            return None
        else:
            if db.isblock(id):
                await call.message.answer("Доступ к отправке запрещен КиберДружиной", reply_markup=callunban())
                return None
            await call.message.answer("Хорошо, вышлите ссылку на нарушение", reply_markup=cancel()) 
            await state.set_state(Form.adres)
    if call.data == "set_fio":
        await call.message.answer("Введите ваше ФИО✏️")
        await state.set_state(Form.FIO)
    if call.data == "rules":
        await call.message.answer("<b>Правила использования:</b>\n1. Для отправки сообщений необходимо указать информацию  которая от вас требуется\n2. Запрещено злоупотребление сообщениями по одной теме\n3. Запрещено использование возможностей бота не по назначению\n\n<b>За нарушение любого из  пункта правил, участник дружины имеет право выдать вам перманентную блокировку.</b>\n\nЗапрос на разблокировку можно подать 1 раз после блокировки.\n(Запрос доступен снова после повторной блокировки)")
    if call.data == "query_unban":
        id = call.from_user.id
        if db.isquery(call.from_user.id):
            await call.message.answer("Запрос уже был отправлен")
        else:
            await call.message.answer("<b>Запрос на разблокировку направлен дружине 🏹 \nЕсли вы будете разблокированы вам придет сообщение 📥</b>")
            db.insert_unban(id)
            await bot.send_message(-1002321664383,f"Поступил запрос на разблокировку:\n<b>ФИО отправителя: </b>{db.get_fio(id)}\n<b>Колледж:</b> {db.get_collage(id)}\n<b>Группа:</b> {db.get_group(id)}",reply_markup=unban(id))
    if call.data == "cancel":
        await call.message.answer("Отменено❌")
        await call.message.answer("Доступные действия:",reply_markup=get_inline_kb())
        await state.clear()
    if call.data == "set_collage":
        await call.message.answer("Введите ваш колледж🏘")
        await state.set_state(Form.Collage)
    if call.data == "set_group":
        await call.message.answer("Введите вашу группу👥")
        await state.set_state(Form.group)
    if db.search(call.data):
        if db.isquery(call.data) and db.isblock(call.data):
            db.unban(call.data)
            await call.message.answer("<b>Успешно!Пользователь разблокирован🔓</b>")
            await bot.send_message(call.data,"<b>Доступ к боту предоставлен✅</b>",reply_markup=get_inline_kb())
            return None
        db.block(call.data)
        await call.message.answer("<b>Пользователь заблокирован🔒</b>")
    await call.answer()
