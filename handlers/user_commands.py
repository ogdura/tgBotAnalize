from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile

import keyboards.keyboards
from analize.analize import Analize
from data.database import DataBase
from config.config import bd_path
from keyboards import keyboards
from utils import states
from aiogram.fsm.context import FSMContext
from utils.states import Bebra, ShowBebra, DellBebra, AnalizeBebra
from aiogram.filters.callback_data import CallbackData
bd = DataBase(bd_path)
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user = bd.get_user(message.from_user.id)
    if(not user):
        bd.add_user(message.from_user.id)
    await message.answer("Введите соответствующую команду:\n/spend - ввести трату \n/analize - анализ трат\n/show-показать трату",reply_markup=keyboards.main)
@router.message(F.text.lower() == "отмена")
async def cancel(message: Message, state:FSMContext):
    await state.clear()
    await message.answer("Запись отменена.",reply_markup=keyboards.main)
@router.message(F.text == "📊  Анализ затрат")
async def anal(message: Message, state:FSMContext):
    types_spend = bd.get_types(message.from_user.id)
    if (not types_spend):
        await state.set_state(Bebra.set_type)
        await message.answer(
            'У вас нет еще ни одной категории затрат. Пожалуйста, прежде чем вводить затрату, введите категорию.',
            reply_markup=keyboards.cancel)
    else:
        await message.answer("Выберите номер категории трат:")
        for index, a in enumerate(types_spend):
            await message.answer(f"{index + 1} - {a[1]}")
        await state.set_state(AnalizeBebra.choise)
@router.message(Command('analize'))
async def anal(message: Message,state: FSMContext):
    types_spend = bd.get_types(message.from_user.id)
    if (not types_spend):
        await state.set_state(Bebra.set_type)
        await message.answer(
            'У вас нет еще ни одной категории затрат. Пожалуйста, прежде чем вводить затрату, введите категорию.',
            reply_markup=keyboards.cancel)
    else:
        await message.answer("Выберите номер категории трат:")
        for index, a in enumerate(types_spend):
            await message.answer(f"{index + 1} - {a[1]}")
        await state.set_state(AnalizeBebra.choise)
@router.message(F.text == "💵  Ввести затраты")
async def anal(message: Message, state: FSMContext):
    types_spend = bd.get_types(message.from_user.id)
    if (not types_spend):
        await state.set_state(Bebra.set_type)
        await message.answer(
            'У вас нет еще ни одной категории затрат. Пожалуйста, прежде чем вводить затрату, введите категорию.',
            reply_markup=keyboards.cancel)
    else:
        await message.answer("Выберите номер категории трат или создайте новую категорию", reply_markup=keyboards.ik())
@router.message(Command('spend'))
async def anal(message: Message, state: FSMContext):
    types_spend = bd.get_types(message.from_user.id)
    if (not types_spend):
        await state.set_state(Bebra.set_type)
        await message.answer(
            'У вас нет еще ни одной категории затрат. Пожалуйста, прежде чем вводить затрату, введите категорию.',
            reply_markup=keyboards.cancel)
    else:
        await message.answer("Выберите номер категории трат или создайте новую категорию", reply_markup=keyboards.ik())
@router.message(F.text == "👁  Показать траты")
async def showType(message: Message,state: FSMContext):
    user_types=bd.get_types(message.from_user.id,)
    if(user_types):
        await message.answer("Выберите категорию:")
        for index, a in enumerate(user_types):
            await message.answer(f"{index+1} - {a[1]}")
        await state.set_state(ShowBebra.choise_type)
    else:
        await message.answer("У вас еще нет трат")
@router.message(Command("show"))
async def showType(message: Message,state: FSMContext):
    user_types=bd.get_types(message.from_user.id,)
    if(user_types):
        await message.answer("Выберите категорию:")
        for index, a in enumerate(user_types):
            await message.answer(f"{index+1} - {a[1]}")
        await state.set_state(ShowBebra.choise_type)
    else:
        await message.answer("У вас еще нет трат")
