import API_BASE_URL from "./api";

export type Transaction = {
    id: number
    description: string
    amount: number
    transaction_type: "income" | "expense"   
    transaction_date: string
    created_at: string
    category_id: number | null
}

export async function getTransactions(): Promise<Transaction[]>{
    
    const response = await fetch(`${API_BASE_URL}/transactions?limit=5`)

    if (!response.ok) {
        throw new Error("Failed to fetch transactions")
    }

    return response.json()
}


export async function getChartTransactions(): Promise<Transaction[]> {
    const today = new Date()

    const startDate = new Date(
        today.getFullYear(),
        today.getMonth() - 5,
        1
    )

    const formatDate = (date: Date) => {
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, "0")
        const day = String(date.getDate()).padStart(2, "0")

        return `${year}-${month}-${day}`
    }

    const response = await fetch(
        `${API_BASE_URL}/transactions?start_date=${formatDate(startDate)}&end_date=${formatDate(today)}&limit=100`
    )

    if (!response.ok) {
        throw new Error("Failed to fetch chart transactions")
    }

    return response.json()
}