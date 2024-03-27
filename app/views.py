from flask import render_template, request, jsonify
from app import app
from datetime import date
from app.models import Resultado

# Definimos las preguntas
preguntas_data = [
    {
        "pregunta": "¿Orina con más frecuencia de lo habitual?",
        "nombre": "orina_frecuente",
        "id": "p1",
    },
    {
        "pregunta": "¿La orina tiene un olor dulce o espumoso?",
        "nombre": "orina_olor_dulce",
        "id": "p2",
    },
    {
        "pregunta": "¿Siente una sed intensa y constante, incluso después de beber mucha agua?",
        "nombre": "sed_excesiva",
        "id": "p3",
    },
    {
        "pregunta": "¿Siente hambre más de lo habitual, incluso después de comer una comida completa?",
        "nombre": "hambre_excesiva",
        "id": "p4",
    },
    {
        "pregunta": "¿Ha tenido pérdida o aumento de peso inexplicable?",
        "nombre": "perdica_peso",
        "id": "p5",
    },
    {
        "pregunta": "¿Se siente cansado y sin energía la mayor parte del tiempo?",
        "nombre": "fatiga",
        "id": "p6",
    },
    {
        "pregunta": "¿Ha notado que su visión se ha vuelto borrosa o presenta dificultad para enfocar?",
        "nombre": "vision_borrosa",
        "id": "p7",
    },
    {
        "pregunta": "¿Ha notado manchas en los ojos como si fueran moscas volando?",
        "nombre": "manchas_ojos",
        "id": "p8",
    },
    {
        "pregunta": "¿Tiene algún familiar cercano (padres, hermanos, hijos) con diabetes?",
        "nombre": "familiar_diabetes",
        "id": "p9",
    },
    {
        "pregunta": "¿Lleva una vida sedentaria es decir no realiza al menos 30 minutos de actividad física moderada la mayoría de los días de la semana?",
        "nombre": "sedentarismo",
        "id": "p10",
    },
    {
        "pregunta": "¿Le han diagnosticado hipertensión arterial?",
        "nombre": "hipertension_arterial",
        "id": "p11",
    },
    {
        "pregunta": "¿Su nivel de colesterol HDL es inferior a 40 mg/dL?",
        "nombre": "colesterol_menor_40",
        "id": "p12",
    },
    {
        "pregunta": "¿Su nivel de triglicéridos es superior a 150 mg/dL?",
        "nombre": "trigliceridos_mayor_150",
        "id": "p13",
    },
    {
        "pregunta": "¿Tiene manchas oscuras en la piel, especialmente en los pliegues del cuerpo (axilas, cuello, ingles)?",
        "nombre": "manchas_oscuras",
        "id": "p14",
    },
    {
        "pregunta": "¿Le han diagnosticado Síndrome de Ovario Poliquístico?",
        "nombre": "sindrome_ovario_poliquistico",
        "id": "p15",
    },
    {
        "pregunta": "¿Ha experimentado hormigueo, picazón o adormecimiento en la piel?",
        "nombre": "hormigueo_piel",
        "id": "p16",
    },
    {
        "pregunta": "¿Ha tenido problemas para caminar debido a dolor en los pies?",
        "nombre": "dolor_pie",
        "id": "p17",
    },
    {
        "pregunta": "¿Ha notado manchas blancas en la lengua (candidiasis orofaríngea)?",
        "nombre": "marchas_blancas_lengua",
        "id": "p18",
    },
    {
        "pregunta": "¿Ha tenido o tiene heridas que tardan en cicatrizar?",
        "nombre": "heridas_tardan_cicatrizar",
        "id": "p19",
    },
    {
        "pregunta": "¿Ha experimentado irritabilidad o cambios en el estado de ánimo?",
        "nombre": "irritabilidad",
        "id": "p20",
    },
    {
        "pregunta": "¿Ha tenido infecciones urinarias frecuentes?",
        "nombre": "infecciones_urinarias",
        "id": "p21",
    },
    {
        "pregunta": "¿Ha tenido mareos o desmayos?",
        "nombre": "mareos",
        "id": "p22",
    },
    {
        "pregunta": "¿Ha notado disfunción sexual?",
        "nombre": "disfunción_sexual",
        "id": "p23",
    },
    {
        "pregunta": "¿Ha tenido algún infarto?",
        "nombre": "infarto",
        "id": "p24",
    },
    {
        "pregunta": "¿Ha sido diagnosticado con el VIH?",
        "nombre": "tiene_VIH",
        "id": "p25",
    },
    {
        "pregunta": "¿Se identifica como afrodescendiente o hispano?",
        "nombre": "afrodescendiente",
        "id": "p26",
    }
]

# Definimos las bases de conocimiento para los diferentes factores de riesgo
base_conocimiento_factores_riesgo_modificables = {
    "obesidad_o_sobrepeso": False,
    "sedentarismo": False,
    "colesterol_menor_40": False,
    "trigliceridos_mayor_150": False,
    "hipertension_arterial": False,
}

base_conocimiento_factores_riesgo_no_modificables = {
    "mayor_45_anios": False,
    "familiar_diabetes": False,
    "afrodescendiente": False,
    "es_mujer": False,
    "tiene_VIH": False,
}

base_conocimiento_sintomas_signos_2_puntos = {
    "vision_borrosa": False,
    "fatiga": False,
    "irritabilidad": False,
    "infecciones_urinarias": False,
    "mareos": False,
    "disfunción_sexual": False,
    "perdica_peso": False,
    "sindrome_ovario_poliquistico": False,
    "manchas_ojos": False,
    "infarto": False,
}

