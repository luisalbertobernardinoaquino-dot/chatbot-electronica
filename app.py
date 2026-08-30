from flask import Flask, request, render_template_string, session, redirect, url_for
from google import genai
from google.genai import types
import os
import re
from datetime import datetime

from zoneinfo import ZoneInfo

from hmac import compare_digest
app = Flask(__name__)

historial_preguntas = []

app.secret_key = os.environ.get("SECRET_KEY")
def limpiar_respuesta(texto):

    if not texto:
        return ""

    # Quitar Markdown
    texto = texto.replace("**", "")
    texto = texto.replace("__", "")
    texto = texto.replace("###", "")
    texto = texto.replace("##", "")
    texto = texto.replace("#", "")
    texto = texto.replace("```", "")
    texto = texto.replace("$$", "")
    texto = texto.replace("$", "")

    # Convertir expresiones LaTeX comunes
    texto = texto.replace("\\Omega", "Ω")
    texto = texto.replace("\\times", "×")
    texto = texto.replace("\\cdot", "×")
    texto = texto.replace("\\text", "")
    texto = texto.replace("\\mathrm", "")

    # Convertir fracciones sencillas
    texto = re.sub(
        r'\\frac\{([^{}]+)\}\{([^{}]+)\}',
        r'(\1) / (\2)',
        texto
    )

    # Quitar llaves de LaTeX
    texto = texto.replace("{", "")
    texto = texto.replace("}", "")

    # Limpiar barras LaTeX restantes
    texto = texto.replace("\\", "")

    # Evitar demasiados saltos de línea
    texto = re.sub(r'\n{3,}', '\n\n', texto)

    return texto.strip()

def responder(pregunta):

    if not pregunta.strip():
        return "Por favor escribe una pregunta."

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "BernaBOT todavía no tiene configurada la clave de inteligencia artificial."

    try:

        client = genai.Client(api_key=api_key)

        respuesta = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=pregunta,

            config=types.GenerateContentConfig(

                system_instruction="""
                Eres BernaBOT, un asistente educativo especializado en
                electrónica, circuitos eléctricos, electrónica analógica,
                electrónica digital y microcontroladores.

                Tu función es apoyar a estudiantes universitarios de ingeniería.

                Responde siempre en español.

                Explica de manera clara, didáctica y técnicamente correcta.

                Cuando el usuario solicite resolver un problema numérico:

                1. Identifica los datos.
                2. Indica qué se desea calcular.
                3. Escribe la fórmula correspondiente.
                4. Sustituye los valores.
                5. Realiza el cálculo paso a paso.
                6. Indica correctamente las unidades.
                7. Explica brevemente qué significa el resultado.

                Tienes conocimientos principalmente sobre:

                - Ley de Ohm
                - Leyes de Kirchhoff
                - Resistencias
                - Capacitores
                - Inductores
                - Diodos
                - Transistores
                - Amplificadores operacionales
                - Circuitos eléctricos
                - Electrónica analógica
                - Electrónica digital
                - Compuertas lógicas
                - Flip-Flops
                - Contadores
                - Registros
                - GAL y dispositivos lógicos programables
                - WinCUPL
                - Microcontroladores
                - PIC
                - Fuentes de alimentación
                - Rectificadores
                - Tiristores
                - PWM
                - Temporizador 555
                - Osciladores
                - Instrumentación electrónica
                - Multímetros
                - Osciloscopios
                - Generadores de funciones

                Cuando una pregunta tenga relación con un circuito,
                explica también el funcionamiento físico del circuito.

                Si existen varias formas de resolver un problema,
                comienza por el método más sencillo para un estudiante.

                No inventes valores que no hayan sido proporcionados.
                Si falta información necesaria para realizar un cálculo,
                indícalo.

                Cuando sea conveniente, utiliza ecuaciones.

                Tu nombre es BernaBOT.

                IMPORTANTE PARA EL FORMATO DE RESPUESTA:

No utilices Markdown.
No utilices símbolos como **, ### o ``` .
No utilices LaTeX ni expresiones como \text{}, \frac{}, $$ o \( \).

Escribe las ecuaciones en texto sencillo y fácil de leer.

Ejemplo:

V = I × R

R = V / I

R = 10 V / 0.02 A

R = 500 Ω

Separa cada sección utilizando saltos de línea.
Utiliza títulos sencillos como:

DATOS:
FÓRMULA:
SUSTITUCIÓN:
RESULTADO:
CONCLUSIÓN:

REGLA DE FORMATO OBLIGATORIA:

Devuelve únicamente texto plano.

NO utilices Markdown.
NO utilices LaTeX.
NO utilices ** para negritas.
NO utilices # ni ### para títulos.
NO utilices símbolos $.
NO utilices comandos como \frac, \text, \Omega o similares.

Para escribir fórmulas utiliza texto normal.

Ejemplo correcto:

DATOS:

Voltaje de fuente = 12 V
Voltaje del LED = 2 V
Corriente = 20 mA = 0.02 A

FÓRMULA:

R = (Vfuente - Vled) / I

SUSTITUCIÓN:

R = (12 V - 2 V) / 0.02 A

RESULTADO:

R = 500 Ω

                """,

                temperature=0.3,

                max_output_tokens=1200
            )
        )

        return limpiar_respuesta(respuesta.text)

    except Exception as error:

        print("ERROR EN BERNABOT:", error)

        return "Ocurrió un problema al consultar la inteligencia artificial. Intenta nuevamente."



