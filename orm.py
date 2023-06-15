from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

#https://docs.sqlalchemy.org/en/20/orm/quickstart.html
#Esta clase se define si o sí según la documentación de SQL alchemy
class Base(DeclarativeBase):
     pass

class BaseCRUD:
    def create(self, data):
        raise NotImplementedError

    def read(self, id):
        raise NotImplementedError

    def update(self, id, data):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

class UserDomain:
    def __init__(self, name, age, id = 0):
        self.id = id
        self.name = name
        self.age = age

    #Si bien no definimos atributos de instancia en User
    #La sintaxis utilizada CREA los atributos de instancia para el objeto de esa clase
    def to_user(self):
        return User(name=self.name, age=self.age)

    def __str__(self):
        return f"{self.name} {self.age}"

#Heredamos de la clase base de SqlAlchemy
#Configuramos la clase para que luego los objetos se persistan
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def to_user_domain(self):
        return UserDomain(id=self.id, name=self.name, age=self.age)

class UserCRUD(BaseCRUD):
    def __init__(self):
        """
        Crea un objeto de tipo Engine que representa una conexión con la base de datos SQLite que está definida en el
        archivo "example.db". Si no existe, crea la DB.
        La función create_engine se utiliza para crear objetos Engine que proporcionan
        una interfaz para conectarse a una base de datos.
        El argumento que se le pasa a create_engine es una cadena de conexión que especifica la ubicación y
        el tipo de base de datos que se desea utilizar.
        En este caso, la cadena de conexión especifica que se va a usar una base de datos SQLite
        y que se encuentra en el archivo "example.db".
        """
        engine = create_engine('sqlite:///example.db')

        """
         Se encarga de crear todas las tablas correspondientes a las clases definidas en el modelo de SQLAlchemy.
         Este método recorre todas las clases definidas en el modelo y crea las tablas correspondientes en la base de 
         datos según los atributos y configuraciones definidos en cada una de ellas.
        """
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def create(self, user):
        session = self.Session()
        session.add(user)
        session.commit()
        return user.id

    def read(self, id):
        session = self.Session()
        user = session.query(User).filter_by(id=id).first()
        return user.to_user_domain() if user else None

    def read_all(self):
        session = self.Session()
        return session.query(User).all()

    def update(self, id, userDomain):
        session = self.Session()
        user = session.query(User).filter_by(id=id).first()
        if user:
            user.name = userDomain.name
            user.age = userDomain.age
            session.commit()

    def delete(self, id):
        session = self.Session()
        user = session.query(User).filter_by(id=id).first()
        if user:
            session.delete(user)
            session.commit()


if __name__ == '__main__':
    userCRUD = UserCRUD()
    user = UserDomain(name="Lucas", age=20).to_user()
    id_created_user = userCRUD.create(user)

    userByIdDomain = userCRUD.read(id_created_user)
    print(userByIdDomain)

    userByIdDomain.name = "ACTUALIZADO"
    userCRUD.update(id_created_user, userByIdDomain)

    userByIdDomain = userCRUD.read(id_created_user)
    print(userByIdDomain)