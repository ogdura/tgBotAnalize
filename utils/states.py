from aiogram.fsm.state import StatesGroup, State

class Bebra(StatesGroup):
    type_spend = State()
    choise_type = State()
    set_type = State()
    spend_name = State()
    spend_price = State()
class ShowBebra(StatesGroup):
    choise_type = State()
class DellBebra(StatesGroup):
    dell_type = State()
    choise_spend = State()
    dell_spend = State()
class AnalizeBebra(StatesGroup):
    choise=State()