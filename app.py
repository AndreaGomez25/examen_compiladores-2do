from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def validar_curp():
    mensaje_sintactico = ""
    tabla_lexico = []
    tabla_sintactico = []
    token_count = {"Letras": 0, "Números": 0, "Otros": 0}
    curp = ""  # Inicializa la variable curp

    if request.method == "POST":
        curp = request.form["curp"].strip().upper()

        # Validación básica de longitud y estructura de CURP
        if len(curp) == 18:
            # Análisis Sintáctico: Todos los tokens son correctos si la longitud es 18
            tabla_sintactico.append(("CURP Completa", "Correcto"))

            # Desglose de la CURP en campos específicos para el análisis léxico
            tabla_lexico = [
                ("Apellido Paterno", curp[0:2]),
                ("Apellido Materno", curp[2]),
                ("Inicial del Nombre", curp[3]),
                ("Año de Nacimiento", curp[4:6]),
                ("Mes de Nacimiento", curp[6:8]),
                ("Día de Nacimiento", curp[8:10]),
                ("Género", curp[10]),  # Solo H o M
                ("Entidad de Nacimiento", curp[11:13]),
                ("Consonante Primer Apellido", curp[13]),
                ("Consonante Segundo Apellido", curp[14]),
                ("Consonante Primer Nombre", curp[15]),
                ("Renapo", curp[16:18])
            ]
            mensaje_sintactico = "CURP válida y desglosada con éxito."
        else:
            mensaje_sintactico = "CURP inválida. Debe contener exactamente 18 caracteres."
            # Análisis Sintáctico: Error en la longitud de la CURP
            tabla_sintactico.append(("Error de longitud", f"Error en la CURP: longitud incorrecta ({len(curp)} caracteres)"))

        # Contar tipos de tokens
        token_count["Letras"] = len(re.findall(r"[A-Z]", curp))
        token_count["Números"] = len(re.findall(r"[0-9]", curp))
        token_count["Otros"] = len(re.findall(r"[^A-Z0-9]", curp))

    return render_template("index.html", mensaje_sintactico=mensaje_sintactico, tabla_lexico=tabla_lexico, tabla_sintactico=tabla_sintactico, token_count=token_count, curp=curp)

if __name__ == "__main__":
    app.run(debug=True)