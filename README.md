# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para el componente práctico del curso **Programación (213023)** de la **Universidad Nacional Abierta y a Distancia (UNAD)**.

## 📋 Descripción del Proyecto
Aplicación de consola desarrollada en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)** sin uso de bases de datos. El sistema administra los clientes, servicios (reservas de salas, alquiler de equipos y asesorías especializadas) y reservas de la empresa **Software FJ**, garantizando estabilidad y continuidad operativa mediante un manejo robusto de excepciones y registro automático de eventos en archivos de log.

## 🏗️ Arquitectura y Conceptos Aplicados
* **Abstracción y Herencia:** Clases abstractas base (`Entidad`, `Servicio`) y clases derivadas especializadas (`Sala`, `Equipo`, `Asesoria`).
* **Polimorfismo y Sobrecarga:** Métodos sobrescritos para validación de parámetros, descripción y cálculo dinámico de costos con impuestos, descuentos y parámetros opcionales.
* **Encapsulación:** Protección y validación estricta de datos personales en la clase `Cliente` y control de estados en la clase `Reserva`.
* **Manejo Avanzado de Excepciones:** Excepciones personalizadas, encadenamiento de excepciones (`raise ... from ...`) y uso estructurado de bloques `try / except / else / finally`.
* **Persistencia en Memoria y Logs:** Gestión de datos mediante listas internas de objetos y registro de errores/eventos en un archivo `.log` plano.

## 🌿 Estructura de Ramas del Repositorio
* `main`: Versión estable e integrada del sistema funcional.
* `feature/excepciones-logs`: Excepciones personalizadas y sistema de registro en archivo de logs.
* `feature/entidades-clientes`: Clase abstracta base y clase `Cliente` con validaciones.
* `feature/servicios`: Clase abstracta `Servicio` y servicios especializados.
* `feature/reservas-main`: Clase `Reserva` y simulación de las 10 operaciones completas.

## 🚀 Ejecución
1. Clonar el repositorio:
   ```bash
   git clone https://github.com
   ```
2. Ejecutar el archivo principal:
   ```bash
   python main.py
   ```