@router.message(F.text == "❌  Удалить")
async def showType(message: Message,state: FSMContext):
    types_spend = bd.get_types(message.from_user.id)
    if (not types_spend):
        await state.set_state(Bebra.set_type)
        await message.answer(
            'У вас нет еще ни одной категории затрат. Пожалуйста, прежде чем удалять, введите категорию.',
            reply_markup=keyboards.cancel)
    else:
        await message.answer("Выберите, что вы хотите удалить",reply_markup=keyboards.bebra())
@router.message(AnalizeBebra.choise)
async def choise_type(message: Message, state: FSMContext):
    types_spend = bd.get_types(message.from_user.id)
    type_id = -1
    for index, a in enumerate(types_spend):
        if index+1 == int(message.text):
            type_id = a[0]
    spending = bd.get_spend_type(type_id, message.from_user.id)
    if (spending):
        a = Analize(spending)
        a.analize(message.from_user.id)

        await message.answer(f"Анализ трат:\n\nМаксимальное трата: {a.max_name} - {a.maxxx} рублей\n\nМинимальная трата: {a.min_name} - {a.min} рублей\n\nСредняя сумма траты: {round(a.avg,2)} рублей\n\n Всего трат совершено: {a.all_spendes}")
        await message.answer("График трат:")
        await message.reply_photo(
            photo=FSInputFile(
                path=a.path
            )
        )
        a.delPhoto()

@router.message(ShowBebra.choise_type)
async def choise_type(message: Message, state: FSMContext):

    types_spend = bd.get_types(message.from_user.id)
    type_id = -1
    for index, a in enumerate(types_spend):
        if index == int(message.text) - 1:
            type_id = a[0]
    spending=bd.get_spend_type(type_id,message.from_user.id)
    if(spending):
        for index, a in enumerate(spending):
            await message.answer(str(a[2])+" - "+str(a[3])+" рублей")
    else:
        await message.answer("Такой категории не существует или в ней нет трат")
        await state.set_state(ShowBebra.choise_type)
@router.message(Bebra.choise_type)
async def choise_type(message: Message, state: FSMContext):
    try:
        types_spend = bd.get_types(message.from_user.id)
        for index, a in enumerate(types_spend):
            if index+1 == float(message.text):
                await state.update_data(type=a[1])
                await state.set_state(Bebra.spend_name)
                await message.answer("Введите наименование траты.")
        if float(message.text) > index+1 or float(message.text)<=0:
            await message.answer("Введите корректный номер категории", reply_markup=keyboards.cancel)
            await state.set_state(Bebra.choise_type)
    except ValueError:
        await message.answer("Введите корректное значение")
        await state.set_state(Bebra.choise_type)
        await message.answer("Введите наименование траты.")
@router.message(Bebra.set_type)
async def set_type(message: Message, state:FSMContext):
    await state.update_data(type=message.text)
    types = bd.get_type_id(message.text, message.from_user.id)
    if (not types):
        bd.add_type(message.text, message.from_user.id)
        await state.set_state(Bebra.spend_name)
        await message.answer("Введите название траты", reply_markup=keyboards.cancel)
    else:
        await message.answer("Такая категория уже существует.")
@router.message(Bebra.spend_name)
async def set_name(message: Message, state:FSMContext):
    await state.update_data(spend_name=message.text)
    await state.set_state(Bebra.spend_price)
    await message.answer("Введите сумму траты",reply_markup=keyboards.cancel)
@router.message(Bebra.spend_price)
async def set_price(message: Message, state:FSMContext):
    try:
        price = float(message.text)
        if (price > 0):
            await state.update_data(spend_price=message.text)
            data = await state.get_data()
            await state.clear()
            type_user_id=bd.get_type_id(data["type"],message.from_user.id)
            bd.add_spend(data["spend_name"],data["spend_price"],message.from_user.id,type_user_id[0][0])
            await message.answer(f"Вы успешно ввели затрату {data['spend_name']} на сумму {data['spend_price']} в категорию {data['type']}", reply_markup=keyboards.main)
        else:
            await message.answer("На этом этапе вы должны ввести число больше нуля.")
            await state.set_state(Bebra.spend_price)
            await message.answer("Введите сумму траты.", reply_markup=keyboards.cancel)
    except ValueError:
        await message.answer("Cумма должна быть положительным числом")
        await state.set_state(Bebra.spend_price)
        await message.answer("Введите сумму траты.", reply_markup=keyboards.cancel)

