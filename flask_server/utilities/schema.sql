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
    credito FLOAT NOT NULL DEFAULT 0.00,
    deuda FLOAT NOT NULL DEFAULT 0.00,
    tipo VARCHAR(20) NOT NULL
);

DROP TABLE IF EXISTS venta;

CREATE TABLE venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deudor VARCHAR(20) NOT NULL,
    acreedor VARCHAR(20) NOT NULL,
    items TEXT,
    pago_inmediato BOOLEAN NOT NULL,
    cantidad_pagada FLOAT NOT NULL DEFAULT 0.00,
    total FLOAT,
    fecha TEXT NOT NULL
);

DROP TABLE IF EXISTS compra;

CREATE TABLE compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deudor VARCHAR(15) NOT NULL,
    acreedor VARCHAR(20) NOT NULL,
    items TEXT,
    pago_inmediato BOOLEAN NOT NULL,
    cantidad_pagada FLOAT NOT NULL DEFAULT 0.00,
    total FLOAT,
    fecha TEXT NOT NULL
);

DROP TABLE IF EXISTS pago;

CREATE TABLE pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_origen INTEGER NOT NULL,
    origen VARCHAR(15) NOT NULL,
    cant_abono FLOAT NOT NULL,
    fecha TEXT NOT NULL
);