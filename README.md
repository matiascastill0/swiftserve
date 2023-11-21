# swiftserve
SwiftServe es un sistema de gestión de pedidos para restaurantes que digitaliza el proceso de toma de órdenes. Elimina la necesidad de papel y acelera la facturación, generando automáticamente facturas detalladas para un proceso de pago eficiente


# SwiftServe Database Documentation

Este repositorio contiene los archivos necesarios para configurar la base de datos del sistema de gestión de pedidos SwiftServe para restaurantes.

## Estructura de Archivos

- `consultas.sql`: Este archivo incluye las consultas SQL utilizadas para extraer información de la base de datos. Además, contiene las declaraciones de índices que optimizan estas consultas para mejorar el rendimiento.

- `dataset.sql`: Este archivo contiene las declaraciones SQL para crear la estructura de la base de datos. Incluye la definición de todas las tablas y las relaciones entre ellas necesarias para almacenar y gestionar los datos de los restaurantes.

## Uso

Para utilizar estos archivos, siga estos pasos:

1. Asegúrese de tener instalado PostgreSQL y acceso a un servidor PostgreSQL.
2. Abra una interfaz de línea de comandos para PostgreSQL, como psql, o una interfaz gráfica, como pgAdmin.
3. Ejecute `dataset.sql` para crear las tablas en su base de datos.
4. Ejecute `consultas.sql` para realizar las consultas en la base de datos ya poblada.

## Contribuciones

Para contribuir a este proyecto, por favor envíe un pull request con sus sugerencias.

## Licencia

Este proyecto está licenciado bajo [BasedeDatos-Brenner Ojeda] - ver el archivo LICENSE.md para más detalles.

