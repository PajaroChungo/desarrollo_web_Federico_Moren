from sqlalchemy import create_engine, Integer, String, Column, ForeignKey, Enum, Text, DateTime, func
from sqlalchemy.orm import joinedload, sessionmaker, declarative_base, relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME= "tarea2"
DB_USERNAME= "cc5002"
DB_PASSWORD= "programacionweb"
DB_HOST= "localhost"
DB_PORT= 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo= False, future=True)
SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

#----MODELS----

class Region(Base):
    __tablename__ = 'region'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    
    # Relación con comuna
    comunas = relationship('Comuna', backref='region', lazy=True)

class Comuna(Base):
    __tablename__ = 'comuna'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    
    # Relación con miembro
    miembros = relationship('Miembro', backref='comuna', lazy=True)

class Miembro(Base):
    __tablename__ = 'miembro'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(80), nullable=False)
    telefono = Column(String(15), nullable=False)
    contraseña_hash = Column(String(255), nullable= False)
    fecha_registro = Column(DateTime, nullable=False, default=datetime.now)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    tipo_miembro = Column(Enum('estudiante_pre', 'estudiante_post', 'funcionario', 'academico'), nullable=False)
    cargo = Column(Enum('administrativo', 'profesional', 'coordinador', 'jefatura', 'auxiliar'), nullable=True)
    
    # Relación con actividad
    actividades = relationship('Actividad', backref='miembro', lazy=True)

class Actividad(Base):
    __tablename__ = 'actividad'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    miembro_id = Column(Integer, ForeignKey('miembro.id'), nullable=False)
    dia = Column(Enum('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'), nullable=False)
    hora_inicio = Column(String(5), nullable=False)
    duracion = Column(String(5), nullable=False)
    tipo = Column(Enum('arte', 'deporte', 'tecnología', 'social', 'recreación', 'otra'), nullable=False)
    nombre = Column(String(45), nullable=False)
    descripcion = Column(Text, nullable=True)
    url = Column(Text, nullable = True)
    
    # Relación con foto
    fotos = relationship('Foto', backref='actividad', lazy=True)

    # Relación con comentario
    comentarios = relationship('Comentario', backref= 'actividad', lazy = True)

class Foto(Base):
    __tablename__ = 'foto'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class Comentario(Base):
    __tablename__ = 'comentario'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

#----Database functions----

def get_regiones():
    session = SessionLocal()
    regiones = session.query(Region).order_by(Region.nombre)
    session.close()
    return regiones

#Se buscan las comunas de una región en específico
def get_comunas(region_id):
    session= SessionLocal()
    comunas = session.query(Comuna).filter(Comuna.region_id == region_id).order_by(Comuna.nombre).all()
    session.close()
    return comunas

#Se busca una comuna por Id
def get_comuna_byId(comuna_id):
    session= SessionLocal()
    comuna = session.query(Comuna).filter(Comuna.id == int(comuna_id)).first
    session.close()
    return comuna

def get_user_byEmail(email):
    session = SessionLocal()
    user = session.query(Miembro).filter_by(email=email).first()
    session.close()
    return user

def get_activity_byId(activity_id):
    session = SessionLocal()
    actividad = session.query((Actividad))\
        .options(
            joinedload(Actividad.miembro),
            joinedload(Actividad.fotos),
            joinedload(Actividad.comentarios)
        )\
        .filter(Actividad.id == activity_id).first()
    session.close()
    return actividad
    
def get_user_byId(user_id):
    session = SessionLocal()
    user = session.query(Miembro).filter_by(id=user_id).first()
    session.close()
    return user

def create_user(nombre, apellido, correo, telefono, contraseña, comuna, tipo, cargo):
    session = SessionLocal()
    nombre = f"{nombre} {apellido}"
    fecha_registro = datetime.now()
    contraseña_hash = generate_password_hash(contraseña)
    if not cargo:
        cargo = None
    new_user= Miembro(nombre = nombre, email = correo, telefono = telefono, contraseña_hash = contraseña_hash, fecha_registro = fecha_registro, comuna_id= int(comuna), tipo_miembro= tipo, cargo = cargo)
    session.add(new_user)
    session.commit()
    session.close()

def register_user(nombre, apellido, correo, telefono, contraseña, comuna, tipo, cargo):
    if get_user_byEmail(correo) is not None:
        return False, "El correo ya esta en uso."
    create_user(nombre, apellido, correo, telefono, contraseña, comuna, tipo, cargo)
    return True, None 

