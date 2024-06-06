
class Usuario:
    
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password
        
    def autenticar(self, password_ingresada):
        return self.__password == password_ingresada

    def obtener_email(self):
        return self.__email

    def cambiar_password(self, nueva_password):
        self.__password = nueva_password
        
        

    
class Bibliotecario(Usuario):
    def __init__(self, username, email, password, nivel_acceso):
        super().__init__(username, email, password)
        self.__nivel_acceso = nivel_acceso

    def agregar_libro(self, titulo, autor, isbn):
        nuevo_libro = Libro(titulo, autor, isbn)
        # Aquí podrías agregar el libro a una base de datos o una lista
        return nuevo_libro

    def eliminar_libro(self, libro):
        # Aquí podrías eliminar el libro de una base de datos o una lista
        pass

class Libro:
    def __init__(self, titulo, autor, isbn):
        self.__titulo = titulo
        self.__autor = autor
        self.__isbn = isbn
        self.__prestado = False

    def prestar(self):
        if not self.__prestado:
            self.__prestado = True
            return True
        return False

    def devolver(self):
        if self.__prestado:
            self.__prestado = False
            return True
        return False

    def esta_prestado(self):
        return self.__prestado