-- Índices para optimización

-- Índice para mejorar el rendimiento de la consulta 1
CREATE INDEX idx_detalle_reserva_restaurante_id ON DetalleReserva(restaurante_id);

-- Índice para mejorar el rendimiento de la consulta 2
CREATE INDEX idx_reserva_fecha ON Reserva(fecha);

-- Índice para mejorar el rendimiento de la consulta 3
CREATE INDEX idx_platos_tipo ON Platos(tipo);
CREATE INDEX idx_detalle_reserva_plato_id ON DetalleReserva(plato_id);

-- Índice para mejorar el rendimiento de la consulta 4
CREATE INDEX idx_reserva_estado_fecha ON Reserva(estado, fecha);

-- Consultas

-- Consulta 1: Calcula el promedio de ventas por restaurante.
SELECT R.restaurante_id, R.nombre, AVG(D.cantidad) AS promedio_ventas
FROM Restaurante R
JOIN DetalleReserva D ON R.restaurante_id = D.restaurante_id
GROUP BY R.restaurante_id, R.nombre
ORDER BY promedio_ventas DESC;

-- Consulta 2: Compara el número de reservas del año actual contra el año anterior.
SELECT EXTRACT(YEAR FROM fecha) AS año, COUNT(*) AS total_reservas
FROM Reserva
GROUP BY año
ORDER BY año;

-- Consulta 3: Cuenta la cantidad de platos vendidos agrupados por tipo de plato.
SELECT P.tipo, COUNT(D.plato_id) AS cantidad_vendida
FROM Platos P
JOIN DetalleReserva D ON P.plato_id = D.plato_id
GROUP BY P.tipo
ORDER BY cantidad_vendida DESC;

-- Consulta 4: Encuentra el número de reservas pendientes para los próximos 7 días.
SELECT fecha, COUNT(*) AS total_reservas_pendientes
FROM Reserva
WHERE estado = 'pendiente' AND fecha BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
GROUP BY fecha
ORDER BY fecha;