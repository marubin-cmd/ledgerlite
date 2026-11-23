import { Outlet } from "react-router";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";


function MainLayout() {

    return (

        <div className="app-layout">
            <Sidebar />

            <div className="main-area">
            
                <Header />
                
                <main>
                    <Outlet />
                </main>
            </div>
        </div>

    )
}

export default MainLayout