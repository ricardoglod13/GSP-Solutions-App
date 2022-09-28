import React, { useEffect, useState, Fragment } from 'react';
import clientAxios from '../../config/axios'
import Product from './Product'

const Products = () => {

    const [productState, setProducts] = useState([])

    const dataAPI = async () => {
        const productsData = await clientAxios.get('/products');

        setProducts(productsData.data)
    }

    useEffect(() => {
        dataAPI()
    }, [])

    return (
        <Fragment>
            <h1>Productos</h1>
            <ul className='listado-clientes'>
                {productState.map(product => (
                    <Product 
                        product={product}
                    />
                ))}
            </ul>
        </Fragment>
    );
}
 
export default Products;