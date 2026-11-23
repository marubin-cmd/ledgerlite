import { NavLink } from "react-router";
import {
  LayoutDashboard,
  ArrowLeftRight,
  FileText,
  Users,
  Tags,
  Wallet,
} from 'lucide-react'

function Sidebar() {

    return (

        <aside>

            <h2>Ledgerlite</h2>

            <nav>
                <NavLink to="/" className={ ({ isActive }) => isActive ? 'active' : ''}>
                    <LayoutDashboard size={18} />  
                    Dashboard
                </NavLink>

                <NavLink to="/transactions" className={ ({ isActive }) => isActive ? 'active' : ''}>
                    <ArrowLeftRight size={18} />
                    Transactions
                </NavLink>

                <NavLink to="/invoices" className={ ({ isActive }) => isActive ? 'active' : ''}>
                    <FileText size={18} />
                    Invoices
                </NavLink>

                <NavLink to="/clients" className={ ({ isActive}) => isActive ? 'active' : ''}>
                    <Users size={18} />
                    Clients
                </NavLink>

                <NavLink to="/categories" className={ ({ isActive }) => isActive ? 'active' : ''}>
                    <Tags size={18} />
                    Categories
                </NavLink>

                <NavLink to="/payments" className={ ({ isActive }) => isActive ? 'active' : ''}>
                    <Wallet size={18} />
                    Payments
                </NavLink>
            </nav>

        </aside>
    )
}

export default Sidebar