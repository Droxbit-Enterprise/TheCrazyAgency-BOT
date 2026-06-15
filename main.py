import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from states import RegistroStates
url_static= "https://panel-droxbit-media-706168159909-us-east-2-an.s3.us-east-2.amazonaws.com/The+Crazy+Agency/media/"

load_dotenv()
TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Diccionario temporal para mapear IDs internos
user_map = {}

# Simulación de escritura
async def typing(message: Message, seconds: int = 2):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(seconds)

# Botones Nueva / Antigua
def botones_nueva_antigua():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Soy nueva 💎")
    kb.button(text="Ya estoy en la agencia 💸")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

# Botones Sí / No
def botones_si_no():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Sí 💎")
    kb.button(text="No 💸")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def botones_apps():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Sugo")
    kb.button(text="Salsa")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


###-------- INICIOS DEL BOT --------------###
# Comando /start
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear() 
    await typing(message, 2)
    await message.answer(
        "💎 Bienvenida señorita 💛\n"
        "Antes de comenzar, cuéntame algo:\n\n"
        "👉 ¿Eres nueva o ya perteneces a *The Crazy Agency*?",
        reply_markup=botones_nueva_antigua()
    )
    await state.set_state(RegistroStates.seleccion_inicial)

# Se ejecuta si la chica dice que es menor de edad y vuelve a responder si la misma chica escribe de nuevo
@dp.message(F.text.lower().in_({"hola", "buenas", "hey", "holi", "ola", "holis", "Holis", "Holi", "Ola", "Hey", "Buenas", "Hola"}))
async def reiniciar_conversacion(message: Message, state: FSMContext):
    await state.clear()
    await typing(message, 1)
    await message.answer(
        "💎 Hola señorita, bienvenida nuevamente 💛\n"
        "Vamos a comenzar de nuevo.\n\n"
        "👉 ¿Eres nueva o ya perteneces a *The Crazy Agency*?",
        reply_markup=botones_nueva_antigua()
    )
    await state.set_state(RegistroStates.seleccion_inicial)

# Selección inicial
@dp.message(RegistroStates.seleccion_inicial)
async def seleccion_inicial(message: Message, state: FSMContext):
    texto = message.text.lower()
    # NUEVA
    if "nueva" in texto:
        await bot.send_message(
            GROUP_ID,
            f"💎 *Nueva chica interesada en generar ingresos* 💸\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n\n"
            f"⚠️ Equipo, estén pendientes: acaba de iniciar el proceso de registro."
        )
        await typing(message, 2)
        await message.answer(
            "Perfecto señorita 💎💸\n"
            "Vamos a hacerte unas preguntas rápidas.\n\n"
            "👉 ¿Eres mayor de 18 años?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.esperando_edad)

    # ANTIGUA
    elif "agencia" in texto or "antigua" in texto:
        await typing(message, 2)
        await message.answer(
            "Perfecto señorita 💛\n"
            "Cuéntame, ¿qué necesitas hoy? 💎",
            reply_markup=None
        )
        await state.set_state(RegistroStates.antigua_pregunta)

    else:
        await message.answer("No entendí señorita 💎, ¿eres nueva o ya estás en la agencia?")

# Pregunta 1: Edad
@dp.message(RegistroStates.esperando_edad)
async def preguntar_edad(message: Message, state: FSMContext):
    texto = message.text.lower()
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)
        await message.answer(
            "Perfecto 💎\n👉 ¿Tienes teléfono propio y acceso a internet estable?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.esperando_wifi)

    elif any(x in texto for x in ["no", "No", "n", "not"]):
        await typing(message, 2)
        await state.clear()
        await message.answer(
            "Lo siento señorita 💛, por ahora no puedes continuar.\n"
            "Si deseas volver a empezar cuando seas mayor de edad, solo escribe *hola* o usa el comando /start 💎"
        )        
        await bot.send_message(
            GROUP_ID,
            f"⚠️ La chica es menor de edad\n"
            f"👤 @{message.from_user.username}\n"
            f"💬 Esta chica quiere trabajar pero es menor de edad."
        )
        return

    else:
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Respuesta no reconocida en *edad*\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 {message.text}"
        )
        await message.answer("No entendí tu respuesta señorita 💎, ¿eres mayor de 18?")

