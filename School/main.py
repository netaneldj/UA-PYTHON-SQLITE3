from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy import Table, Text

#Database engine
engine = create_engine('sqlite:///:memory:')

#Clase
db = declarative_base()

#Relación de muchos a muchos entre Curso y Profesor
prof_cursos = Table('prof_cursos', db.metadata,
    Column('curso_id', ForeignKey('curso.id'), primary_key=True),
    Column('profesor_id', ForeignKey('profesor.id'), primary_key=True),
)

#Clase Alumno
class Alumno(db):
    __tablename__ = 'alumno'

    id = Column(Integer, Sequence('id'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    curso_id = Column(Integer, ForeignKey('curso.id'))
    curso = relationship("Curso", back_populates="alumnos")

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


#Clase Profesor
class Profesor(db):
    __tablename__ = 'profesor'

    id = Column(Integer, Sequence('id'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    cursos = relationship('Curso', secondary=prof_cursos, back_populates='profesores')

    horario_prof = relationship("Horario", uselist=False, back_populates="profesor")

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


#Clase Curso
class Curso(db):
    __tablename__ = 'curso'

    id = Column(Integer, Sequence('id'), primary_key=True)
    name = Column(String)

    alumnos = relationship("Alumno", order_by="Alumno.id", back_populates="curso",
                    cascade="all, delete, delete-orphan")

    profesores = relationship('Profesor', secondary=prof_cursos, back_populates='cursos')

    horario_curso = relationship("Horario", uselist=False, back_populates="curso")

    def __repr__(self):
        return "{}".format(self.name)


#Clase Horario
class Horario(db):
    __tablename__ = 'horario'

    id = Column(Integer, Sequence('id'), primary_key=True)
    dia = Column(String)
    hora_inicio = Column(Integer)
    hora_final = Column(Integer)

    profesor_id = Column(Integer, ForeignKey('profesor.id'))
    profesor = relationship("Profesor", uselist=False, back_populates="horario_prof")

    curso_id = Column(Integer, ForeignKey('curso.id'))
    curso = relationship("Curso", uselist=False, back_populates="horario_curso")

    def __repr__(self):
        return "{} at {}-{}: {} - {}".format(self.dia, self.hora_inicio, self.hora_final, self.profesor, self.curso)


#Crea las tablas según las clases definidas
db.metadata.create_all(engine)

#Creación de la sesión
Session = sessionmaker(bind=engine)
session = Session()

#Crear cursos
mate = Curso(name='Matemáticas')
geo = Curso(name='Geometría')

#Crear alumnos
mate.alumnos = [Alumno(firstname='Laura', lastname='Patiña'),
                Alumno(firstname='Lauro', lastname='Patiño')]

geo.alumnos = [Alumno(firstname='Laure', lastname='Patiñe'),
                Alumno(firstname='Lauri', lastname='Patiñi')]

#Crear profesores
profesor1 = Profesor(firstname='Hernán', lastname='Hernández')
profesor2 = Profesor(firstname='Hernana', lastname='Hernandeza')
profesor3 = Profesor(firstname='Hernane', lastname='Hernandeze')

#Asignar dos profesores a un curso
mate.profesores = [profesor1, profesor2]
geo.profesores = [profesor3]

#Crear horarios y asignar a curso y profesor
horario1 = Horario(dia='Lunes', hora_inicio=8, hora_final=10, profesor=mate.profesores[0], curso=mate)
horario2 = Horario(dia='Martes', hora_inicio=2, hora_final=4, profesor=mate.profesores[1], curso=mate)
horario3 = Horario(dia='Viernes', hora_inicio=8, hora_final=10, profesor=geo.profesores[0], curso=geo)

#Guardar
session.add(mate)
session.add(geo)
session.commit()

#Pruebas
print("Alumno simple")
print(session.query(Alumno).filter_by(firstname='Laura').one())

print("Alumnos en curso Geometría")
print(session.query(Curso).filter_by(name="Geometría").one().alumnos)

print("Profesores en curso Matemáticas")
print(session.query(Curso).filter_by(name="Matemáticas").one().profesores)

print("Horario del lunes")
print(session.query(Horario).filter_by(dia='Lunes').one())

print("Horario de Hernane")
print(session.query(Horario).filter(Horario.profesor.has(Profesor.firstname=='Hernane')).one())