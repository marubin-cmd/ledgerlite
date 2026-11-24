import { Search, Bell } from 'lucide-react'
import { useLocation } from 'react-router'

function Header() {

    const location = useLocation()

    const pageInfo: Record<string, { title: string, description: string }> = {

        "/": 
        {
            title: "Dashboard",
            description: "Here's what's happening with your finances"
        },

        "/transactions":
        {
            title: "Transactions",
            description: "Track and manage your financial transactions."
        },

        "/invoices":
        {
            title: "Invoices",
            description: "Manage your invoices and billing."
        },

        "/clients":
        {
            title: "Clients",
            description: "Manage your client relationships."
        },

        "/categories":
        {
            title: "Categories",
            description: "Organize your income and expenses."
        },

        "/payments":
        {
            title: "Payments",
            description: "Track and manage invoice payments."
        }

    }

    const currentPage = pageInfo[location.pathname] ?? pageInfo['/']


    return(

        <header className="app-header">

            <div className="header-title">
                <h1>{currentPage.title}</h1>
                <p>{currentPage.description}</p>
            </div>

            <div className="header-actions">
                <div className="search-box">
                    <Search size={18} />
                    <input type="text" placeholder="Search..."></input>
                </div>

                <button className="notification-button" type="button">
                    Notifications <Bell size={20} />
                </button>

            </div>

            <div className="user-avatar">
                <span>MC</span>
            </div>

        </header>
    )

}

export default Header