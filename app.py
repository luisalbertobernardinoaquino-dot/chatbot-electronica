from flask import Flask, request, render_template_string

app = Flask(__name__)

def responder(pregunta):

    pregunta = pregunta.lower()

    if "ley de ohm" in pregunta:
        return "La Ley de Ohm establece que V = I × R"

    elif "kirchhoff" in pregunta:
        return "Las leyes de Kirchhoff permiten analizar corrientes y voltajes en circuitos."

    elif "resistencia" in pregunta:
        return "La resistencia se mide en Ohms (Ω)."

    elif "diodo" in pregunta:
        return "Un diodo permite el paso de corriente en una sola dirección."

    elif "transistor" in pregunta:
        return "Un transistor puede funcionar como amplificador o interruptor."

    else:
        return "Lo siento, aún no conozco esa respuesta."


html = """
<!DOCTYPE html>
<html>
<head>
<title>CircuitBot UAG</title>

<style>

body{
    margin:0;
    font-family:Arial, Helvetica, sans-serif;
    background:#f4f6f9;
}

.header{
    background:#7B1E3A;
    color:white;
    display:flex;
    align-items:center;
    padding:15px 30px;
    box-shadow:0px 3px 8px gray;
}

.logo{
    width:80px;
    margin-right:20px;
    border-radius:10px;
    background:white;
    padding:5px;
}

.titulo{
    font-size:30px;
    font-weight:bold;
}

.subtitulo{
    font-size:18px;
    margin-top:5px;
}

.contenido{
    margin:40px;
    text-align:center;
}

.caja{
    background:white;
    width:75%;
    margin:auto;
    padding:30px;
    border-radius:12px;
    box-shadow:0px 2px 10px lightgray;
}

input[type=text]{
    width:500px;
    height:40px;
    font-size:16px;
    border-radius:8px;
    border:1px solid gray;
    padding-left:10px;
}

input[type=submit]{
    height:44px;
    border:none;
    border-radius:8px;
    background:#7B1E3A;
    color:white;
    padding:0px 20px;
    cursor:pointer;
    font-size:16px;
}

input[type=submit]:hover{
    background:#9A2749;
}

.respuesta{
    margin-top:30px;
    background:#ffffff;
    padding:20px;
    border-radius:10px;
    width:70%;
    margin-left:auto;
    margin-right:auto;
    box-shadow:0px 2px 8px lightgray;
    text-align:left;
}

.pregunta{
    color:#7B1E3A;
    font-weight:bold;
}

</style>

</head>

<body>

<div class="header">

<img src="/static/uag.png" class="logo">

<div>
    <div class="titulo">UNIVERSIDAD AUTÓNOMA DE GUADALAJARA</div>
    <div class="subtitulo">BernaBOT UAG | Chatbot de Electronica y Circuitos Electricos</div>
</div>

</div>

<div class="contenido">

<div class="caja">

<h2>Bienvenido al Chatbot de Electrónica</h2>

<p>Escribe una pregunta relacionada con electrónica o circuitos eléctricos.</p>

<form method="POST">

    <input type="text" name="pregunta" placeholder="Escribe tu pregunta aquí...">

    <input type="submit" value="Preguntar">

</form>

</div>

{% if pregunta %}

<div class="respuesta">

<h3>Pregunta</h3>

<p class="pregunta">{{ pregunta }}</p>

<h3>Respuesta</h3>

<p>{{ respuesta }}</p>

</div>

{% endif %}

</div>

</body>

</html>
"""


@app.route("/", methods=["GET","POST"])
def inicio():

    pregunta = ""
    respuesta = ""

    if request.method == "POST":
        pregunta = request.form["pregunta"]
        respuesta = responder(pregunta)

    return render_template_string(
        html,
        pregunta=pregunta,
        respuesta=respuesta
    )


if __name__ == "__main__":
    app.run(debug=True)
