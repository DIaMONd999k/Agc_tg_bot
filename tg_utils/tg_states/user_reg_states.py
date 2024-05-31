from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    requestFIO = State()
    regName = State()
    regPhone = State()
    inputPhone = State()
    wrongName = State()
    wrongPhone = State()
    dataGotSuccess = State()
    sendRequestToAdmin = State()

