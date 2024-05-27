import json

Datos = {}

def cargar_datos():
    global Datos
    with open('datos.json', 'r') as f:
        Datos = json.load(f)

def obtener_precio(codigo):
    global Datos
    for insumo in Datos["insumos"]:
        if codigo == insumo["codigo"]:
            return insumo["precio"]
         



## clases de insumos ##
class Insumo:
    def __init__(self):
        self.codigo = 0
        self.nombre = ''
        self.calidad = 1
    
    def actualizarPrecio(self):
        pass

class InsumoMts(Insumo):
    def __init__(self, metros):
        super().__init__()
        self.metros = metros

    def calcularPrecio(self):
        return obtener_precio(self.codigo)

class InsumoCntd(Insumo):
    def __init__(self, cantidad):
        super().__init__()
        self.cantidad = cantidad

    def calcularPrecio(self):
        return obtener_precio(self.codigo)
        

## clases de insumos dependientes de metros ##
class Perfil(InsumoMts):
    def __init__(self, calidad, metros, codigo, nombre):
        super().__init__(metros)
        self.calidad = calidad
        self.nombre = nombre
        self.codigo = codigo

    def calcularPrecio(self):
        global Datos
        for p in Datos["perfiles_aluminio"]:
            if self.codigo == p["codigo"] and self.calidad == p["calidad"]: 
                return p["kg/mts"]*self.metros*Datos["precio_kg_aluminio"]


class Felpa(InsumoMts):
    def __init__(self, metros):
        super().__init__(metros)
        self.codigo = 200
        self.nombre = 'felpa'

class Burlete(InsumoMts):
    def __init__(self, metros):
        super().__init__(metros)
        self.codigo = 201
        self.nombre = 'burlete'

class Vidrio(InsumoMts):
    def __init__(self, metros, calidad, codigo, nombre):
        super().__init__(metros)
        self.calidad = calidad
        self.codigo = codigo
        self.nombre = nombre

    def calcularPrecio(self):
        global Datos
        for insumo in Datos["insumos"]:
            if self.codigo == insumo["codigo"] and self.calidad == insumo["calidad"]: 
                return insumo["precio"]


## clases de insumos dependientes de una cantidad ##
class Cierre(InsumoCntd):
    def __init__(self, cantidad):
        super().__init__(cantidad)
        self.codigo = 203
        self.nombre = 'cierre central'

class Rueda(InsumoCntd):
    def __init__(self, cantidad):
        super().__init__(cantidad)
        self.codigo = 204
        self.nombre = 'rueda'

class Tirafondo(InsumoCntd):
    def __init__(self, cantidad):
        super().__init__(cantidad)
        self.codigo = 205
        self.nombre = 'tirafondo'

class Escuadra(InsumoCntd):
    def __init__(self, cantidad):
        super().__init__(cantidad)
        self.codigo = 206
        self.nombre = 'escuadra'

class Remache(InsumoCntd):
    def __init__(self, cantidad):
        super().__init__(cantidad)
        self.codigo = 207
        self.nombre = 'remache'


## clases del modelo de la ventana ##
class Hoja:
    def __init__(self, ancho, alto, calidad):
        self.ancho = ancho
        self.alto = alto
        self.calidad = calidad

        self.perfiles = Perfil(self.calidad, self.ancho*2, 1002, 'Dintel y Umbral' ), Perfil(self.calidad, self.alto, 1003, 'Parante Lateral' ), Perfil(self.calidad, self.alto, 1004, 'Parante Central' )
        self.tirafondo = Tirafondo(4)
        self.rueda = Rueda(2)
        self.vidrio = Vidrio((self.ancho - .16)*(self.alto - .16) , self.calidad, 202, 'vidrio')
        self.burlete = Burlete( self.ancho*2 + self.alto*2 )
        self.felpa = Felpa( self.alto*3 + self.ancho*2)

    def calcularPrecio(self):
        perfiles = sum( p.calcularPrecio() for p in self.perfiles)
        tirafondos = self.tirafondo.calcularPrecio()
        ruedas = self.rueda.calcularPrecio()
        vidrio = self.vidrio.calcularPrecio()
        burlete = self.burlete.calcularPrecio()
        felpa = self.felpa.calcularPrecio()
        return perfiles+tirafondos+ruedas+vidrio+burlete+felpa


class Marco:
    def __init__(self, ancho, alto, calidad):
        self.ancho = ancho
        self.alto = alto
        self.calidad = calidad

        self.perfil = Perfil(self.calidad, (self.ancho)*2 + (self.alto)*2, 1001, 'Marco Pesado')
        self.escuadra = Escuadra(4)
        self.remache = Remache(32)
        self.hojas = [ Hoja(self.ancho/2 -.094, self.alto - .06, self.calidad) for _ in range(2) ]
    
    def calcularPrecio(self):
        perfil = self.perfil.calcularPrecio()
        escuadra = self.escuadra.calcularPrecio()
        remache = self.remache.calcularPrecio()
        hojas = sum( [h.calcularPrecio() for h in self.hojas] )
        return perfil+escuadra+remache+hojas


class Ventana:    
    def __init__(self, ancho, alto, calidad):
        self.ancho = ancho
        self.alto = alto
        self.calidad = calidad

        self.cierre = Cierre(1)
        self.marco = Marco(self.ancho, self.alto, self.calidad)
    
    def calcularPrecio(self):
        cargar_datos()
        return self.marco.calcularPrecio() + self.cierre.calcularPrecio()




v = Ventana(1,1,1)

print(v.calcularPrecio())







    









