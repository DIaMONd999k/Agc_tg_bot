from aiogram.fsm.state import StatesGroup, State


class AdminRegisterState(StatesGroup):
    newUser = State()
    multipleMatch = State()
    multipleRequests = State()
    searchInDB = State()
    userFound = State()
    userNotFound = State()
    searchById = State()
    requestId = State()
    idNotFound = State()
    deleteRequest = State()

