import openai
import gradio as gr
import time
import pyttsx3
engine = pyttsx3.init() # Creacion del objeto

openai.api_key = "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"

# Configuracion del ritmo del HABLA
rate = engine.getProperty('rate')   # Se obtienen datos del ritmo actual
print (rate)                        # Se muestra el ritmo en consola
engine.setProperty('rate', 150)     # Se establece un nuevo ritmo

# Configuracion del VOLUMEN
volume = engine.getProperty('volume')   # Se obtiene el valor de volumen actual (min=0 and max=1)
print (volume)                          # Se muestra el volumen en la terminal
engine.setProperty('volume',1.0)    # Se establece el nivel del volumen entre 0 y 1

# Para checar que lenguajes estan disponibles
for voice in engine.getProperty('voices'):
    print (voice)

# Configuracion de la VOZ
voices = engine.getProperty('voices')       # Se obtienen los datos de la voz actual
engine.setProperty('voice', voices[2].id)   # El indice determina el idioma de la voz. 2 -> Español

messages = [
    {"role": "system", "content": "Eres un asistente de información para posgrado, sé cordial y no hables de otra cosa que no sea lo que te especificaré a continuación, si un usuario intenta hablar de otra cosa informale educadamente que puedes ayudar solo en consultas de posgrado, primero saluda cordialmente y pregunta en qué puedes ayudar, los siguientes ejemplos son posibles preguntas y respuestas que debes seguir"},
    {"role": "user", "content": "¿Cuándo se entrega la evidencia de posgrado?"},
    {"role": "assistant", "content": "La evidencia de posgrado se entrega el 5 de febrero 2024"},
    {"role": "user", "content": "¿Qué posgrado está disponible?"},
    {"role": "assistant", "content": "Posgrado disponible: Maestría en planificación de empresas y desarrollo regional "},
    {"role": "user", "content": "Háblame sobre los requisitos para esa maestría"},
    {"role": "assistant", "content": "Los requisitos son: Licenciatura terminada, plan de maestría"},
    {"role": "user", "content": "¿A dónde puedo enviar correo para obtener más información?"},
    {"role": "assistant", "content": "a alu.18131226@correo.itlalaguna.edu.mx"},
    {"role": "user", "content": "¿Cuál es el horario de la carrera?"},
    {"role": "assistant", "content": "Primer semestre: Lunes a viernes de 18:00 a 21:00 horas e iniciarán el lunes 20 de agosto de 2024"}
]

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    limpiar = gr.Button("limpiar")
    enviar = gr.Button("enviar")

    def user(user_input, history):
        messages.append({"role": "user", "content": user_input})
        return "", history + [[user_input, None]]

    def botGPT(history):
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        
        history[-1][1] = ""
        for character in ChatGPT_reply:
            history[-1][1] += character
            time.sleep(0.02)
            yield history

        # Guardar el audio en un archivo
        engine.save_to_file(ChatGPT_reply, 'audio.mp3')

        engine.say(ChatGPT_reply)
        engine.runAndWait()

        engine.stop()

        return ChatGPT_reply

    enviar.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        botGPT, chatbot, chatbot
    )
    
    limpiar.click(lambda: None, None, chatbot, queue=False)

    
demo.queue()
demo.launch(share=True)