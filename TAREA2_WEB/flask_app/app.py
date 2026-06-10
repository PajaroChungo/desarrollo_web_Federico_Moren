from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_cors import cross_origin
from utils.validations import validate_activity, validate_comment, validate_login_user, validate_register_user, validateCommentName, validateCommentText
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os

from database.db import create_activity, create_comentario, create_image, get_activities, get_activities_and_user, get_activities_per_district, get_activities_per_type, get_activity_byId, get_comentarios_byActividad, get_comunas, get_regiones, get_user_byEmail, get_user_byId, get_users_register_per_date, get_usuarios, get_usuarios_recientes, login_user, register_user

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#-----Auth Routes------
@app.route("/login", methods= ["GET", "POST"])
def login():
    user = session.get("user", None)
    if request.method == "POST":
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")
        error = ""
        if validate_login_user(correo, contraseña):
            status, msg = login_user(correo, contraseña)
            if status:
                userId= get_user_byEmail(correo).id
                session["user"] = userId
                return redirect(url_for('index'))
            error += msg
        else:
            error += "Uno de los campos no es válido."
        return render_template("auth/login.html", error = error)
    elif request.method == "GET":
        if user:
            return redirect(url_for('index'))
        else:
            return render_template("auth/login.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    user = session.get("user", None)
    if request.method == "POST":
        nombre = request.form.get("Nombre-Usuario")
        apellido = request.form.get("Apellido-Usuario")
        correo = request.form.get("Correo-Usuario")
        telefono = request.form.get("Telefono-Usuario")
        contraseña = request.form.get("Contraseña-Usuario")
        repetir_contraseña = request.form.get("Confirmar-Contraseña-Usuario")
        comuna = request.form.get("Comuna-Usuario")
        tipo = request.form.get("Tipo-Usuario")
        cargo = request.form.get("Cargo-Usuario")
        error = ""
        if validate_register_user(nombre, apellido, contraseña, repetir_contraseña, correo, telefono, comuna, tipo, cargo):
            status, msg = register_user(nombre, apellido, correo, telefono, contraseña, comuna, tipo, cargo)
            if status:
                userId= get_user_byEmail(correo).id
                session["user"] = userId
                return redirect(url_for("index"))
            error += msg
        else:
            error += "Uno de los campos no es válido."
        regiones = get_regiones()
        return render_template("auth/registro.html", error = error, regiones= regiones)
    elif request.method == "GET":
        if user:
            return redirect(url_for('index'))
        else:
            regiones = get_regiones()
            return render_template('auth/registro.html', regiones = regiones)
        
@app.route('/comunas/<int:region_id>')
def comunas (region_id):
    comunas = get_comunas(region_id)
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])

#---- Routes ----
@app.route("/", methods=["GET"])
def index():
    user = session.get("user", None)
    nombre = None
    if user:
        miembro = get_user_byId(user)
        nombre = miembro.nombre if miembro else None
    miembros_recientes = get_usuarios_recientes()
    return render_template('activities/index.html', user=user, nombre=nombre, miembros_recientes= miembros_recientes)

@app.route("/actividades", methods=["GET", "POST"])
def actividades():
    user = session.get("user", None)
    if request.method == "GET":
        todas_actividades = get_activities()
        return render_template('activities/actividades.html', actividades=todas_actividades, user=user)
    elif request.method == "POST":
        dia = request.form.get("Dia-Actividad")
        hora_inicio = request.form.get("Hora-Actividad")
        duracion = request.form.get("Duracion-Actividad")
        tipo = request.form.get("Categoria-Actividad")
        nombre = request.form.get("Nombre-Actividad")
        descripcion = request.form.get("Descripcion-Actividad")
        url = request.form.get("Url")

        activity_images = request.files.getlist("files")
        if validate_activity(user, nombre, dia, hora_inicio, duracion, tipo, descripcion, url, activity_images):
            activity_id = create_activity(user, nombre, dia, hora_inicio, duracion, tipo, descripcion, url)
            for image in activity_images:
                imagen_bytes = image.read()
                nombre_imagen = hashlib.sha256(
                    secure_filename(image.filename)
                    .encode("utf-8")
                    ).hexdigest()
                _tipo = filetype.guess(imagen_bytes)
                _extension = _tipo.extension if _tipo else image.filename.rsplit('.', 1)[-1]
                nombre_ruta = f"{nombre_imagen}.{_extension}"
                image.seek(0)
                image.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_ruta))
                create_image(f"uploads/{nombre_ruta}", image.filename, activity_id)
            return redirect(url_for('actividades'))
        todas_actividades = get_activities()
        return render_template('activities/actividades.html', actividades=todas_actividades, user=user, error = "Uno de los campos no es válido.")

