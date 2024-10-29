from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
def get_inline_kb():
    inline_kb_list = [
            [InlineKeyboardButton(text = "Сообщить о правонарушении🔞",callback_data='get_warn')],
            [InlineKeyboardButton(text="Наш телеграм-канал📰", url='https://t.me/kiberdruzhina')],
            [InlineKeyboardButton(text="Правила",callback_data="rules")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def cancel():
    inline_Cancel = [
        [InlineKeyboardButton(text = "Отменить❌", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_Cancel)

def ban(userid):
    inline_ban = [
        [InlineKeyboardButton(text = "Запретить доступ к отправке", callback_data=str(userid))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_ban)

def callunban():
    inline_unban = [
        [InlineKeyboardButton(text = "Запросить разблокировку", callback_data="query_unban")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_unban)

def unban(userid):
    inline_unban = [
        [InlineKeyboardButton(text = "Открыть доступ к отправке", callback_data=str(userid))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_unban)

def root_inline_kb(db,id):
    builder = InlineKeyboardBuilder()
    if not db.select_collage(id):
        builder.row(InlineKeyboardButton(text="Ввести информацию о колледже", callback_data='set_collage'))
    if not db.select_fio(id):
        builder.row(InlineKeyboardButton(text="Ввести ваше ФИО", callback_data='set_fio'))
    if not db.select_group(id):
        builder.row(InlineKeyboardButton(text="Ввести вашу группу", callback_data='set_group'))
    builder.adjust(1)
    return builder.as_markup()