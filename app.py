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
    margin-top:30px;
    background:#ffffff;
    padding:24px;
    border-radius:12px;
    width:70%;
    margin-left:auto;
    margin-right:auto;
    box-shadow:0px 4px 12px rgba(0,0,0,0.12);
    text-align:left;
}

.pregunta{
    color:#7B1E3A;
    font-weight:bold;
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

        <form method="POST" class="formulario">

            <input type="text" name="pregunta" placeholder="Escribe o pega tu imagen aquí...">

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







<div class="buho-container">

    <div class="globo-bienvenida">
        <b>Hola, soy BernaBOT.</b><br>
        Puedo ayudarte con Ley de Ohm, Kirchhoff, resistencias, diodos, transistores y circuitos eléctricos.
    </div>

    <img src="/static/uag.png" class="buho" alt="BernaBOT">

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
