import { NavLink } from "react-router";
import {
  LayoutDashboard,
  ArrowLeftRight,
  FileText,
  Users,
  Tags,
  Wallet,
} from 'lucide-react'

type SidebarProps = {
    isOpen: boolean
    onClose: () => void
}

function Sidebar({ isOpen, onClose} : SidebarProps) {

    return (

        <>
            {isOpen && (
                <button
                    className="sidebar-backdrop"
                    onClick={onClose}
                    aria-label="Close navigation menu"
                />
            )}
        

            <aside className={`sidebar ${isOpen ? "open" : ""}`}>

                <h2>Ledgerlite</h2>

                <nav>
                    <NavLink to="/" onClick={onClose} className={ ({ isActive }) => isActive ? 'active' : ''}>
                        <LayoutDashboard size={18} />  
                        Dashboard
                    </NavLink>

                    <NavLink to="/transactions" onClick={onClose} className={ ({ isActive }) => isActive ? 'active' : ''}>
                        <ArrowLeftRight size={18} />
                        Transactions
                    </NavLink>

                    <NavLink to="/invoices" onClick={onClose} className={ ({ isActive }) => isActive ? 'active' : ''}>
                        <FileText size={18} />
                        Invoices
                    </NavLink>

                    <NavLink to="/clients" onClick={onClose} className={ ({ isActive}) => isActive ? 'active' : ''}>
                        <Users size={18} />
                        Clients
                    </NavLink>

                    <NavLink to="/categories" onClick={onClose} className={ ({ isActive }) => isActive ? 'active' : ''}>
                        <Tags size={18} />
                        Categories
                    </NavLink>

                    <NavLink to="/payments" onClick={onClose} className={ ({ isActive }) => isActive ? 'active' : ''}>
                        <Wallet size={18} />
                        Payments
                    </NavLink>
                </nav>

            </aside>
        </>
    )
}

export default Sidebar