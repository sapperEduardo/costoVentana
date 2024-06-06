import json

Datos = {}

def cargar_datos():
    global Datos
    with open('datos.json', 'r') as f:
        Datos = json.load(f)

def guardar_datos():
    global Datos
    with open('datos.json', 'w') as f:
        json.dump(Datos, f, indent=1)

def obtener_precio(codigo):
    global Datos
    for insumo in Datos["insumos"]:
        if codigo == insumo["codigo"]:
            return insumo["precio"]
    

def actualizar_precio_kg_aluminio(nuevo_precio_kg_aluminio):
    global Datos
    Datos['precio_kg_aluminio'] = nuevo_precio_kg_aluminio

def actualizar_precio_insumo(codigo, nuevo_precio):
    global Datos
    for insumo in Datos['insumos']:
        if insumo['codigo'] == codigo:
            insumo['precio'] = nuevo_precio
            break

def actualizar_precio_vidrio(codigo, calidad, nuevo_precio):
    global Datos
    for insumo in Datos['insumos']:
        if insumo['codigo'] == codigo and insumo['calidad'] == calidad:
            insumo['precio'] = nuevo_precio
            break

def obtener_lista_precios():
    global Datos
    if Datos == None: cargar_datos()
    lista = []
    lista.append( ("precio kg aluminio", float(Datos["precio_kg_aluminio"]) )  )
    
    for insumo in Datos["insumos"]:
        lista.append( ( insumo["nombre"], float( insumo["precio"] ) ) )

    return lista

def guardar_precios(lista):
    global Datos
    if Datos == None: cargar_datos()
    actualizar_precio_kg_aluminio(lista[0][1])
    actualizar_precio_insumo(200, lista[1][1])
    actualizar_precio_insumo(201, lista[2][1])
    actualizar_precio_vidrio(202, 1, lista[3][1])
    actualizar_precio_vidrio(202, 2, lista[4][1])

    for c, tupla in zip( range(203,2010), lista[5:]):
        precio = tupla[1]
        actualizar_precio_insumo(c, precio)

    guardar_datos()


## clases de insumos ##
class Insumo:
    def __init__(self):
        self.codigo = 0
        self.nombre = ''
        self.calidad = 1
    
    def actualizarPrecio(self, nuevo_precio):
        actualizar_precio_insumo(self.codigo, nuevo_precio)

class InsumoMts(Insumo):
    def __init__(self, metros):
        super().__init__()
        self.metros = metros

    def calcularPrecio(self):
        return obtener_precio(self.codigo) * self.metros

class InsumoCntd(Insumo):
    def __init__(self, cantidad):
        super().__init__()
        self.cantidad = cantidad

    def calcularPrecio(self):
        return obtener_precio(self.codigo) * self.cantidad

## clases de insumos dependientes de metros ##
class Perfil(InsumoMts):
    def __init__(self, calidad, metros, codigo):
        super().__init__(metros)
        self.calidad = calidad
        self.codigo = codigo

    def calcularPrecio(self):
        global Datos
        for p in Datos["perfiles_aluminio"]:
            if self.codigo == p["codigo"] and self.calidad == p["calidad"]: 
                return p["kg/mts"] * self.metros * Datos["precio_kg_aluminio"]
        return None

class Felpa(InsumoMts):
    def __init__(self, metros=1):
        super().__init__(metros)
        self.codigo = 200
        self.nombre = 'felpa'

class Burlete(InsumoMts):
    def __init__(self, metros=1):
        super().__init__(metros)
        self.codigo = 201
        self.nombre = 'burlete'

class Vidrio(InsumoMts):
    def __init__(self, calidad, metros=1):
        super().__init__(metros)
        self.calidad = calidad
        self.codigo = 202

    def calcularPrecio(self):
        global Datos
        for insumo in Datos["insumos"]:
            if self.codigo == insumo["codigo"] and self.calidad == insumo["calidad"]: 
                return insumo["precio"] * self.metros
        
            
    def actualizarPrecio(self, nuevo_precio):
        actualizar_precio_vidrio(self.codigo, self.calidad, nuevo_precio)

## clases de insumos dependientes de una cantidad ##
class Cierre(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 203
        self.nombre = 'cierre central'

class Rueda(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 204
        self.nombre = 'rueda'

class Tirafondo(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 205
        self.nombre = 'tirafondo'

class Escuadra(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 206
        self.nombre = 'escuadra'

class Remache(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 207
        self.nombre = 'remache'

class AntiRuido(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 208
        self.nombre = 'Anti-ruido'

class ParTJ(InsumoCntd):
    def __init__(self, cantidad=1):
        super().__init__(cantidad)
        self.codigo = 209
        self.nombre = 'Par T-J'

## clases del modelo de la ventana ##
class Hoja:
    def __init__(self, ancho, alto, calidad):
        self.ancho = ancho
        self.alto = alto
        self.calidad = calidad
        self.metros_vidrio = (self.ancho - .08)*(self.alto - .08)
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
        cargar_datos()
        return round( self.marco.calcularPrecio() + self.cierre.calcularPrecio(), 2)

