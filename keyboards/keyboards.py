from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


main = ReplyKeyboardMarkup(
    keyboard=[
         [
             KeyboardButton(text="💵  Ввести затраты"),
             KeyboardButton(text="📊  Анализ затрат"),
         ],
        [
             KeyboardButton(text="👁  Показать траты"),
             KeyboardButton(text="❌  Удалить"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действия из меню"
)
cancel= ReplyKeyboardMarkup(
    keyboard=[
       [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    one_time_keyboard = True
)

class Pagination(CallbackData,prefix="pag"):
    action: str

def ik():
    keyboard_builder=InlineKeyboardBuilder()
    keyboard_builder.button(text="Создать", callback_data=Pagination(action="create").pack())
    keyboard_builder.button(text="Выбрать", callback_data=Pagination(action="choise").pack())
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()

class DelSpend(CallbackData,prefix="del"):
    action: str
def bebra():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Категорию", callback_data=DelSpend(action="type").pack())
    keyboard_builder.button(text="Трату", callback_data=DelSpend(action="spend").pack())
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()