html = """
<!DOCTYPE html>
<html>
<head>
<title>BernaBOT UAG</title>

<style>






.buho-container{
    position:fixed;
    right:25px;
    bottom:25px;
    display:flex;
    align-items:flex-end;
    gap:12px;
    z-index:1000;
}

.buho{
    width:110px;
    animation: flotar 2.5s ease-in-out infinite;
}

.globo-bienvenida{
    background:white;
    color:#333;
    padding:14px 18px;
    border-radius:18px 18px 4px 18px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.2);
    max-width:260px;
    font-size:15px;
    text-align:left;
    border-left:5px solid #7B1E3A;
    animation: aparecer 1s ease;
}

.globo-bienvenida b{
    color:#7B1E3A;
}

@keyframes flotar{
    0%{
        transform:translateY(0px);
    }
    50%{
        transform:translateY(-10px);
    }
    100%{
        transform:translateY(0px);
    }
}

@keyframes aparecer{
    from{
        opacity:0;
        transform:translateX(20px);
    }
    to{
        opacity:1;
        transform:translateX(0px);
    }
}

@media screen and (max-width: 768px){
    .buho-container{
        right:10px;
        bottom:10px;
        flex-direction:column;
        align-items:flex-end;
    }

    .buho{
        width:80px;
    }

    .globo-bienvenida{
        max-width:210px;
        font-size:13px;
    }
}







body{
    margin:0;
    font-family:Arial, Helvetica, sans-serif;
    background:linear-gradient(180deg,#f6f8fb 0%,#eef2f7 100%);
}

/* ENCABEZADO PROFESIONAL */

.header-container{
    padding:12px 20px 5px 20px;
}

.header-card{
    background:white;
    border-radius:18px;
    box-shadow:0px 8px 24px rgba(0,0,0,0.18);
    overflow:hidden;
    max-width:1500px;
    margin:auto;
    position:relative;
}

.header-main{
    display:flex;
    align-items:center;
    padding:18px 28px 10px 28px;
}

.logo-box{
    width:25%;
    min-width:180px;
    text-align:center;
    border-right:2px solid #7B1E3A;
    padding-right:20px;
}

.logo-uag{
    width:80%;
    max-width:240px;
    height:auto;
}

.header-text{
    width:68%;
    text-align:center;
    padding-left:34px;
}

.header-title{
    color:#7B1E3A;
    font-size:22px;
    font-weight:900;
    letter-spacing:1px;
    margin-bottom:8px;
}

.campus-line{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:12px;
    margin-bottom:10px;
}

.line-orange{
    height:3px;
    width:140px;
    background:#F28C28;
}

.campus{
     color:#7B1E3A;
    font-size:17px;
    letter-spacing:5px;
    font-weight:500;
}

.bot-bar{
    background:linear-gradient(90deg,#7B001B,#9A1233,#7B001B);
    color:white;
    font-size:15px;
    font-weight:bold;
    letter-spacing:1px;
    border-radius:8px;
    padding:10px 14px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.18);
}

.header-wave{
    height:26px;
    background:#7B001B;
    position:relative;
}

.header-wave:before{
    content:"";
    position:absolute;
    top:-12px;
    left:-5%;
    width:110%;
    height:30px;
    background:#F28C28;
    border-radius:0 0 50% 50%;
}

.header-wave:after{
    content:"";
    position:absolute;
    top:-8px;
    left:-5%;
    width:110%;
    height:28px;
    background:white;
    border-radius:0 0 50% 50%;
}

/* CONTENIDO */

.contenido{
    margin:35px;
    text-align:center;
}

.caja{
    background:white;
    width:70%;
    margin:auto;
    padding:35px;
    border-radius:14px;
    box-shadow:0px 5px 18px rgba(0,0,0,0.12);
}

.caja h2{
    margin-top:0;
    font-size:28px;
}

.caja p{
    font-size:17px;
}

.formulario{
    margin-top:28px;
}

input[type=text]{
    width:55%;
    height:46px;
    font-size:16px;
    border-radius:8px;
    border:1px solid #c9c9c9;
    padding-left:14px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

input[type=submit]{
    height:49px;
    border:none;
    border-radius:8px;
    background:#7B1E3A;
    color:white;
    padding:0px 28px;
    cursor:pointer;
    font-size:16px;
    font-weight:bold;
    margin-left:10px;
}

input[type=submit]:hover{
    background:#9A2749;
}

.respuesta{
    margin:20px auto;
    background:#ffffff;
    padding:25px 30px;
    border-radius:12px;
    width:70%;
    box-shadow:0px 4px 12px rgba(0,0,0,0.12);
    text-align:left;
    line-height:1.5;
    white-space:normal !important;
}

/* TITULOS PREGUNTA Y RESPUESTA */
.respuesta h3{
    margin:0 0 8px 0 !important;
    padding:0 !important;
    font-size:22px;
    line-height:1.3;
}

/* TEXTO DE LA PREGUNTA */
.respuesta .pregunta{
    color:#7B1E3A;
    font-weight:bold;
    margin:0 0 22px 25px !important;
    padding:0 !important;
    line-height:1.5;
    white-space:normal !important;
}

/* TEXTO GENERADO POR BERNABOT */
.texto-respuesta{
    white-space:pre-wrap;
    font-family:Georgia, "Times New Roman", serif;
    font-size:17px;
    line-height:1.6;
    margin:0 0 0 25px !important;
    padding:0 !important;
}
.texto-respuesta{
    white-space:pre-wrap;
    font-family:Georgia, "Times New Roman", serif;
    font-size:17px;
    line-height:1.6;
    margin-top:10px;
}


/* RESPONSIVE */

@media screen and (max-width: 900px){

    .header-main{
        flex-direction:column;
        padding:28px 22px 18px 22px;
    }

    .logo-box{
        width:100%;
        border-right:none;
        border-bottom:2px solid #7B1E3A;
        padding-right:0;
        padding-bottom:18px;
        margin-bottom:18px;
    }

    .logo-uag{
        max-width:300px;
    }

    .header-text{
        width:100%;
        padding-left:0;
    }

    .header-title{
        font-size:26px;
    }

    .campus{
        font-size:18px;
        letter-spacing:5px;
    }

    .line-orange{
        width:80px;
    }

    .bot-bar{
        font-size:16px;
    }

    .caja{
        width:90%;
        padding:25px;
    }

    input[type=text]{
        width:90%;
        margin-bottom:12px;
    }

    input[type=submit]{
        margin-left:0;
        width:92%;
    }

    .respuesta{
        width:90%;
    }
}

/* TITULOS DE LA SOLUCION */
.titulo-seccion{
    font-weight:bold;
    font-family:Arial, sans-serif;
    font-size:20px;
    color:#7B1E3A;
    margin:18px 0 8px 0;
}

/* TEXTO EXPLICATIVO */
.parrafo-respuesta{
    font-family:Georgia, "Times New Roman", serif;
    font-size:17px;
    line-height:1.7;
    text-indent:28px;
    margin:6px 0;
    color:#222;
}

/* RECUADRO PARA FORMULAS */
.formula-box{
    max-width:520px;
    margin:16px auto;
    padding:14px 20px;
    background:#f8f8f8;
    border:1px solid #d8d8d8;
    border-left:6px solid #7B1E3A;
    border-radius:12px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.10);
    text-align:center;
    font-family:"Cambria Math", Georgia, serif;
    font-size:26px;
    font-weight:bold;
    color:#111;
}

/* PEQUEÑA SEPARACION ENTRE BLOQUES */
.espacio-respuesta{
    height:8px;
}

</style>




</head>

<body>

<div class="header-container">

    <div class="header-card">

        <div class="header-main">

            <div class="logo-box">
                <img src="/static/uaglogo.png" class="logo-uag" alt="Logo UAG">
            </div>

            <div class="header-text">

                <div class="header-title">
                    UNIVERSIDAD AUTÓNOMA DE GUADALAJARA
                </div>

                <div class="campus-line">
                    <div class="line-orange"></div>
                    <div class="campus">CAMPUS TABASCO</div>
                    <div class="line-orange"></div>
                </div>

                <div class="bot-bar">
                    BernaBOT / CHATBOT DE ELECTRÓNICA Y CIRCUITOS ELÉCTRICOS
                </div>

            </div>

        </div>

        <div class="header-wave"></div>

    </div>

</div>

<div class="contenido">

    <div class="caja">

        <h2>Bienvenido al Chatbot de Electrónica y Circuitos Electricos</h2>

        <p>Escribe una pregunta relacionada con electrónica o circuitos eléctricos o pega una imagen de un circuito.</p>

 <form method="POST" class="formulario" id="formulario-bernabot">

    <input
        type="text"
        name="pregunta"
        id="pregunta"
        placeholder="Escribe tu pregunta aquí..."
        required
    >

    <input
        type="submit"
        id="boton-preguntar"
        value="Preguntar"
    >

</form>

<div id="estado-bernabot"></div>


    </div>

{% if pregunta %}

<div class="respuesta">

    <h3>Pregunta</h3>

    <p class="pregunta">
        {{ pregunta }}
    </p>

    <h3>Respuesta</h3>

<div class="texto-respuesta" id="texto-respuesta">
    {{ respuesta }}
</div>

</div>

{% endif %}

</div>







<div class="buho-container">

{% if not respuesta %}
<div class="globo-bienvenida">
    <b>Hola, soy BernaBOT.</b><br>
    Puedo ayudarte con Ley de Ohm, Kirchhoff, resistencias, diodos, transistores y circuitos eléctricos.
</div>
{% endif %}

    <img src="/static/uag.png" class="buho" alt="BernaBOT">

</div>




<script>

window.addEventListener("load", function(){

    if (window.history.replaceState) {
        window.history.replaceState(null, "", "/");
    }

});

</script>

<script>
    const navegacion = performance.getEntriesByType("navigation")[0];

    if (navegacion && navegacion.type === "reload") {
        window.location.replace("/");
    }
</script>

<script>

const formulario = document.getElementById("formulario-bernabot");
const estado = document.getElementById("estado-bernabot");
const boton = document.getElementById("boton-preguntar");

formulario.addEventListener("submit", async function(evento) {

    evento.preventDefault();

    estado.innerHTML = "BernaBOT está procesando tu pregunta. Por favor espera...";
    boton.disabled = true;
    boton.value = "Procesando...";

    const datos = new FormData(formulario);

    try {

        const respuesta = await fetch("/", {
            method: "POST",
            body: datos
        });

        if (!respuesta.ok) {
            throw new Error("Error del servidor");
        }

        const html = await respuesta.text();

        document.open();
        document.write(html);
        document.close();

    } catch (error) {

        estado.innerHTML =
            "BernaBOT está tardando más de lo normal en responder. " +
            "Por favor intenta realizar nuevamente tu pregunta.";

        boton.disabled = false;
        boton.value = "Preguntar";
    }

});

</script>


</body>

</html>
"""












