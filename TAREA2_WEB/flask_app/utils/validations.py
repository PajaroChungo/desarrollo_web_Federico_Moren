import re
import filetype

from database import db

def validateName(name):
    return (
        bool(name)
        and len(name.strip()) >= 3
        and bool(re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s]+$', name))
    )

def validate_gmail(email):
    gmail_format = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.fullmatch(gmail_format, email))

def validate_telephone(telephone):
    telephone_format_cl = r'^9\d{8}$'
    return bool(re.fullmatch(telephone_format_cl, telephone))


def validate_password(password):
    password_format = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
    return bool(re.fullmatch(password_format, password))

def validate_confirm_password(password, confirm_password):
     return password == confirm_password

def validate_comuna(comuna):
    if not comuna:
        return False
    comuna_id = int(comuna)
    return db.get_comuna_byId(comuna_id) is not None

def validate_tipo(tipo):
    TIPOS_VALIDOS = ['estudiante_pre', 'estudiante_post', 'funcionario', 'academico']
    return tipo in TIPOS_VALIDOS

def validate_cargo(tipo, cargo):
    CARGOS_VALIDOS = ['administrativo', 'profesional', 'coordinador', 'jefatura', 'auxiliar']
    if tipo == 'funcionario':
        return cargo in CARGOS_VALIDOS
    return True

def validate_register_user(nombre, apellido, contraseña, repetir_contraseña, correo, telefono, comuna, tipo, cargo):
        return (validateName(nombre) and
        validateName(apellido) and
        validate_gmail(correo) and
        validate_telephone(telefono) and
        validate_password(contraseña) and
        validate_confirm_password(contraseña, repetir_contraseña) and
        validate_comuna(comuna) and
        validate_tipo(tipo) and
        validate_cargo(tipo, cargo))

def validate_login_user(correo, contraseña):
     return (validate_gmail(correo) and validate_password(contraseña))

def validate_activityName(nombre_actividad):
     return (nombre_actividad and len(nombre_actividad.strip()) >= 5)

def validate_duracion(duracion):
     return (duracion and int(duracion) > 0)

def validate_descripcion(descripcion):
     return (not(descripcion) or len(descripcion.strip()) >= 10)

def validate_url(url):
     formato_url = r'^(https?:\/\/)?([\w.-]+)\.([a-z]{2,})(\/\S*)?$'
     return (not(url) or bool(re.fullmatch(formato_url, url)))

def validate_imagenes(imagenes):
     return (imagenes and (len(imagenes) > 0))

def validate_activity(user, nombre, dia, hora_inicio, duracion, tipo, descripcion, url, imagenes):
     return (user and 
     validate_activityName(nombre) and
     validate_duracion(duracion) and
     validate_descripcion(descripcion) and
     validate_url(url) and
     validate_imagenes(imagenes) and
     dia and hora_inicio and tipo
     )