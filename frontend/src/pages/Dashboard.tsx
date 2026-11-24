import { NavLink } from "react-router"
import IncomeExpenseChart from "../components/charts/IncomeExpenseChart"
import ExpensesByCategoryChart from "../components/charts/ExpensesbyCategoryChart"

function Dashboard() {
    return(
        <div className="dashboard">
            
            {/* <div className="dashboard-heading">
                <h1>Dashboard</h1>
                <p>Welcome to ledgerlite</p>
            </div> */}

            <div className="summary-cards">

                <div className="summary-card">
                    <p>Total Income</p>
                    <h2>₱0.00</h2>
                </div>

                <div className="summary-card">
                    <p>Total Expense</p>
                    <h2>₱0.00</h2>
                </div>

                <div className="summary-card">
                    <p>Balance</p>
                    <h2>₱0.00</h2>
                </div>

                <div className="summary-card">
                    <p>Outstanding Invoices</p>
                    <h2>₱0.00</h2>
                </div>

            </div>

            <div className="recent-transactions">

                <div className="section-heading">
                    <h2>Recent Transactions</h2>
                    <p>Your latest financial activities.</p>
                </div>

                <div>
                    <NavLink to="/transactions" className="view-all-link">
                        View all
                    </NavLink>
                </div>

                <div className="transactions-placeholder">
                    <div className="transactions-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Description</th>
                                    <th>Category</th>
                                    <th>Date</th>
                                    <th>Type</th>
                                    <th>Amount</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr>
                                    <td>Groceries</td>
                                    <td>Food</td>
                                    <td>Nov 24, 2026</td>
                                    <td><span className="transaction-type expense">Expense</span></td>
                                    <td>₱1,500.00</td>
                                </tr>

                                <tr>
                                    <td>Monthly Salary</td>
                                    <td>Salary</td>
                                    <td>Nov 23, 2026</td>
                                    <td><span className="transaction-type income">Income</span></td>
                                    <td>₱25,000.00</td>
                                </tr>

                            </tbody>
                        </table>
                    </div>
                </div>

            </div>


            <div className="financial-overview">

                <div className="section-heading">
                    <h2>Financial Overview</h2>
                    <p>Compare your income and expenses.</p>
                </div>

                <div className="charts-grid">
                    <div className="chart-card">
                        <IncomeExpenseChart />
                    </div>

                    <div className="chart-card">
                        <ExpensesByCategoryChart />
                    </div>
                    
                </div>

            </div>

            
            <div className="recent-invoices">

                <div className="section-heading">
                    <h2>Recent Invoices</h2>
                    <p>Your latest invoices and payment status.</p>
                </div>

                <div>
                    <NavLink to="/invoices" className="view-all-link">
                        View all
                    </NavLink>
                </div>

                <div className="invoices-placeholder">
                    
                    <div className="invoices-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Invoice</th>
                                    <th>Client</th>
                                    <th>Issue Date</th>
                                    <th>Due Date</th>
                                    <th>Amount</th>
                                    <th>Status</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr>
                                    <td>INV-0001</td>
                                    <td>John Doe</td>
                                    <td>Nov 20, 2026</td>
                                    <td>Nov 30, 2026</td>
                                    <td>₱15,000.00</td>
                                    <td>
                                        <span className="invoice-status paid">Paid</span>
                                    </td>
                                </tr>

                                <tr>
                                    <td>INV-0002</td>
                                    <td>Jane Smith</td>
                                    <td>Nov 12, 2026</td>
                                    <td>Dec 02, 2026</td>
                                    <td>₱8,500.00</td>
                                    <td>
                                        <span className="invoice-status unpaid">Unpaid</span>
                                    </td>
                                </tr>
                            </tbody>

                        </table>

                    </div>
                
                </div>

            </div>

        </div>
    )
}   

export default Dashboard





