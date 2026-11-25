import { Outlet } from "react-router";
import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";


function MainLayout() {

    const [isSidebarOpen, setIsSidebarOpen] = useState(false)

    return (

        <div className="app-layout">
            <Sidebar
                isOpen={isSidebarOpen}
                onClose={() => setIsSidebarOpen(false)}

            />

            <div className="main-area">
            
                <Header onMenuClick={() => setIsSidebarOpen(true)} />
                
                <main>
                    <Outlet />
                </main>
            </div>
        </div>

    )
}

export default MainLayout