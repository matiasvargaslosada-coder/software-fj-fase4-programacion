"""
Script principal de ejecución y simulación del Sistema Integral de Software FJ.
Ejecuta 10 operaciones que validan el flujo completo, cálculos polimórficos,
control de estados, manejo de excepciones y generación del archivo de logs.
"""
from src.entidades import Cliente
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.reservas import GestorSoftwareFJ
from src.excepciones import ErrorSistemaFJ


def ejecutar_simulacion():
    print("=" * 80)
    print(" SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ")
    print("=" * 80)

    # Instancia el gestor principal del sistema con archivo de log
    gestor = GestorSoftwareFJ("sistema_fj.log")

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro exitoso de múltiples clientes
    # -------------------------------------------------------------------------
    print("\n Registrando clientes válidos...")
    c1 = Cliente("CLI-001", "Laura Martínez", "laura.martinez@empresa.com", "3104567890")
    c2 = Cliente("CLI-002", "Carlos Gómez", "carlos.gomez@tech.co", "3209876543")
    c3 = Cliente("CLI-003", "Andrés Rojas", "andres.rojas@correo.org", "3001122334")
    for cliente in (c1, c2, c3):
        gestor.registrar_cliente(cliente)
        print("   ->", cliente.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Intento de registro de cliente con datos inválidos (Excepción)
    # -------------------------------------------------------------------------
    print("\n Probando validación de cliente con correo inválido...")
    try:
        Cliente("CLI-999", "Pedro", "correo-sin-arroba.com", "123")
    except ErrorSistemaFJ as err:
        gestor.logger.registrar_error("Validación fallida de cliente", err)
        print(f"   -> Excepción controlada ({type(err).__name__}): {err}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Registro de los 3 tipos especializados de servicios
    # -------------------------------------------------------------------------
    print("\n Registrando catálogo de servicios...")
    s1 = ReservaSala("SRV-01", "Sala Ejecutiva Norte", 80000, capacidad=12, tiene_proyector=True)
    s2 = AlquilerEquipo("SRV-02", "Workstation Dell Precision", 65000, gama="profesional", incluye_seguro=True)
    s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud AWS", 150000, especialidad="Cloud", es_remota=False)
    for servicio in (s1, s2, s3):
        gestor.registrar_servicio(servicio)
        print("   ->", servicio.obtener_detalle())

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Creación de reservas válidas con cálculo polimórfico
    # -------------------------------------------------------------------------
    print("\n Creando reservas válidas...")
    r1 = gestor.crear_reserva("RES-101", c1, s1, "2026-12-01", cantidad=4, descuento=0.10)
    r2 = gestor.crear_reserva("RES-102", c2, s2, "2026-12-02", cantidad=3, descuento=0.0)
    r3 = gestor.crear_reserva("RES-103", c3, s3, "2026-12-05", cantidad=2, descuento=0.15)
    for reserva in (r1, r2, r3):
        print("   ->", reserva.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Confirmación de reservas y bloqueo de disponibilidad
    # -------------------------------------------------------------------------
    print("\n Confirmando reserva RES-101 y RES-102...")
    r1.confirmar()
    gestor.logger.registrar_evento("INFO", f"Reserva confirmada: {r1.id}")
    r2.confirmar()
    gestor.logger.registrar_evento("INFO", f"Reserva confirmada: {r2.id}")
    print(f"   -> Estado {r1.id}: {r1.estado} | Servicio disponible: {s1.disponible}")
    print(f"   -> Estado {r2.id}: {r2.estado} | Servicio disponible: {s2.disponible}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Intento de reservar un servicio ya ocupado (Excepción encadenada)
    # -------------------------------------------------------------------------
    print("\n Intentando reservar sala ya ocupada (RES-104)...")
    try:
        gestor.crear_reserva("RES-104", c3, s1, "2026-12-01", cantidad=2)
    except ErrorSistemaFJ as err:
        print(f"   -> Error capturado ({type(err).__name__}): {err}")
        if err.__cause__:
            print(f"      Causa encadenada ({type(err.__cause__).__name__}): {err.__cause__}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Intento de confirmar una reserva que ya está confirmada
    # -------------------------------------------------------------------------
    print("\n Intentando reconfirmar reserva RES-101...")
    try:
        r1.confirmar()
    except ErrorSistemaFJ as err:
        gestor.logger.registrar_error("Cambio de estado inválido", err)
        print(f"   -> Excepción controlada ({type(err).__name__}): {err}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Cancelación de reserva y liberación automática del servicio
    # -------------------------------------------------------------------------
    print("\n Cancelando reserva RES-101 para liberar la sala...")
    r1.cancelar()
    gestor.logger.registrar_evento("INFO", f"Reserva cancelada: {r1.id}. Servicio {s1.id} liberado.")
    print(f"   -> Estado {r1.id}: {r1.estado} | Servicio disponible nuevamente: {s1.disponible}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Nueva reserva exitosa sobre el servicio recién liberado
    # -------------------------------------------------------------------------
    print("\n Creando nueva reserva RES-105 sobre la sala liberada...")
    r5 = gestor.crear_reserva("RES-105", c3, s1, "2026-12-03", cantidad=3, descuento=0.05)
    r5.confirmar()
    print("   ->", r5.obtener_resumen())

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Intento de reserva con fecha en formato inválido
    # -------------------------------------------------------------------------
    print("\n Probando validación de fecha con formato incorrecto...")
    try:
        gestor.crear_reserva("RES-106", c1, s3, "05/12/2026", cantidad=1)
    except ErrorSistemaFJ as err:
        print(f"   -> Excepción controlada ({type(err).__name__}): {err}")

    # Resumen final en consola
    print("\n" + "=" * 80)
    print(f" RESUMEN FINAL: {len(gestor.clientes)} Clientes | {len(gestor.servicios)} Servicios | {len(gestor.reservas)} Reservas")
    print(" Los eventos y errores quedaron registrados en el archivo 'sistema_fj.log'.")
    print("=" * 80)


if __name__ == "__main__":
    ejecutar_simulacion()
