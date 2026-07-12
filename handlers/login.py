from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import RegistroStates, MenuStates, UsuariaRegistroStates
from database import save_user_full
from handlers.menu import menu_principal
from functions import *
from config import *

login_router = Router()

###-------- VALIDA EL INICIO DE SESION --------------###
# Recibe el pais
@login_router.message(UsuariaRegistroStates.iniciar_sesion)
async def iniciar_sesion_pais(message: Message, state: FSMContext):
    if message.text.lower() == "soy nueva":
        await state.set_state(RegistroStates.edad)
        await message.answer("Perfecto 💛\n¿Cuántos años tienes?")
    else:
        await message.answer("Si ya perteneces a la agencia, escribe tu ID para verificar.")
        # Aquí puedes validar si ya existe en DB