import json

class Coneccion:
    _instances = {}    
    Datos = {}

    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
            cls.cargar_datos(cls)
        return cls._instances[cls]
    
    ### metodos basicos de la coneccion ###
    def cargar_datos(cls):
        with open('datos.json', 'r') as f:
            cls.Datos = json.load(f)
    def guardar_datos(cls):
        with open('datos.json', 'w') as f:
            json.dump(cls.Datos, f, indent=1)

    ### metodos para obtener precios de los distintos insumos ###
    def obtenerPrecioAluminio(cls):
        return cls.Datos["precio_kg_aluminio"]


    def obtenerPrecio(cls, codigo):
        for insumo in cls.Datos["insumos"]:
            if codigo == insumo["codigo"]:
                return insumo["precio"]
            
    def obtenerPrecioPerfil(cls, codigo, calidad):
        for p in cls.Datos["perfiles_aluminio"]:
            if codigo == p["codigo"] and calidad == p["calidad"]: 
                return p["kg/mts"] * cls.Datos["precio_kg_aluminio"]

    def obtenerPrecioVidrio(cls, calidad):
        for insumo in cls.Datos["insumos"]:
            if 202 == insumo["codigo"] and calidad == insumo["calidad"]: 
                return insumo["precio"]
    def obtenerNombreVidrio(cls, calidad):
        for insumo in cls.Datos["insumos"]:
            if 202 == insumo["codigo"] and calidad == insumo["calidad"]: 
                return insumo["nombre"]
            
    ### metodos para actualizar precios de los insumos ###
    def actualizarPrecioAluminio(cls, nuevo_precio_kg_aluminio):
        cls.Datos['precio_kg_aluminio'] = nuevo_precio_kg_aluminio

    def actualizarPrecioInsumo(cls, codigo, nuevo_precio):
        for insumo in cls.Datos['insumos']:
            if insumo['codigo'] == codigo:
                insumo['precio'] = nuevo_precio
                break

    def actualizarPrecioVidrio(cls, codigo, calidad, nuevo_precio):
        for insumo in cls.Datos['insumos']:
            if insumo['codigo'] == codigo and insumo['calidad'] == calidad:
                insumo['precio'] = nuevo_precio
                break





def obtener_insumos():
    return [Aluminio(), Felpa(), Burlete(), Vidrio(1), Vidrio(2), Cierre(), Rueda(),
             Tirafondo(), Escuadra(), Remache(), AntiRuido(), ParTJ()]





## clases de insumos ##
class Insumo:
    def __init__(self):
        self.codigo = 0
        self.nombre = ''
        self.calidad = 1
        self.precio = 0
        

    def cargarPrecio(self):
        self.precio = Coneccion().obtenerPrecio(self.codigo)
    def getNombre(self):
        return self.nombre
    def getPrecio(self):
        return self.precio
    
    def actualizarPrecio(self, nuevo_precio):
        self.precio = nuevo_precio
        Coneccion().actualizarPrecioInsumo(self.codigo, self.precio)

class Aluminio(Insumo):
    def __init__(self):
        super().__init__()
        self.nombre = 'Kg de Aluminio'
        self.cargarPrecio()

    def cargarPrecio(self):
        self.precio = Coneccion().obtenerPrecioAluminio()
    def actualizarPrecio(self, nuevo_precio):
        self.precio = nuevo_precio
        Coneccion().actualizarPrecioAluminio(self.precio)


class InsumoMts(Insumo):
    def __init__(self, metros):
        super().__init__()
        self.metros = metros

    def calcularPrecio(self):
        self.cargarPrecio() 
        return self.precio * self.metros

class InsumoCntd(Insumo):
    def __init__(self, cantidad):
        super().__init__()
        self.cantidad = cantidad

    def calcularPrecio(self):
        self.cargarPrecio() 
        return self.precio * self.cantidad

## clases de insumos dependientes de metros ##
class Perfil(InsumoMts):
    def __init__(self, calidad, metros, codigo):
        super().__init__(metros)
        self.calidad = calidad
        self.codigo = codigo

    def cargarPrecio(self):
        self.precio = Coneccion().obtenerPrecioPerfil(self.codigo, self.calidad)
    

class Felpa(InsumoMts):
    def __init__(self, metros=1):
        super().__init__(metros)
        self.codigo = 200
        self.nombre = 'felpa'
        self.cargarPrecio()

