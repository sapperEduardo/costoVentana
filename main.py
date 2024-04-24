from app import Inicio, Calcular_precio, Confguraciones


 
class App:

    def __init__(self):
        self.ventana = 0 


    def mostrar_inicio(self):
        self.ventana = Inicio(self)

    def mostrar_calcular(self):
        self.ventana = Calcular_precio(self)

    def mostrar_configuraciones(self):
        self.ventana = Confguraciones(self)
        

Programa = App()

Programa.mostrar_inicio()




