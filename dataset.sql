-- Crear tabla Restaurante
CREATE TABLE Restaurante (
  restaurante_id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  direccion TEXT NOT NULL,
  tipo_cocina VARCHAR(100) NOT NULL,
  capacidad_maxima INTEGER CHECK (capacidad_maxima > 0),
  horario_apertura TIME NOT NULL,
  horario_cierre TIME NOT NULL
);

-- Crear tabla Cliente
CREATE TABLE Cliente (
  cliente_id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  direccion TEXT,
  telefono VARCHAR(20),
  correo VARCHAR(255) UNIQUE
);

-- Crear tabla Mesa
CREATE TABLE Mesa (
  mesa_id SERIAL PRIMARY KEY,
  numero_mesa INTEGER NOT NULL CHECK (numero_mesa > 0),
  estado VARCHAR(50) NOT NULL CHECK (estado IN ('disponible', 'ocupada', 'reservada')),
  capacidad INTEGER CHECK (capacidad > 0),
  restaurante_id INTEGER NOT NULL REFERENCES Restaurante(restaurante_id) ON DELETE CASCADE
);

-- Crear tabla Reserva
CREATE TABLE Reserva (
  reserva_id SERIAL PRIMARY KEY,
  hora TIME NOT NULL,
  numero_comensales INTEGER CHECK (numero_comensales > 0),
  observaciones TEXT,
  estado VARCHAR(50) NOT NULL CHECK (estado IN ('pendiente', 'confirmada', 'cancelada')),
  fecha DATE NOT NULL,
  mesa_id INTEGER NOT NULL REFERENCES Mesa(mesa_id) ON DELETE SET NULL,
  cliente_id INTEGER REFERENCES Cliente(cliente_id) ON DELETE SET NULL
);

-- Crear tabla Platos
CREATE TABLE Platos (
  plato_id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  precio NUMERIC(5, 2) CHECK (precio > 0),
  tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('entrada', 'principal', 'postre', 'bebida')),
  restaurante_id INTEGER NOT NULL REFERENCES Restaurante(restaurante_id) ON DELETE CASCADE
);

-- Crear tabla Proveedor
CREATE TABLE Proveedor (
  proveedor_id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  direccion TEXT,
  telefono VARCHAR(20),
  tipo_suministro VARCHAR(255) NOT NULL
);

-- Crear tabla DetalleReserva (asumiendo que esta es una tabla de unión entre Reserva y Platos)
CREATE TABLE DetalleReserva (
  detalle_id SERIAL PRIMARY KEY,
  reserva_id INTEGER NOT NULL REFERENCES Reserva(reserva_id) ON DELETE CASCADE,
  plato_id INTEGER NOT NULL REFERENCES Platos(plato_id) ON DELETE RESTRICT,
  cantidad INTEGER NOT NULL CHECK (cantidad > 0),
  precio NUMERIC(5, 2) NOT NULL CHECK (precio > 0) -- Suponiendo que se pueda sobrescribir el precio por ofertas especiales
);