# Pregunta 2: Wifi / Teléfono
@dp.message(RegistroStates.esperando_wifi)
async def preguntar_wifi(message: Message, state: FSMContext):
    texto = message.text.lower()        
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)        
        await message.answer(
            "Perfecto 💎\n👉 ¿Tienes disponibilidad al menos 4 o 6 horas diarias para trabajar?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.esperando_disponibilidad)
    
    elif any(x in texto for x in ["no", "No", "n", "not"]):
        await typing(message, 2)
        await state.clear()
        await message.answer(
            "Lo siento señorita 💛, necesitas un teléfono e internet estable para trabajar con nosotros, por ahora no puedes continuar.\n"
            "Si deseas volver a empezar cuando Tengas un teléfono y conexión a internet, solo escribe *hola* o usa el comando /start 💎"
        )
        return

    else:
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Respuesta no reconocida en *wifi*\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 {message.text}"
        )
        await message.answer("No entendí tu respuesta señorita 💎, ¿tienes un buen teléfono e internet estable?")

# Pregunta 3: Disponibilidad
@dp.message(RegistroStates.esperando_disponibilidad)
async def preguntar_disponibilidad(message: Message, state: FSMContext):
    texto = message.text.lower()    
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 3)
        await message.answer(
            "Perfecto señorita 💎💸\n"
            "Ya cumples los requisitos minimos para empezar a trabajar con *The Crazy Agency* 💛\n\n"
            "Ahora cuéntame, ¿con qué aplicación deseas trabajar?  Nosotros de momento trabajamos con estas apps",
            reply_markup=botones_apps()
        )
        await state.set_state(RegistroStates.seleccion_app)
    
    elif any(x in texto for x in ["no", "No", "n", "not"]):
        await typing(message, 2)
        await state.clear()
        await message.answer(
            "Lo siento señorita 💛, necesitas disponibilidad para trabajar al menos unas 4 a 6 horas diarias 💸 con nosotros, por ahora necesitamos chicas para que generen bien.\n"
            "Si deseas volver a empezar cuando Tengas disponilidad de tiempo para trabajar, solo escribe *hola* o usa el comando /start 💎"
        )
        return

    else:
        await bot.send_message(
            GROUP_ID,
            f"⚠️ Respuesta no reconocida en *disponibilidad*\n"
            f"👤 @{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 {message.text}"
        )
        await message.answer("No entendí tu respuesta señorita 💎, ¿tienes disponibilidad?")

