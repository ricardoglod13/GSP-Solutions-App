DROP TABLE IF EXISTS producto;

CREATE TABLE producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(12) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    descripcion TEXT NOT NULL,
    precio_costo FLOAT NOT NULL,
    precio_venta FLOAT NOT NULL,
    cantidad INTEGER NOT NULL
);

DROP TABLE IF EXISTS contacto;

CREATE TABLE contacto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento VARCHAR(15) NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion TEXT NOT NULL,
    deuda_favor FLOAT NOT NULL DEFAULT 0.00,
    deuda_contra FLOAT NOT NULL DEFAULT 0.00,
    tipo VARCHAR(20) NOT NULL
);

DROP TABLE IF EXISTS venta;

CREATE TABLE venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_contacto VARCHAR(20) NOT NULL,
    documento_sucursal VARCHAR(20) NOT NULL,
    items TEXT,
    pago_inmediato BOOLEAN NOT NULL,
    total FLOAT,
    fecha TEXT NOT NULL
);

DROP TABLE IF EXISTS compra;

CREATE TABLE compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_sucursal VARCHAR(15) NOT NULL,
    documento_proveedor VARCHAR(20) NOT NULL,
    items TEXT,
    pago_inmediato BOOLEAN NOT NULL,
    total FLOAT,
    fecha TEXT NOT NULL
);

DROP TABLE IF EXISTS abono;

CREATE TABLE abono (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento_contacto VARCHAR(15) NOT NULL,
    cant_abono FLOAT NOT NULL,
    fecha TEXT NOT NULL
);