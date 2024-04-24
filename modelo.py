import pyodbc


consulta_precio_perfil = lambda n, n_c: f"select precio/metros from Insumos where nombre = '{n}' and nivel_calidad = {n_c}"
consulta_precio_porcantidad = lambda n: f"select precio/cantidad from Insumos where nombre = '{n}'"
consulta_precio_pormetro = lambda n: f"select precio/metros from Insumos where nombre = '{n}'"


class Conexion:
    def __init__(self):
        self.server = 'DESKTOP-1VRJ5PA\\MSSQLSERVER01' 
        self.db = 'Aberturas'
        self.user = 'ventana'
        self.password = '123'
        
    def establecer_coneccion(self):
        self.coneccion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; '+
                                        'SERVER='+self.server+';'+
                                        'DATABASE='+self.db+';'+
                                        'UID='+self.user+';'+
                                        'PWD='+self.password+';')
        # self.cursor = self.coneccion.cursor()
    def cerrar_coneccion(self):
        self.coneccion.close()


    def precio_pmetro_perfil(self, nombre, nivel_calidad):
        precio = self.coneccion.execute(consulta_precio_perfil(nombre, nivel_calidad)).fetchone()[0]
        return float( round(precio, 4) )

    def precio_pcantidad(self, nombre):
        precio = self.coneccion.execute(consulta_precio_porcantidad(nombre)).fetchone()[0]
        return float( round(precio, 4) )

    def precio_pmetro(self, nombre):
        precio = self.coneccion.execute(consulta_precio_pormetro(nombre)).fetchone()[0]
        return float( round(precio, 4) )    
    
    # def obtener_fila(self, nombre):
    #     return self.coneccion.execute(f"select TOP 1 * from Insumos where nombre = '{nombre}'").fetchone()

    # def obtener_perfil(self, nombre, n_c):
    #     return self.coneccion.execute(f"select TOP 1 * from Insumos where nombre = '{nombre}' and nivel_calidad = '{n_c}'").fetchone()

    def obtener_tabla(self):
        return self.coneccion.execute('select * from Insumos').fetchall()


    def actualizar_perfil(self, nombre, n_c, metros, precio):
        try:
            metros, precio  =  float(metros), float(precio) 
            self.coneccion.execute(f"update Insumos set metros = {metros}, precio = {precio} WHERE nombre = '{nombre}' and nivel_calidad = {int(n_c)}")
            self.coneccion.commit()
        except:
            ValueError
    
    def actualizar_por_metros(self, nombre, metros, precio):
        try:
            metros, precio = float(metros), float(precio)
            self.coneccion.execute(f"update Insumos set metros = {metros}, precio = {precio} WHERE nombre = '{nombre}'")
            self.coneccion.commit()
        except:
            ValueError
    
    def actualizar_por_cantidad(self, nombre, cantidad, precio):
        try:
            cantidad, precio = float(cantidad), float(precio)
            self.coneccion.execute(f"update Insumos set cantidad = {cantidad}, precio = {precio} WHERE nombre = '{nombre}'")
            self.coneccion.commit()
        except:
            ValueError



conn = Conexion()

conn.establecer_coneccion()





class Burlete:
    def __init__(self, metros):
        self.nombre = 'burlete'
        self.metros = metros
    def calcular_precio(self):
        return conn.precio_pmetro(self.nombre) * self.metros

class Felpa:
    def __init__(self, metros):
        self.nombre = 'felpa'
        self.metros = metros
    def calcular_precio(self):
        return conn.precio_pmetro(self.nombre) * self.metros

class Escuadra:
    def __init__(self, cantidad):
        self.nombre = 'escuadra'
        self.cantidad = cantidad
    def calcular_precio(self):
        return conn.precio_pcantidad(self.nombre) * self.cantidad

class Remache:
    def __init__(self, cantidad):
        self.nombre = 'remache'
        self.cantidad = cantidad
    def calcular_precio(self):
        return conn.precio_pcantidad(self.nombre) * self.cantidad

class Rueda:
    def __init__(self, cantidad):
        self.nombre = 'rueda'
        self.cantidad = cantidad
    def calcular_precio(self):
        return conn.precio_pcantidad(self.nombre) * self.cantidad


class Tirafondo:
    def __init__(self, cantidad):
        self.nombre = 'tirafondo'   
        self.cantidad = cantidad
    def calcular_precio(self):
        return conn.precio_pcantidad(self.nombre) * self.cantidad


class Panel_vidrio:
    def __init__(self, metrosC):
        self.nombre = 'vidrio'
        self.metrosC = metrosC
    def calcular_precio(self):
        return conn.precio_pmetro(self.nombre) * self.metrosC

class Perfil:
    def __init__(self, tipo, nive_calidad, metros):
        self.tipo = tipo
        self.nivel_calidad = nive_calidad
        self.metros = metros
        
    def calcular_precio(self):
        return conn.precio_pmetro_perfil(self.tipo, self.nivel_calidad) * self.metros
    

class Hoja:
    def __init__(self, ancho, alto, nivel_calidad):
        self.ancho = ancho
        self.alto = alto
        self.nivel_calidad = nivel_calidad
        self.umbral = Perfil('p_dintel_umbral', self.nivel_calidad, self.ancho*2 - 0.2)
        self.parante_cen = Perfil('p_parante_central', self.nivel_calidad, self.alto)
        self.parante_lat = Perfil('p_parante_lateral', self.nivel_calidad, self.alto)
        self.panel_vidrio = Panel_vidrio( (self.ancho - 0.16)*(self.alto - 0.16) )
        self.rueda = Rueda(2)
        self.tirafondo = Tirafondo(4)
        self.burlete = Burlete(self.ancho*2 + self.alto*2)
        self.felpa = Felpa(self.alto*3 + self.ancho*2)
    def calcular_precio(self):
        umbral_dintel = self.umbral.calcular_precio()
        parante_c = self.parante_cen.calcular_precio()
        parante_l = self.parante_lat.calcular_precio()
        vidrio = self.panel_vidrio.calcular_precio()
        ruedas = self.rueda.calcular_precio()
        tirafondos = self.tirafondo.calcular_precio()
        burlete = self.burlete.calcular_precio()
        felpa = self.felpa.calcular_precio()
        return umbral_dintel+parante_c+parante_l+vidrio+ruedas+tirafondos+burlete+felpa


class Marco:
    def __init__(self, ancho, alto, nivel_calidad):
        self.ancho = ancho
        self.alto = alto
        self.nivel_calidad = nivel_calidad
        self.perfil = Perfil('p_marco', self.nivel_calidad, self.ancho*2 + self.alto*2)
        self.hoja_x_2 = Hoja(self.ancho/2 - 0.094, self.alto - 0.06, self.nivel_calidad)
        self.remache = Remache(32)
        self.escuadra = Escuadra(4)

    def calcular_precio(self):
        perfil = self.perfil.calcular_precio()
        hojas = self.hoja_x_2.calcular_precio()*2
        remaches = self.remache.calcular_precio()
        escuadras = self.escuadra.calcular_precio()

        return  perfil + hojas + remaches + escuadras



class Ventana:
    def __init__(self, ancho, alto, nivel_calidad):
        self.ancho = ancho
        self.alto = alto
        self.nivel_calidad = nivel_calidad
        self.marco = Marco(self.ancho, self.alto, self.nivel_calidad)
    
    def calcular_precio(self):
        return round( self.marco.calcular_precio(), 2)

