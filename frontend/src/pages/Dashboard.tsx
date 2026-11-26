import { NavLink } from "react-router"
import { useEffect, useState } from "react"

import { getCategories, type Category } from "../services/categoryService"
import { getDashboardSummary, type DashboardSummary } from "../services/dashboardService"
import { getDashboardInvoices, type DashboardInvoice } from "../services/invoiceService"
import {
    getTransactions,
    getChartTransactions,
    type Transaction
} from "../services/transactionService"

import IncomeExpenseChart from "../components/charts/IncomeExpenseChart"
import ExpensesByCategoryChart from "../components/charts/ExpensesbyCategoryChart"

function Dashboard() {

    const [summary, setSummary] = useState<DashboardSummary | null>(null)
    const [invoices, setInvoices] = useState<DashboardInvoice[]>([]) 
    const [transactions, setTransactions] = useState<Transaction[]>([])
    const [chartTransactions, setChartTransactions] = useState<Transaction[]>([])
    const [categories, setCategories] = useState<Category[]>([])

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const outstandingBalance = invoices.filter(invoice =>
        ["unpaid", "partially_paid", "overdue"].includes(invoice.status))
        .reduce((total, invoice) => total + Number(invoice.balance), 0)
    

    useEffect(() => {
        async function fetchSummary() {
            try {
                const summaryData = await getDashboardSummary()
                setSummary(summaryData)

                const invoiceData = await getDashboardInvoices()
                setInvoices(invoiceData)

                const transactionData = await getTransactions()
                setTransactions(transactionData)

                const chartTransactionData = await getChartTransactions()
                setChartTransactions(chartTransactionData)

                const categoryData = await getCategories()
                setCategories(categoryData)

            } catch (err) {
                setError("Unable to load dashboard data.")
                console.error(err)
            } finally {
                setLoading(false)
            }
        }

        fetchSummary()
    }, [])

    if (loading) {
        return <p>Loading dashboard...</p>
    }

    if (error) {
        return <p>{error}</p>
    }

    return(
        <div className="dashboard">

            <div className="summary-cards">

                <div className="summary-card">
                    <p>Total Income</p>
                    <h2>
                        ₱{summary?.total_income.toLocaleString("en-PH", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        })}
                    </h2>
                </div>

                <div className="summary-card">
                    <p>Total Expense</p>
                    <h2>
                        ₱{summary?.total_expenses.toLocaleString("en-PH", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        })}
                    </h2>
                </div>

                <div className="summary-card">
                    <p>Balance</p>
                    <h2>
                        ₱{summary?.balance.toLocaleString("en-PH", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        })}
                    </h2>
                </div>

                <div className="summary-card">
                    <p>Outstanding Invoices</p>
                        <h2>
                            ₱{outstandingBalance.toLocaleString("en-PH", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            })}
                        </h2>
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
                                {transactions.map((transaction) => (

                                    <tr key={transaction.id}>

                                        <td>{transaction.description}</td>

                                        <td>{transaction.category_id ?? "--"}</td>

                                        <td>
                                            {new Date(transaction.transaction_date).toLocaleDateString("en-PH", {
                                                month: "short",
                                                day: "numeric",
                                                year: "numeric"
                                            })}
                                        </td>

                                        <td>
                                            <span className={`transaction-type ${transaction.transaction_type}`}>
                                                {transaction.transaction_type === "income" ? "Income" : "Expense"}
                                            </span>
                                            
                                        </td>

                                        <td>
                                            {transaction.transaction_type === "income" ? "+" : "-"}
                                            ₱{Number(transaction.amount).toLocaleString("en-PH", {
                                                minimumFractionDigits: 2,
                                                maximumFractionDigits: 2
                                            })}
                                        </td>

                                    </tr>

                                )
                            
                            
                            )}

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
                        <IncomeExpenseChart transactions={chartTransactions} />
                    </div>

                    <div className="chart-card">
                        <ExpensesByCategoryChart transactions={chartTransactions} categories={categories}/>
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
                                {invoices.map((invoice) => (
                                    <tr key={invoice.id}>

                                        <td>{invoice.invoice_number}</td>
                                        <td>{invoice.client_name}</td>

                                        <td>
                                            {new Date(invoice.issue_date).toLocaleDateString("en-PH", {
                                                month: "short",
                                                day: "numeric",
                                                year: "numeric"
                                            })}
                                        </td>

                                        <td>
                                            {new Date(invoice.due_date).toLocaleDateString("en-PH", {
                                                month: "short",
                                                day: "numeric",
                                                year: "numeric"
                                            })}
                                        </td>

                                        <td>
                                            ₱{Number(invoice.total).toLocaleString("en-PH", {
                                                maximumFractionDigits: 2,
                                                minimumFractionDigits: 2
                                            })}
                                        </td>

                                        <td>
                                            <span className={`invoice-status ${invoice.status}`}>
                                                {invoice.status.replace("_", " ")}
                                            </span>
                                        </td>


                                    </tr>
                                
                                )
                                
                            
                            )}

                            </tbody>

                        </table>

                    </div>
                
                </div>

            </div>

        </div>
    )
}   

export default Dashboard





