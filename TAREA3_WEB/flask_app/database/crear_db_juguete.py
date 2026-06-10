from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from db import Comentario, SessionLocal, Miembro, Actividad

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

fechas_registro = [
    datetime.now() - timedelta(days=60),
    datetime.now() - timedelta(days=60),
    datetime.now() - timedelta(days=30),
    datetime.now() - timedelta(days=30),
    datetime.now() - timedelta(days=15),
    datetime.now() - timedelta(days=7),
    datetime.now() - timedelta(days=2),
]

comunas = [10304, 20303, 30202, 40102, 50506, 60105, 20202]

session = SessionLocal()
for i, (nombre, apellido, email, telefono, tipo, cargo) in enumerate(usuarios):
    user = Miembro(
        nombre=f"{nombre} {apellido}",
        email=email,
        telefono=telefono,
        contraseña_hash=generate_password_hash('Password1'),
        fecha_registro=fechas_registro[i],
        comuna_id=comunas[i],
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
print('Actividades creadas exitosamente')

actividades = session.query(Actividad).all()

comentarios = [
    Comentario(actividad_id=actividades[0].id, nombre='Pedro Álvarez',
               texto='Excelente torneo, muy bien organizado.',
               fecha=datetime.now() - timedelta(days=5)),
    Comentario(actividad_id=actividades[0].id, nombre='Camila Torres',
               texto='Me encantó participar, volveré el próximo mes.',
               fecha=datetime.now() - timedelta(days=3)),
    Comentario(actividad_id=actividades[2].id, nombre='Roberto Fuentes',
               texto='El taller estuvo muy entretenido, aprendí bastante.',
               fecha=datetime.now() - timedelta(days=10)),
    Comentario(actividad_id=actividades[4].id, nombre='Valentina Cruz',
               texto='Gran partido, ojalá se repita pronto.',
               fecha=datetime.now() - timedelta(days=1)),
    Comentario(actividad_id=actividades[5].id, nombre='Andrés Morales',
               texto='Muy buena charla, quedé con ganas de aprender más de IA.',
               fecha=datetime.now() - timedelta(hours=5)),
]

for comentario in comentarios:
    session.add(comentario)
session.commit()
session.close()
print('Comentarios creados exitosamente')