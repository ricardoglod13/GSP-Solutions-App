import React from 'react';

const Product = ({product}) => {

    const {id, codigo, tipo, descripcion, precio_costo, precio_venta, cantidad} = product

    return ( 
        <ul class="listado-clientes">
            <li class="cliente">
                <div class="info-cliente">
                    <p class="nombre">{codigo}</p>
                    <p class="empresa">{descripcion}</p>
                    <p>Tipo: {tipo}</p>
                    <p>Costo: {precio_costo}</p>
                    <p>Precio de Venta: {precio_venta}</p>
                    <p>Cantidad: {cantidad}</p>
                </div>
                <div class="acciones">
                    <a href="#" class="btn btn-azul">
                        <i class="fas fa-pen-alt"></i>
                        Editar Cliente
                    </a>
                    <button type="button" class="btn btn-rojo btn-eliminar">
                        <i class="fas fa-times"></i>
                        Eliminar Cliente
                    </button>
                </div>
            </li>
        </ul> 
    );
}
 
export default Product;