@app.route("/admin")
def admin_panel():

    if not session.get("admin"):
        return redirect("/admin/login")

    hoy_fecha = datetime.now(
        ZoneInfo("America/Merida")
    ).strftime("%d/%m/%Y")

    preguntas_hoy = sum(
        1 for item in historial_preguntas
        if item["fecha"] == hoy_fecha
    )

    total_preguntas = len(historial_preguntas)

    preguntas_recientes = list(
        reversed(historial_preguntas[-10:])
    )

    seccion = request.args.get("seccion", "")

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">

    <head>

        <meta charset="UTF-8">

        <title>Panel BernaBOT</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
            }

            .encabezado {
                background: #7B1E3A;
                color: white;
                text-align: center;
                padding: 25px;
            }

            .contenedor {
                width: 85%;
                max-width: 900px;
                margin: 35px auto;
            }

            .hoy {
                background: white;
                padding: 25px;
                text-align: center;
                border-radius: 12px;
                margin-bottom: 25px;
            }

            .numero {
                font-size: 45px;
                font-weight: bold;
                color: #7B1E3A;
            }

            .menu {
                display: block;
                background: white;
                padding: 20px;
                margin-bottom: 12px;

                border-radius: 10px;
                border-left: 7px solid #7B1E3A;

                text-decoration: none;

                color: #333;

                font-size: 18px;
                font-weight: bold;
            }

            .menu:hover {
                background: #f8edf1;
            }

            .resultado {

                background: white;

                padding: 25px;

                margin-top: 25px;

                border-radius: 10px;

                border-top: 5px solid #7B1E3A;
            }

            .pregunta {

                padding: 12px 0;

                border-bottom: 1px solid #ddd;
            }

            .fecha {

                color: #777;

                font-size: 14px;

                margin-top: 5px;
            }

            .botones {

                text-align: center;

                margin-top: 30px;
            }

            .boton {

                display: inline-block;

                background: #7B1E3A;

                color: white;

                padding: 12px 22px;

                margin: 5px;

                text-decoration: none;

                border-radius: 7px;
            }

            .salir {
                background: #555;
            }

        </style>

    </head>

    <body>


        <div class="encabezado">

            <h1>BernaBOT</h1>

            <p>Panel de Administración</p>

        </div>


        <div class="contenedor">


            <div class="hoy">

                <h2>Preguntas realizadas hoy</h2>

                <div class="numero">

                    {{ preguntas_hoy }}

                </div>

            </div>


            <a class="menu"
               href="/admin?seccion=total">

                1. Preguntas realizadas en total

            </a>


            <a class="menu"
               href="/admin?seccion=temas">

                2. Temas más consultados

            </a>


            <a class="menu"
               href="/admin?seccion=historial">

                3. Historial de preguntas recientes

            </a>


            <a class="menu"
               href="/admin?seccion=fechas">

                4. Fecha y hora de cada pregunta

            </a>



            {% if seccion == "total" %}

                <div class="resultado">

                    <h2>Preguntas realizadas en total</h2>

                    <div class="numero">

                        {{ total_preguntas }}

                    </div>

                </div>

            {% endif %}



            {% if seccion == "temas" %}

                <div class="resultado">

                    <h2>Temas más consultados</h2>

                    <p>
                        Estadística de temas disponible próximamente.
                    </p>

                </div>

            {% endif %}



            {% if seccion == "historial" %}

                <div class="resultado">

                    <h2>
                        Historial de preguntas recientes
                    </h2>


                    {% if preguntas_recientes %}


                        {% for item in preguntas_recientes %}

                            <div class="pregunta">

                                <strong>

                                    {{ item.pregunta }}

                                </strong>

                                <div class="fecha">

                                    {{ item.fecha }}
                                    -
                                    {{ item.hora }}

                                </div>

                            </div>

                        {% endfor %}


                    {% else %}


                        <p>

                            Todavía no se han realizado preguntas.

                        </p>


                    {% endif %}


                </div>

            {% endif %}



            {% if seccion == "fechas" %}

                <div class="resultado">

                    <h2>
                        Fecha y hora de cada pregunta
                    </h2>


                    {% if preguntas_recientes %}


                        {% for item in preguntas_recientes %}

                            <div class="pregunta">

                                <strong>

                                    {{ item.fecha }}
                                    -
                                    {{ item.hora }}

                                </strong>

                                <br><br>

                                {{ item.pregunta }}

                            </div>

                        {% endfor %}


                    {% else %}

                        <p>

                            No existen registros todavía.

                        </p>

                    {% endif %}

                </div>

            {% endif %}



            <div class="botones">

                <a href="/"
                   class="boton">

                    Ver BernaBOT

                </a>


                <a href="/admin/logout"
                   class="boton salir">

                    Cerrar sesión

                </a>

            </div>


        </div>

    </body>

    </html>
    """,
    preguntas_hoy=preguntas_hoy,
    total_preguntas=total_preguntas,
    preguntas_recientes=preguntas_recientes,
    seccion=seccion
    )




@app.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(url_for("admin_login"))
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = ""

    if request.method == "POST":
        password = request.form.get("password", "")
        admin_password = os.environ.get("ADMIN_PASSWORD", "")

        if admin_password and compare_digest(password, admin_password):
            session["admin"] = True
            return redirect(url_for("admin_panel"))

        error = "Contraseña incorrecta."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Administrador - BernaBOT</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .login {
                background: white;
                padding: 35px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                width: 320px;
                text-align: center;
            }

            input {
                width: 90%;
                padding: 12px;
                margin: 15px 0;
                border: 1px solid #ccc;
                border-radius: 6px;
            }

            button {
                background: #0066cc;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 6px;
                cursor: pointer;
            }

            .error {
                color: red;
            }
        </style>
    </head>

    <body>

        <div class="login">
            <h2>BernaBOT</h2>
            <h3>Panel de administrador</h3>

            <form method="POST">

                <input
                    type="password"
                    name="password"
                    placeholder="Contraseña"
                    required
                >

                <br>

                <button type="submit">
                    Ingresar
                </button>

            </form>

            {% if error %}
                <p class="error">{{ error }}</p>
            {% endif %}

        </div>

    </body>
    </html>
    """, error=error)
@app.route("/", methods=["GET","POST"])
def inicio():

    pregunta = ""
    respuesta = ""

    if request.method == "POST":
        pregunta = request.form["pregunta"]

 if pregunta.strip():
        ahora = datetime.now(ZoneInfo("America/Merida"))

        historial_preguntas.append({
            "pregunta": pregunta.strip(),
            "fecha": ahora.strftime("%d/%m/%Y"),
            "hora": ahora.strftime("%H:%M")
        })

        if len(historial_preguntas) > 50:
            historial_preguntas.pop(0)
        
        respuesta = responder(pregunta)

    return render_template_string(
        html,
        pregunta=pregunta,
        respuesta=respuesta
    )


if __name__ == "__main__":
    app.run(debug=True)
