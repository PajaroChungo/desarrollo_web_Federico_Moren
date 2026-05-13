from werkzeug.security import generate_password_hash
from datetime import datetime
from db import SessionLocal, Miembro, Actividad

#Ejecute python database/init_db.py y luego el archivo de region-comunas.sql
#Luego, en la terminal: "python database/crear_db_juguete.py"
#Hay que hacerlo con la ruta "...\flask_app"

#Para correr el archivo region-comuna.sql, una forma de hacerlo es con crtl + a
#luego corriendo con la expansión de mySql
#Pd. disculpe el inconveniente, no encontré como automatizar este proceso, si quiere probar toda
#la página por su cuenta puede cerrar sesión para crear más de un usuario
#Pd.2. Notesé que las actividades creadas acá no poseen imagenes, esto es debido al proceso de hashlib por el que
#pasan antes de ser guardados en la carpeta uploads

usuarios = [
    ('Juan', 'Pérez', 'juan.perez@example.com', '912345678', 'estudiante_pre', None),
    ('María', 'González', 'maria.gonzalez@example.com', '923456789', 'estudiante_post', None),
    ('Carlos', 'Rodríguez', 'carlos.rodriguez@example.com', '934567890', 'funcionario', 'administrativo'),
    ('Ana', 'Martínez', 'ana.martinez@example.com', '945678901', 'academico', None),
    ('Luis', 'López', 'luis.lopez@example.com', '956789012', 'funcionario', 'jefatura'),
    ('Sofía', 'Sánchez', 'sofia.sanchez@example.com', '967890123', 'estudiante_pre', None),
    ('Diego', 'Ramírez', 'diego.ramirez@example.com', '978901234', 'academico', None),
]

session = SessionLocal()
for nombre, apellido, email, telefono, tipo, cargo in usuarios:
    user = Miembro(
        nombre=f"{nombre} {apellido}",
        email=email,
        telefono=telefono,
        contraseña_hash=generate_password_hash('Password1'),
        fecha_registro=datetime.now(),
        comuna_id=10101,
        tipo_miembro=tipo,
        cargo=cargo
    )
    session.add(user)
session.commit()
session.close()
print('Usuarios creados exitosamente')

session = SessionLocal()
usuarios = session.query(Miembro).all()

actividades = [
    Actividad(miembro_id=usuarios[0].id, nombre='Torneo de Ajedrez', dia='lunes', 
              hora_inicio='15:00', duracion='120', tipo='recreación',
              descripcion='Torneo abierto para todos los niveles.', url=None),
    Actividad(miembro_id=usuarios[0].id, nombre='Club de Lectura', dia='jueves', 
              hora_inicio='17:00', duracion='60', tipo='social',
              descripcion='Discusión del libro del mes.', url=None),
    Actividad(miembro_id=usuarios[1].id, nombre='Taller de Pintura', dia='miércoles',
              hora_inicio='14:00', duracion='90', tipo='arte',
              descripcion='Taller para principiantes con materiales incluidos.', url=None),
    Actividad(miembro_id=usuarios[1].id, nombre='Exposición de Arte', dia='sábado', 
              hora_inicio='11:00', duracion='180', tipo='arte',
              descripcion='Exposición de trabajos realizados en el taller.', url='https://www.google.com'),
    Actividad(miembro_id=usuarios[2].id, nombre='Partido de Fútbol', dia='sábado',
              hora_inicio='10:00', duracion='90', tipo='deporte',
              descripcion='Partido amistoso en la cancha principal.', url=None),
    Actividad(miembro_id=usuarios[3].id, nombre='Charla de IA', dia='jueves',
              hora_inicio='16:00', duracion='60', tipo='tecnología',
              descripcion='Introducción a inteligencia artificial.', url='https://www.google.com'),
    Actividad(miembro_id=usuarios[4].id, nombre='Reunión Social', dia='viernes',
              hora_inicio='18:00', duracion='120', tipo='social',
              descripcion='Encuentro informal para conocerse.', url=None),
]

for actividad in actividades:
    session.add(actividad)
session.commit()
session.close()
print('Actividades creadas exitosamente')