@app.route("/usuarios")
def usuarios():
    busqueda = request.args.get('busqueda', '')
    filtro_tipo = request.args.get('filtro_tipo', '')
    filtro_cargo = request.args.get('filtro_cargo', '')
    ordenar_por = request.args.get('ordenar_por', 'nombre')
    pagina = int(request.args.get('pagina', 1))
    por_pagina = 5

    todos_usuarios = get_usuarios(busqueda, filtro_tipo, filtro_cargo, ordenar_por)
    total_paginas = max(1, -(-len(todos_usuarios) // por_pagina))  # redondeo hacia arriba
    
    inicio = (pagina - 1) * por_pagina
    usuarios = todos_usuarios[inicio:inicio + por_pagina]

    return render_template('activities/usuarios.html', 
                         usuarios=usuarios,
                         pagina=pagina,
                         total_paginas=total_paginas,
                         user=session.get("user", None))

@app.route("/miembro/<int:miembro_id>")
def perfil_miembro(miembro_id):
    miembro = get_activities_and_user(miembro_id)
    if not miembro:
        return redirect(url_for('usuarios'))
    return render_template('activities/perfil_miembro.html', miembro=miembro, user= session.get("user", None))

@app.route("/actividad/<int:actividad_id>", methods=["GET"])
def perfil_actividad(actividad_id):
    actividad = get_activity_byId(actividad_id)
    if not actividad:
        return redirect(url_for('actividades'))
    return render_template('activities/perfil_actividad.html',actividad=actividad, user=session.get("user", None))

@app.route("/actividad/<int:actividad_id>/comentario", methods = ["POST"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def agregar_comentario(actividad_id):
    actividad = get_activity_byId(actividad_id)
    if not actividad:
        return jsonify({"status": "error", "data": "No hay actividad."}), 400
    data = request.get_json()
    nombre = (data.get("nombre") or "").strip()
    texto = (data.get("texto") or "").strip()
    errores = {}
    if not validateCommentName(nombre):
        errores["nombre"] = "El nombre debe tener entre 3 y 80 caracteres."
    if not validateCommentText(texto):
        errores["texto"] = "El comentario debe tener al menos 5 caracteres."
    if errores:
        return jsonify({"status": "error", "data": errores}), 400
    create_comentario(actividad_id, nombre, texto)
    return jsonify({"status" : "ok"})
    
@app.route("/actividad/<int:actividad_id>/comentarios", methods = ["GET"])
def lista_comentarios(actividad_id):
    comentarios = get_comentarios_byActividad(actividad_id)
    return jsonify([{
        "nombre": comentario.nombre,
        "texto" : comentario.texto,
        "fecha" : comentario.fecha.strftime("%d/%m/%Y | %H:%M")
    } for comentario in comentarios
    ])

@app.route("/metricas")
def metricas():
    return render_template("activities/metricas.html")

@app.route("/get-stats-registersPerDay", methods=["GET"])
@cross_origin(origin="http://127.0.0.1", supports_credentials = True)
def get_stats_registersPerDay():
    data = get_users_register_per_date()
    return jsonify({
        'dias': [str(dato.dia) for dato in data],
        'cantidad': [dato.cantidad for dato in data]
    })

@app.route("/get-stats-activitiesPerType", methods=["GET"])
@cross_origin(origin="http://127.0.0.1", supports_credentials = True)
def get_stats_activitiesPerType():
    data= get_activities_per_type()
    return jsonify({
        'tipos': [dato.tipo for dato in data],
        'cantidad': [dato.cantidad for dato in data]
    })

@app.route("/get-stats-activitiesPerDistrict", methods=["GET"])
@cross_origin(origin="http://127.0.0.1", supports_credentials = True)
def get_stats_activitiesPerDistrict():
    data = get_activities_per_district()
    return jsonify({
        "comunas": [dato.comuna for dato in data],
        "cantidad": [dato.cantidad for dato in data]
    })

if __name__ == '__main__':
    app.run(debug=True)