import API_BASE_URL from "./api";

export type Invoice = {
    id: number
    client_id: number
    invoice_number: string

    type: "income" | "expense"

    issue_date: string
    due_date: string
    status: 
        | "draft"
        | "unpaid"
        | "partially_paid"
        | "paid"
        | "overdue"
        | "cancelled"

    total: number
    amount_paid: number
    balance: number
}

export type DashboardInvoice = {
    id: number
    client_id: number
    client_name: string
    invoice_number: string

    type: "income" | "expense"

    issue_date: string
    due_date: string
    status: 
        | "draft"
        | "unpaid"
        | "partially_paid"
        | "paid"
        | "overdue"
        | "cancelled"

    total: number
    amount_paid: number
    balance: number
}


export async function getInvoices(): Promise<Invoice[]> {

    const response = await fetch(`${API_BASE_URL}/invoices`)

    if (!response.ok) {
        throw new Error("Failed to fetch invoices")
    }

    return response.json()
}

export async function getDashboardInvoices(): Promise<DashboardInvoice[]> {

    const response = await fetch(`${API_BASE_URL}/invoices/dashboard`)

    if (!response.ok) {
        throw new Error("Failed to fetch dashboard invoices")
    }

    return response.json()
}



