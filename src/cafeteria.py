import csv
from typing import NamedTuple
from datetime import datetime

LineaPedido = NamedTuple("LineaPedido", [
 ("producto", str),
 ("categoria", str),
 ("cantidad", int),
 ("precio_unitario", float)
])

Pedido = NamedTuple("Pedido", [
 ("id_pedido", int),
 ("fecha_hora", datetime),
 ("mesa", str),
 ("metodo_pago", str),
 ("propina", float),
 ("lineas", list[LineaPedido])
])

def lee_pedidos(ruta_fichero: str) -> list[Pedido]:
    with open(ruta_fichero, "rt", encoding="utf-8") as f:
        lector = csv.reader(f, delimiter=";")
        next(lector)
        lista = []
        for id_pedido, fecha_hora, mesa, metodo_pago, propina, lineas in lector:
            id_pedido = int(id_pedido)
            fecha_hora = parseaFecha(fecha_hora)
            mesa = mesa
            metodo_pago = metodo_pago
            propina = float(propina)
            lineas = parseaLineas(lineas)
            tupla = Pedido(id_pedido, fecha_hora, mesa, metodo_pago, propina, lineas)
            lista.append(tupla)
    return lista

def parseaFecha(fecha:str)->datetime:
    res = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
    return res

def parseaLineas(linea_pedido:str)->list[LineaPedido]:
    lista = []
    lineas = linea_pedido.split("*")
    for linea in lineas:
        lista.append(parseaLinea(linea))
    return lista
    
def parseaLinea (linea:str)->LineaPedido:
    line = linea.split("-")
    producto, categoria, cantidad, precio_unitario = line
    producto = producto
    categoria = categoria
    cantidad = int(cantidad)
    precio_unitario = float(precio_unitario)
    tupla = LineaPedido(producto, categoria, cantidad, precio_unitario)
    return tupla


def ingreso_total_por_franja(pedidos: list[Pedido],hora_inicio: int,hora_fin: int, metodo_pago: str|None = None) -> float:
    res = 0
    for pedido in pedidos:
        if (hora_inicio <= pedido.fecha_hora.hour<hora_fin and (metodo_pago == pedido.metodo_pago or metodo_pago is None)):
            res += pedido.propina
            for linea in pedido.lineas:
                res += linea.precio_unitario*linea.cantidad
    return round(res, 2)

def analisis_propinas_ubicacion(pedidos: list[Pedido],metodo_pago: str) -> tuple[str, float]:
    mesas = {}
    contador = {}
    res = []
    for pedido in pedidos:
        if(metodo_pago == pedido.metodo_pago):
            if (pedido.mesa not in mesas):
                mesas[pedido.mesa] = 0
                contador[pedido.mesa] = 0
            mesas[pedido.mesa]+= (pedido.propina/calcular_precio_total(pedido))*100
            contador[pedido.mesa]+=1
    propinas = list(mesas.items())
    for propina in propinas:
        res.append((propina[0] ,round(propina[1]/contador[propina[0]], 2)))
    ordenado = sorted(res, key=lambda x:x[1], reverse=True)
    return ordenado[0]

def calcular_precio_total(pedido:Pedido):
    res=0
    for producto in pedido.lineas:
        res += producto.precio_unitario*producto.cantidad
    return res

def producto_mas_asociado(pedidos: list[Pedido],nombre_producto:str) -> str:
    parejas = {}
    for pedido in pedidos:
        conjunto = set()
        indices = len(pedido.lineas)
        if (indices>1):
            for linea in pedido.lineas:
                conjunto.add(linea.producto)
        if(nombre_producto in conjunto):
            conjunto.remove(nombre_producto)
            for producto in conjunto:
                if (producto not in parejas):
                    parejas[producto] = 0
                parejas[producto] +=1
    lista = sorted(list(parejas.items()), key=lambda x:x[1], reverse=True)
    return lista[0][0]
