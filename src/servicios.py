"""
Módulo que implementa la jerarquía de servicios de Software FJ.
Aplica abstracción, herencia, polimorfismo y sobrecarga simulada mediante parámetros opcionales.
"""
from abc import ABC, abstractmethod
from src.excepciones import DatoInvalidoError, ParametroFaltanteError, ServicioNoDisponibleError


class Servicio(ABC):
    """Clase abstracta base para cualquier servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Valida parámetros obligatorios
        if not id_servicio or not str(id_servicio).strip():
            raise ParametroFaltanteError("El ID del servicio es obligatorio.")
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base del servicio debe ser mayor a cero.")

        self._id = str(id_servicio).strip()
        self._nombre = str(nombre).strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    def validar_disponibilidad(self) -> None:
        """Verifica si el servicio está activo para ser reservado."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no se encuentra disponible.")

    @abstractmethod
    def calcular_costo(self, cantidad: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """
        Método abstracto polimórfico que calcula el valor total del servicio.
        Soporta sobrecarga mediante parámetros opcionales (descuento e IVA).
        """
        pass

    @abstractmethod
    def obtener_detalle(self) -> str:
        """Retorna la descripción específica del servicio."""
        pass


class ReservaSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, tiene_proyector: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a cero.")
        self.capacidad = int(capacidad)
        self.tiene_proyector = bool(tiene_proyector)

    def calcular_costo(self, horas: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo por horas de uso de la sala más recargo por proyector."""
        if horas <= 0:
            raise DatoInvalidoError("Las horas de reserva de sala deben ser mayores a cero.")
        if not (0 <= descuento <= 0.5):
            raise DatoInvalidoError("El descuento debe estar entre 0.0 (0%) y 0.5 (50%).")

        subtotal = self._tarifa_base * horas
        # Si incluye proyector, suma un cargo fijo de 15000 COP
        if self.tiene_proyector:
            subtotal += 15000.0
        subtotal -= subtotal * descuento
        return round(subtotal * 1.19 if aplicar_iva else subtotal, 2)

    def obtener_detalle(self) -> str:
        proyector_txt = "Con proyector" if self.tiene_proyector else "Sin proyector"
        return f"Sala [{self.id}] {self.nombre} (Cap: {self.capacidad} pers., {proyector_txt}) - ${self._tarifa_base:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Servicio especializado para el préstamo o alquiler de equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, gama: str, incluye_seguro: bool = True):
        super().__init__(id_servicio, nombre, tarifa_dia)
        if gama.lower() not in ("estandar", "profesional", "servidor"):
            raise DatoInvalidoError("La gama del equipo debe ser: estandar, profesional o servidor.")
        self.gama = gama.lower()
        self.incluye_seguro = bool(incluye_seguro)

    def calcular_costo(self, dias: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo por días de alquiler del equipo y seguro opcional."""
        if dias <= 0:
            raise DatoInvalidoError("Los días de alquiler deben ser mayores a cero.")
        if not (0 <= descuento <= 0.5):
            raise DatoInvalidoError("El descuento debe estar entre 0.0 (0%) y 0.5 (50%).")

        subtotal = self._tarifa_base * dias
        # Si incluye seguro contra daños, suma 10% sobre el subtotal
        if self.incluye_seguro:
            subtotal *= 1.10
        subtotal -= subtotal * descuento
        return round(subtotal * 1.19 if aplicar_iva else subtotal, 2)

    def obtener_detalle(self) -> str:
        seguro_txt = "Con seguro" if self.incluye_seguro else "Sin seguro"
        return f"Equipo [{self.id}] {self.nombre} (Gama {self.gama}, {seguro_txt}) - ${self._tarifa_base:,.0f}/día"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o desarrollo a medida."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_sesion: float, especialidad: str, es_remota: bool = True):
        super().__init__(id_servicio, nombre, tarifa_sesion)
        if not especialidad or not str(especialidad).strip():
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        self.especialidad = str(especialidad).strip()
        self.es_remota = bool(es_remota)

    def calcular_costo(self, sesiones: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo por sesiones; si es presencial agrega viáticos."""
        if sesiones <= 0:
            raise DatoInvalidoError("El número de sesiones debe ser mayor a cero.")
        if not (0 <= descuento <= 0.5):
            raise DatoInvalidoError("El descuento debe estar entre 0.0 (0%) y 0.5 (50%).")

        subtotal = self._tarifa_base * sesiones
        # Si la asesoría es presencial, agrega un recargo fijo por desplazamiento
        if not self.es_remota:
            subtotal += 25000.0
        subtotal -= subtotal * descuento
        return round(subtotal * 1.19 if aplicar_iva else subtotal, 2)

    def obtener_detalle(self) -> str:
        modalidad = "Remota" if self.es_remota else "Presencial"
        return f"Asesoría [{self.id}] {self.nombre} ({self.especialidad} - {modalidad}) - ${self._tarifa_base:,.0f}/sesión"