class Burlete(InsumoMts):
    def __init__(self, metros=1):
        super().__init__(metros)
        self.codigo = 201
        self.nombre = 'burlete'
        self.cargarPrecio()

class Vidrio(InsumoMts):
    def __init__(self, calidad, metros=1):
        super().__init__(metros)
        self.calidad = calidad
        self.codigo = 202
        self.cargarNombre()
        self.cargarPrecio()

    def cargarNombre(self):
        self.nombre = Coneccion().obtenerNombreVidrio(self.calidad)

    def cargarPrecio(self):
        self.precio = Coneccion().obtenerPrecioVidrio(self.calidad)
            
    def calcularPrecio(self):
        self.cargarPrecio()
        return self.precio * self.metros
        
    def actualizarPrecio(self, nuevo_precio):
        self.precio = nuevo_precio
        Coneccion().actualizarPrecioVidrio(self.codigo, self.calidad, self.precio)


## clases de insumos dependientes de una cantidad ##
class Cierre(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 203
        self.nombre = 'cierre central'
        self.cargarPrecio()

class Rueda(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 204
        self.nombre = 'rueda'
        self.cargarPrecio()

class Tirafondo(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 205
        self.nombre = 'tirafondo'
        self.cargarPrecio()

class Escuadra(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 206
        self.nombre = 'escuadra'
        self.cargarPrecio()

class Remache(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 207
        self.nombre = 'remache'
        self.cargarPrecio()

class AntiRuido(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 208
        self.nombre = 'Anti-ruido'
        self.cargarPrecio()

class ParTJ(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 209
        self.nombre = 'Par T-J'
        self.cargarPrecio()

## clases del modelo de la ventana ##
class Hoja:
    def __init__(self, ancho, alto, calidad):
        self.ancho = ancho
        self.alto = alto
        self.calidad = calidad
        self.metros_vidrio = (self.ancho + .02)*(self.alto - .08)
        self.perfiles = Perfil(self.calidad, self.ancho*2, 1002), Perfil(self.calidad, self.alto, 1003), Perfil(self.calidad, self.alto, 1004)
        self.tirafondo = Tirafondo(4)
        self.rueda = Rueda(2)
        self.vidrio = Vidrio(self.calidad, self.metros_vidrio)
        self.burlete = Burlete(self.ancho*2 + self.alto*2)
        self.felpa = Felpa(self.alto*3 + self.ancho*2)
        self.partj = ParTJ(4)
        self.antiruido = AntiRuido(4)

    def calcularPrecio(self):
        perfiles = sum(p.calcularPrecio() for p in self.perfiles)
        tirafondos = self.tirafondo.calcularPrecio()
        ruedas = self.rueda.calcularPrecio()
        vidrio = self.vidrio.calcularPrecio()
        burlete = self.burlete.calcularPrecio()
        felpa = self.felpa.calcularPrecio()
        partj = self.partj.calcularPrecio()
        antiruido = self.antiruido.calcularPrecio()
        return perfiles + tirafondos + ruedas + vidrio + burlete + felpa + partj + antiruido

class Marco:
    def __init__(self, ancho, alto, calidad):
        self.ancho = ancho
        self.alto = alto
        self.calidad = calidad

        self.perfil = Perfil(self.calidad, (self.ancho)*2 + (self.alto)*2, 1001)
        self.escuadra = Escuadra(4)
        self.remache = Remache(32)
        self.hojas = [Hoja(self.ancho/2 - .094, self.alto - .06, self.calidad) for _ in range(2)]
    
    def calcularPrecio(self):
        perfil = self.perfil.calcularPrecio()
        escuadra = self.escuadra.calcularPrecio()
        remache = self.remache.calcularPrecio()
        hojas = sum(h.calcularPrecio() for h in self.hojas)
        return perfil + escuadra + remache + hojas

class Ventana:    
    def __init__(self, ancho, alto, calidad):
        self.ancho = ancho
        self.alto = alto
        self.calidad = calidad

        self.cierre = Cierre(1)
        self.marco = Marco(self.ancho, self.alto, self.calidad)
    
    def calcularPrecio(self):
        return round( self.marco.calcularPrecio() + self.cierre.calcularPrecio(), 2)

