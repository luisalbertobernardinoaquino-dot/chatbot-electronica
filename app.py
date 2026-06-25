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
    <title>Chatbot de Electrónica</title>
</head>
<body>

<h1>UNIVERSIDAD AUTONOMA DE GUADALAJARA</h1>

<h1>BIENVENIDOS AL CHATBOT DE LA MATERIA DE CIRCUITOS ELECTRICOS</h1>

<form method="POST">
    <input type="text" name="pregunta" size="50" placeholder="Escribe tu pregunta">
    <input type="submit" value="Preguntar">
</form>

{% if pregunta %}
<hr>
<b>Pregunta:</b> {{ pregunta }}
<br><br>
<b>Respuesta:</b> {{ respuesta }}
{% endif %}

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