# Pregunta 4: Seleccionar App
@dp.message(RegistroStates.seleccion_app)
async def seleccionar_app(message: Message, state: FSMContext):
    texto = message.text.lower()
    # Si elige SUGO
    if "sugo" in texto:
        await typing(message, 2)
        # Puedes enviar una foto de ejemplo
        await bot.send_photo(
            message.chat.id,
            photo=url_static+"sugo-logo.png",  # Cambia por tu imagen real
            caption="💎 Esta es la app SUGO donde generarás ingresos 💸"
        )
        await typing(message, 2)
        # Imagen indicando dónde está el video
        await bot.send_photo(
            message.chat.id,
            photo=url_static+"pagina-sugo.png",
            caption="Perfecto señorita 💎\n"
                    "Antes de registrarte, debes ver el *video explicativo* de qué es SUGO.\n\n"
                    "Aquí tienes el contenido:\n"
                    "👉 Video explicativo (arriba en la página)\n\n"
                    "Haz clic aquí para verlo:\n"
                    "🔗 https://thecrazyagency.com/sugo/\n\n"
                    "💛 *IMPORTANTE:* Solo debes ver el video por ahora."
        )
        await typing(message, 10)
        await message.answer(
            "¿Ya viste el video completo señorita? 💎",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.vio_video_sugo)
        return

    # Si elige SALSA
    elif "salsa" in texto:
        await typing(message, 2)
        await message.answer(
            "Perfecto señorita 💎\n"
            "La app SALSA estará disponible muy pronto 💛\n"
            "Por ahora te recomendamos trabajar con SUGO 💸"
        )
        await message.answer(
            "👉 ¿Deseas registrarte en SUGO?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.esperando_disponibilidad)  # Reinicia flujo para Sugo
    else:
        await message.answer("No entendí señorita 💎, selecciona una app:")

# Pregunta 5: Si Confirma haber visto el video de que es SUGO
@dp.message(RegistroStates.vio_video_sugo)
async def validar_video_sugo(message: Message, state: FSMContext):
    texto = message.text.lower()
    # NO vio el video → repetir
    if any(x in texto for x in ["no", "n"]):
        await typing(message, 2)
        await message.answer(
            "Señorita 💛 debes ver el video antes de continuar.\n\n"
            "Aquí está nuevamente:\n"
            "🔗 https://thecrazyagency.com/sugo/\n\n"
            "Cuando termines, seleccione: *Sí 💎*",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.vio_video_sugo)
        return

    # SÍ vio el video → mostrar botón de registro
    elif any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)
        # Imagen del botón de registro
        await bot.send_photo(
            message.chat.id,
            photo=url_static+"pagina-sugo-1.png",
            caption="Perfecto señorita 💎\n Aquí está el botón para registrarte en nuestra plataforma 💸"
        )
        await typing(message, 2)  
        # Imagen de registro
        await bot.send_photo(
            message.chat.id,
            photo=url_static+"ejemplo-registro-streamer.png",
            caption="Ahora sí debes registrarte en el formulario oficial de nuestra plataforma:\n\n"
                    "🔗 https://thecrazyagency.com/usuarias/registrar/?from=sugo"
        )
        await typing(message, 10)
        await message.answer(
            "👉 ¿Nos confirmas si ya te registraste en nuestra plataforma?",
            reply_markup=botones_si_no()
        )
        await state.set_state(RegistroStates.registro_plataforma)
        return
    else:
        await message.answer("No entendí señorita 💎, ¿ya viste el video completo?")

###-------- REGISTRO DE LA STREAMER EN NUESTRA PLATAFORMA --------------###
@dp.message(RegistroStates.registro_plataforma)
async def validar_registro_plataforma(message: Message, state: FSMContext):
    texto = message.text.lower()    
    if any(x in texto for x in ["si", "sí", "s", "yes"]):
        await typing(message, 2)
        await message.answer(
            "Perfecto Señorita 💛\n"
            "Para confirmar tu registro, por favor escribenos tu *nombre* tal como pusiste en el formulario 💎"
        )
        await state.set_state(RegistroStates.pedir_nombre)
        return

#Pregunta 6: Se le pregunta el nombre para saber quien es en el registro y ver cual cuenta activar
@dp.message(RegistroStates.pedir_nombre)
async def recibir_nombre(message: Message, state: FSMContext):
    nombre = message.text.strip()
    # Guardar el nombre en el estado (opcional)
    await state.update_data(nombre=nombre)
    await typing(message, 2)
    # Notificar al grupo
    await bot.send_message(
        GROUP_ID,
        f"💎 *Nueva chica registrada en la plataforma para trabajar en SUGO* 💸\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {message.from_user.id}\n"
        f"📛 Nombre: *{nombre}*\n\n"
        f"⚠️ Deben activar su cuenta en la plataforma.\n\n"
        f"Para activarla usen:\n"
        f"/activar {message.from_user.id}"
    )
    # Mensaje para la chica
    await message.answer(
        f"Perfecto Señorita 💛\n"
        f"Gracias {nombre}.\n"
        "Tu registro fue enviado al equipo.\n"
        "En breve activarán tu cuenta para que puedas continuar con los cursos 💎💸"
    )
    # Guardamos que ya está esperando activación
    await state.set_state(RegistroStates.esperando_activacion)

