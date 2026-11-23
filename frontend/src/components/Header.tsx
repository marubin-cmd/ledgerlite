import { Search, Bell } from 'lucide-react'

function Header() {

    return(

        <header className="app-header">

            <div className="header-title">
                <h1>Dashboard</h1>
                <p>Here's whats happening with your finances.</p>
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