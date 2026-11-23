import { Routes, Route } from "react-router"
import Dashboard from "./pages/Dashboard"
import Transactions from "./pages/Transactions"
import Clients from "./pages/Clients"
import Categories from "./pages/Categories"
import Payments from "./pages/Payments"
import Invoices from "./pages/Invoices"
import MainLayout from "./layouts/MainLayout"
import './App.css'


function App() {

  return (

    <Routes>

      <Route element={<MainLayout />}>

        <Route path="/" element={<Dashboard />} />
        <Route path="/transactions" element={<Transactions />} />
        <Route path="/invoices" element={<Invoices />} />
        <Route path="/clients" element={<Clients />} />
        <Route path="/categories" element={<Categories />} />
        <Route path="/payments" element={<Payments />} />

      </Route>

    </Routes>


  ) 
}

export default App
