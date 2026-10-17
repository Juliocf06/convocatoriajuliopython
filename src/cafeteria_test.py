from cafeteria import *

def test_lee_pedidos(fichero: str) -> list[Pedido]:
    print("TEST lee_pedidos")
    print("Número de registros leídos: ", len(fichero))
    print("\n Los tres primeros registros son:")
    for registro in fichero[:3]:
        print(registro, "\n")

def test_ingreso_total_por_franja(pedidos: list[Pedido],hora_inicio: int,hora_fin: int, metodo_pago: str|None = None):
    if (metodo_pago is None):
        print(f"TEST ingreso_total_por_franja '{hora_inicio}-{hora_fin}'\n", ingreso_total_por_franja(pedidos, hora_inicio, hora_fin, metodo_pago), "€")
    else:
        print(f"TEST ingreso_total_por_franja '{hora_inicio}-{hora_fin}' con método de pago {metodo_pago} \n", ingreso_total_por_franja(pedidos, hora_inicio, hora_fin, metodo_pago), "€")

def test_analisis_propinas_ubicacion(pedidos: list[Pedido],metodo_pago: str):
    mesa, cantidad = analisis_propinas_ubicacion(pedidos, metodo_pago)
    print(f"TEST análisis propinas por ubicación para método de pago: {metodo_pago}")
    print(f"Ubicación con el promedio de propina más alto: {mesa} ({cantidad}%)")

def test_producto_mas_asociado(pedidos: list[Pedido],nombre_producto:str):
    print(f"TEST producto_mas_asociado para producto: {nombre_producto}")
    print("Producto más asociado:", producto_mas_asociado(pedidos, nombre_producto))




if __name__ == "__main__":
    fichero = lee_pedidos(("data/pedidos.csv"))
    print("*********Ejercicio 1*********")
    test_lee_pedidos(fichero)
    print("*********Ejercicio 2*********")
    test_ingreso_total_por_franja(fichero, 8, 12)
    test_ingreso_total_por_franja(fichero, 12, 18, "Tarjeta")
    test_ingreso_total_por_franja(fichero, 18, 24, "Bizum")
    print("*********Ejercicio 3*********")
    test_analisis_propinas_ubicacion(fichero, "Efectivo")
    test_analisis_propinas_ubicacion(fichero, "Tarjeta")
    test_analisis_propinas_ubicacion(fichero, "Bizum")
    print("*********Ejercicio 4*********")
    test_producto_mas_asociado(fichero, "Hamburguesa_Completa")