base_conocimiento_sintomas_signos_3_puntos = {
    "hambre_excesiva": False,
    "sed_excesiva": False,
    "orina_frecuente": False,
    "manchas_oscuras": False,
    "hormigueo_piel": False,
    "dolor_pie": False,
    "marchas_blancas_lengua": False,
    "heridas_tardan_cicatrizar": False,
    "orina_olor_dulce": False,
}

# Función para la ruta '/'
@app.route('/')
def index():
    return render_template('index.html', preguntas = preguntas_data)

# Función para la ruta '/evaluar'
@app.route("/evaluar", methods=["POST"])
def evaluate():   
    # Se obtienen los datos del formulario
    sexo = request.form["sexo"]
    nombre = request.form["nombre"]
    fecha_nacimiento =request.form["fechaNacimiento"]
    talla = request.form["talla"]
    peso = request.form["peso"]
    
    # Se calcula la edad y el IMC
    edad = calcular_edad(fecha_nacimiento)
    imc = calcular_imc(talla, peso)

    # Se determina si el usuario es mayor de 45 años y si tiene sobrepeso u obesidad
    mayor45Anios = edad >= 45
    obesidadOSobrepeso = imc >= 25
    esMujer = sexo == "2"
    txtSexo = "Masculino" if sexo == "1" else "Femenino"

    # Se actualiza la base de conocimiento con las respuestas del usuario
    preguntas_dict = {'mayor_45_anios': mayor45Anios, 'obesidad_o_sobrepeso': obesidadOSobrepeso, 'es_mujer': esMujer}
    for pregunta in preguntas_data:  
        pregunta_id = pregunta["id"]
        pregunta_nombre = pregunta["nombre"]
        pregunta_value = request.form.get(pregunta_id)
        preguntas_dict[pregunta_nombre] = pregunta_value == "1"
    
    # Se realiza el diagnóstico
    resultado = diagnosticar(preguntas_dict)

    # Se preparan las respuestas para mostrar al usuario
    respuestas = []
    for clave, valor in preguntas_dict.items():
        if (convertir_a_frase(clave, valor) != None):
            respuestas.append(convertir_a_frase(clave, valor))

    definicion_imc = obtener_definicion_imc(imc)

    # Se crea el objeto Resultado
    resultado = Resultado(resultado = resultado, nombre=nombre, edad=edad,sexo= txtSexo, talla=talla, peso=peso, imc=round(imc, 2), definicion_imc=definicion_imc, datosProporcionados = respuestas)

    # Se muestra la página de resultados
    return render_template("resultado.html", resultado=resultado)

# Función para convertir una clave y un valor en una frase
def convertir_a_frase(clave, valor):
    pregunta = buscar_pregunta(clave)

    if(pregunta != ""):
        return {
            "pregunta": pregunta,
            "respuesta": "SÍ" if valor else "NO" 
        }

# Función para buscar una pregunta por su nombre
def buscar_pregunta(clave):
    for pregunta in preguntas_data:
        if pregunta["nombre"] == clave:
            return pregunta["pregunta"]

    return ""

# Función para diagnosticar el riesgo de diabetes
def diagnosticar(preguntas_dict):
    puntaje_total = 0
    for key, value in preguntas_dict.items():
        if key in base_conocimiento_factores_riesgo_modificables:
            base_conocimiento_factores_riesgo_modificables[key] = value
        elif key in base_conocimiento_factores_riesgo_no_modificables:
            base_conocimiento_factores_riesgo_no_modificables[key] = value
        elif key in base_conocimiento_sintomas_signos_2_puntos:
            base_conocimiento_sintomas_signos_2_puntos[key] = value
        elif key in base_conocimiento_sintomas_signos_3_puntos:
            base_conocimiento_sintomas_signos_3_puntos[key] = value
    
    for key, value in base_conocimiento_factores_riesgo_modificables.items():
        if value:
            puntaje_total += 1

    for key, value in base_conocimiento_factores_riesgo_no_modificables.items():
        if value:
            puntaje_total += 2

    for key, value in base_conocimiento_sintomas_signos_2_puntos.items():
        if value:
            puntaje_total += 2

    for key, value in base_conocimiento_sintomas_signos_3_puntos.items():
        if value:
            puntaje_total += 3
    
    if(puntaje_total >= 0 and puntaje_total <= 25):
        return "Bajo riesgo de diabetes."
    elif (puntaje_total <= 30):
        return "Riesgo moderado de diabetes."
    elif (puntaje_total <= 61):
        return "Alto riesgo de diabetes."
    else:
        return "No se tiene suficiente evidencia para dar un resultado."


# Función para calcular la edad
def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

# Función para calcular el IMC
def calcular_imc(talla, peso):
    imc = float(peso) / (float(talla) ** 2)
    return imc

# Función para obtener la definición del IMC
def obtener_definicion_imc(imc):
    if (imc < 18.5):
        return "Bajo peso"
    elif (imc >= 18.5 and imc <= 24.9):
        return "Adecuado"
    elif (imc >= 25 and imc <= 29.9):
        return "Sobrepeso"
    elif (imc >= 30 and imc <= 34.9):
        return "Obesidad grado 1"
    elif (imc >= 35 and imc <= 39.9):
        return "Obesidad grado 2"
    else:
        return "Obesidad grado 3"