@dp.message(RegistroStates.esperando_activacion)
async def esperando_activacion(message: Message, state: FSMContext):
    texto = message.text.lower()
    # Palabras que indican que solo está respondiendo
    if any(x in texto for x in ["ok", "gracias", "vale", "listo", "perfecto", "bueno", "entendido", "ok gracias", "oki", "okey"]):
        await typing(message, 2)
        await message.answer(
            "💛 Señorita, solo debemos esperar a que el equipo active tu cuenta.\n"
            "Apenas esté lista te avisaré por aquí 💎"
        )
        return

    # Si escribe otra cosa, igual la mantenemos en espera
    await message.answer(
        "Señorita 💛, ya enviamos tu registro al equipo.\n"
        "Apenas activen tu cuenta te avisaré por aquí 💎"
    )

###---------- FINALIZA EL PRIMERO CICLO DE REGISTRO ---------###


###---------- Estado cuando ya se le ha activado la cuenta en la plataforma a la streamer ---------###
@dp.message(F.text.startswith("/activar"))
async def activar_cuenta(message: Message):
    # Solo permitir que funcione en el grupo
    if message.chat.id != GROUP_ID:
        return
    
    try:
        # Extraer el ID de la chica
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("⚠️ Debes usar: /activar <telegram_id>")
            return
        
        user_id = int(parts[1])
        # Avisar en el grupo
        await message.reply(f"💛 La cuenta de la chica con ID {user_id} fue activada correctamente.")
        # Avisar a la chica - Imagen de cómo iniciar sesión
        await bot.send_photo(
            user_id,
            photo=url_static+"ejemplo-iniciar-streamer.png",
            caption="💛 Señorita, tu cuenta ya fue activada.\n\n"
                    "✨ Ya puedes iniciar sesión.\n\n"
                    "Aquí te explico cómo iniciar sesión 💎 en la plataforma :\n\n"
                    "Solo debes seleccionar su pais, su numero y el pin que añadiste como contraseña\n\n"
                    "🔗 https://thecrazyagency.com/usuarias/iniciar-sesion/"
        ) 
        await bot.send_photo(
            user_id,
            photo=url_static+"inicio-cursos-sugo.jpg",
            caption="Cuando entres verás tus cursos disponibles 💎💸 o bien puedes dirigirte al menu y buscar cursos."
        )

    except Exception as e:
        await message.reply(f"⚠️ Error activando la cuenta: {e}")
       
# Chica antigua
@dp.message(RegistroStates.antigua_pregunta)
async def antigua_pregunta(message: Message, state: FSMContext):
    texto = message.text
    await bot.send_message(
        GROUP_ID,
        f"📩 Mensaje de chica ANTIGUA 💎💸\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {message.from_user.id}\n\n"
        f"💬 {texto}"
    )
    await typing(message, 2)
    await message.answer(
        "Listo señorita 💛, ya envié tu mensaje al equipo.\n"
        "Una jefa o vicejefa te responderá pronto 💎"
    )
    await state.clear()

# Mensajes generales (reenviar al grupo)
@dp.message()
async def handle_message(message: Message):
    if message.chat.type == "private":
        user_id = message.from_user.id
        username = message.from_user.username or "SinUsername"
        user_map[user_id] = username

        text = (
            f"📩 Nuevo mensaje 💎💸\n"
            f"👤 Chica: @{username}\n"
            f"🆔 ID: {user_id}\n\n"
            f"💬 {message.text}"
        )
        await bot.send_message(GROUP_ID, text)

    elif message.chat.id == GROUP_ID and message.text.startswith("Resp:"):
        try:
            parts = message.text.split("\n", 1)
            user_id = int(parts[0].replace("Resp:", "").strip())
            respuesta = parts[1]
            await bot.send_message(user_id, respuesta)
        except:
            await bot.send_message(GROUP_ID, "⚠️ Formato incorrecto. Usa:\nResp: ID\nMensaje...")

async def main():
    print("💎 Bot corriendo... 💸")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
