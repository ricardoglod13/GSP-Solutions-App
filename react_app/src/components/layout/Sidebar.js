import React from 'react'
import { Link } from 'react-router-dom';
import DropdownComponent from './Dropdown'

const Sidebar = () => {
    return(
        <aside className="sidebar col-3">
            <h2>Administración</h2>
            <nav className="navegacion">
                <Link to={"/"} className="home">Inicio</Link>
                <Link to={"/products"} className="productos">Productos</Link>
                <DropdownComponent dropdownName={{name:'Contactos', class:'contacts'}} rutas={[
                    {name:'clients', class:'clientes', label:'Clientes'},
                    {name:'providers', class:'proveedores', label:'Proveedores'},
                    {name:'companies', class:'companies', label:'Compañias'}
                    ]} />
                <DropdownComponent dropdownName={{name:'Transacciones', class:'transactions'}} rutas={[
                    {name:'sales', class:'pedidos', label:'Ventas'},
                    {name:'purchases', class:'pedidos', label:'Compras'}
                    ]} />
                <Link to={"/payments"} className="pagos">Pagos</Link>
            </nav>
        </aside>
    );
}

export default Sidebar;