@router.message(DellBebra.dell_type)
async def delType(message: Message):
    try:
        types_spend = bd.get_types(message.from_user.id)
        id_type = -1
        for index, a in enumerate(types_spend):
            if index == int(message.text)-1:
                id_type = a[0]
        if(id_type>=0):
            bd.del_type(id_type,message.from_user.id)
            await message.answer(f"Категория успешно удалена")
        else:
            await message.answer("❌ Ошибка")
    except:
        await message.answer("Ошибка")
        await states.set_state(DellBebra.dell_type)



@router.message(DellBebra.dell_type)
async def delType(message: Message, state: FSMContext):
    try:
        types_spend = bd.get_types(message.from_user.id)
        id_type = -1
        for index, a in enumerate(types_spend):
            if index+1 == int(message.text):
                id_type = a[0]
        if id_type>=0:
            bd.del_type(id_type)
            await message.answer("Категория успешно удалена")
    except:
        await message.answer("Ошибка")
        await state.set_state(DellBebra.dell_type)

@router.message(DellBebra.choise_spend)
async def delType(message: Message, state: FSMContext):
    try:
        types_spend = bd.get_types(message.from_user.id)
        id_type = -1
        for index, a in enumerate(types_spend):
            if index+1 == int(message.text):
                id_type = a[0]
        if id_type>=0:
            spendes = bd.get_spend_type(id_type, message.from_user.id)
            if(spendes):
                await state.set_state(DellBebra.dell_spend)
                await message.answer("Выберите номер траты")
                for index, a in enumerate(spendes):
                    await state.update_data(type=id_type)
                    await message.answer(f"{index + 1} - {a[2]}")
            else:
                await message.answer("У вас еще нет трат")
    except:
        await message.answer("Ошибка")
        await state.set_state(DellBebra.choise_spend)


@router.message(DellBebra.dell_spend)
async def delSpend(message: Message, state: FSMContext):
    try:
        data=await state.get_data()
        spendes = bd.get_spend_type(data['type'],message.from_user.id)
        id_type = -1
        for index, a in enumerate(spendes):
            if index + 1 == int(message.text):
                id_type = a[0]
        if id_type >= 0:
            bd.del_spend_choise(data['type'],id_type,message.from_user.id)
            await message.answer("Трата успешно удалена")
    except:
        await message.answer("Ошибка")
        await state.set_state(DellBebra.dell_spend)

@router.callback_query(keyboards.Pagination.filter(F.action=="choise"))
async def choise_type(call: CallbackQuery, callback_data:keyboards.Pagination, state: FSMContext):
    types_spend = bd.get_types(call.from_user.id)
    await call.message.answer("Выберите номер категории трат:")
    for index, a in enumerate(types_spend):
        await call.message.answer(f"{index + 1} - {a[1]}")
    await state.set_state(Bebra.choise_type)



@router.callback_query(keyboards.Pagination.filter(F.action=="create"))
async def create_type(call: CallbackQuery, callback_data:keyboards.Pagination, state: FSMContext):
    await call.message.answer("Введите наименование категории трат:")
    await state.set_state(Bebra.set_type)



@router.callback_query(keyboards.DelSpend.filter(F.action=="type"))
async def choise_type(call: CallbackQuery, callback_data:keyboards.DelSpend, state: FSMContext):
    types_spend = bd.get_types(call.from_user.id)
    await call.message.answer("Выберите номер категории трат:")
    for index, a in enumerate(types_spend):
        await call.message.answer(f"{index + 1} - {a[1]}")
    await state.set_state(DellBebra.dell_type)



@router.callback_query(keyboards.DelSpend.filter(F.action=="spend"))
async def choise_type(call: CallbackQuery, callback_data:keyboards.DelSpend, state: FSMContext):
    types_spend = bd.get_types(call.from_user.id)
    await call.message.answer("Выберите номер категории трат:")
    for index, a in enumerate(types_spend):
        await call.message.answer(f"{index + 1} - {a[1]}")
    await state.set_state(DellBebra.choise_spend)
