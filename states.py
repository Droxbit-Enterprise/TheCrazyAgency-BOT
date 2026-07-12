from aiogram.fsm.state import State, StatesGroup

class RegistroStates(StatesGroup):
    edad = State()
    wifi = State()
    disponibilidad = State()
    validador_usuaria = State()
    
    
    
    seleccion_app = State()
    seleccion_inicial = State()
    nombre = State()
    apellidos = State()
    documento = State()
    pais = State()
    telefono = State()
    tiempo = State()
    pin = State()
    whatsapp = State()
    confirmacion = State()
    vio_video_sugo = State()
    registro_plataforma = State()
    antigua_pregunta = State()
    pedir_nombre = State()
    esperando_activacion = State()
    iniciar_sesion_sugo = State()
    preguntar_gestionar_sugo = State()
    numero_telefono = State()
    preguntar_gestionar_sugo = State()
    preguntar_gestionar_sugo = State()
    preguntar_gestionar_sugo = State()
    
class MenuStates(StatesGroup):
    menu_principal = State()
    
class UsuariaRegistroStates(StatesGroup):
    valida_registro_api = State()
    iniciar_sesion = State()
    nombre = State()
    apellido = State()
    doc = State()
    pais = State()
    telefono = State()
    pin = State()
    telefono_wp = State()
    telefono_tg = State()