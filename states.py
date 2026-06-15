from aiogram.fsm.state import State, StatesGroup

class RegistroStates(StatesGroup):
    seleccion_inicial = State()
    esperando_edad = State()
    esperando_wifi = State()
    esperando_disponibilidad = State()
    seleccion_app = State()  
    vio_video_sugo = State()
    registro_plataforma = State() 
    pedir_nombre = State()
    esperando_activacion = State()
    antigua_pregunta = State()