def login_user(correo, contraseña):
    user= get_user_byEmail(correo)
    if user is None:
        return False, "Usuario o contraseña incorrectos"
    contraseña_hash = user.contraseña_hash
    if not check_password_hash(contraseña_hash, contraseña):
        return False, "Usuario o contraseña incorrectos"
    return True, None

def get_activities():
    session = SessionLocal()
    try:
        actividades = session.query(Actividad)\
            .options(
                joinedload(Actividad.miembro),
                joinedload(Actividad.fotos)
            ).order_by(Actividad.id.desc()).all()
        return actividades
    finally:
        session.close()

def create_activity(miembro_id, nombre_actividad, dia, hora_inicio, duracion, tipo, descripcion, url):
    session = SessionLocal()
    nueva_actividad= Actividad(
        miembro_id= miembro_id,
        nombre = nombre_actividad,
        dia = dia,
        hora_inicio = hora_inicio,
        duracion = duracion,
        tipo= tipo,
        descripcion = descripcion,
        url = url)
    session.add(nueva_actividad)
    session.commit()
    session.refresh(nueva_actividad)
    id_actividad = nueva_actividad.id
    session.close()
    return id_actividad

def create_image(ruta_archivo, nombre_archivo, actividad_id):
    session= SessionLocal()
    nueva_foto = Foto(
        ruta_archivo = ruta_archivo,
        nombre_archivo = nombre_archivo,
        actividad_id = actividad_id
    )
    session.add(nueva_foto)
    session.commit()
    session.close()

def create_comentario(actividad_id, nombre, texto):
    session = SessionLocal()
    nuevo_comentario = Comentario(
        actividad_id=actividad_id,
        nombre=nombre,
        texto=texto,
        fecha=datetime.now()
    )
    session.add(nuevo_comentario)
    session.commit()
    session.close()

def get_usuarios(busqueda='', filtro_tipo='', filtro_cargo='', ordenar_por='nombre'):
    session = SessionLocal()
    query = session.query(Miembro)
    if busqueda:
        query = query.filter(Miembro.nombre.ilike(f'%{busqueda}%'))
    if filtro_tipo:
        query = query.filter(Miembro.tipo_miembro == filtro_tipo)
    if filtro_cargo:
        query = query.filter(Miembro.cargo == filtro_cargo)
    columna = getattr(Miembro, ordenar_por, Miembro.nombre)
    query = query.order_by(columna)
    usuarios = query.all()
    session.close()
    return usuarios

def get_usuarios_recientes():
    session = SessionLocal()
    usuarios = session.query(Miembro).order_by(Miembro.fecha_registro.desc()).limit(5).all()
    session.close()
    return usuarios

def get_activities_and_user(user_id):
    session = SessionLocal()
    miembro_y_Actividades = session.query(Miembro).options(joinedload(Miembro.actividades).joinedload(Actividad.fotos))\
    .filter(Miembro.id == user_id).first()
    session.close()
    return miembro_y_Actividades

def get_comentarios_byActividad(actividad_id):
    session = SessionLocal()
    comentarios = session.query(Comentario)\
                         .filter(Comentario.actividad_id == actividad_id)\
                         .order_by(Comentario.fecha.desc()).all()
    session.close()
    return comentarios

#--Funciones de Stats--
#Gráfico 1
def get_users_register_per_date():
    session = SessionLocal()
    users = session.query(func.date(Miembro.fecha_registro).label('dia')
                          ,func.count(Miembro.id).label('cantidad'))\
                            .group_by(func.date(Miembro.fecha_registro)).order_by(func.date(Miembro.fecha_registro))\
                            .all()
    session.close()
    return users

#Gráfico 2
def get_activities_per_type():
    session = SessionLocal()
    activities = session.query(Actividad.tipo.label("tipo")
                               ,func.count(Actividad.id).label("cantidad"))\
                               .group_by(Actividad.tipo).order_by(Actividad.tipo)\
                               .all()

    session.close()
    return activities

#Gráfico 3
def get_activities_per_district():
    session = SessionLocal()
    activities = session.query(Comuna.nombre.label("comuna")
                               ,func.count(Actividad.id).label("cantidad"))\
                               .join(Miembro, Miembro.comuna_id == Comuna.id).join(Actividad, Actividad.miembro_id == Miembro.id)\
                                .group_by(Comuna.id, Comuna.nombre).order_by(Comuna.nombre)\
                                    .all()
    session.close()
    return activities
