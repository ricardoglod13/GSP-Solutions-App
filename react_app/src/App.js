import React, {Fragment} from 'react'
import {Routes, Route} from 'react-router-dom'

// Layout
import Header from './components/layout/Header'
import Sidebar from './components/layout/Sidebar'

// Components
import Home from './components/home/Home'
import Products from './components/products/Products'
import Clients from './components/clients/Clients'
import Providers from './components/providers/Providers'
import Companies from './components/companies/Companies'
import Employees from './components/employees/Employees'
import Sales from './components/sales/Sales'
import Purchases from './components/purchases/Purchases'
import Payments from './components/payments/Payments'

const App = () => {
  return (
      <Fragment>
        <Header />
        <div className="grid contenedor contenido-principal">
          <Sidebar />
          <main className="caja-contenido col-9">
            <Routes>
              <Route path='/' element={ <Home /> }/>
              <Route path='/products' element={ <Products /> }/>
              <Route path='/clients' element={ <Clients /> }/>
              <Route path='/providers' element={ <Providers /> }/>
              <Route path='/companies' element={ <Companies /> }/>
              <Route path='/employees' element={ <Employees /> }/>
              <Route path='/sales' element={ <Sales /> }/>
              <Route path='/purchases' element={ <Purchases /> }/>
              <Route path='/payments' element={ <Payments /> }/>
            </Routes>
          </main>
        </div>
      </Fragment>
  );
}

export default App;
