import API_BASE_URL from "./api";

export type DashboardSummary = {
    total_income: number
    total_expenses: number
    balance: number
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
    const response = await fetch(`${API_BASE_URL}/transactions/summary`)

    if (!response.ok) {
        throw new Error("Failed to fetch dashboard summary")
    }

    return response.json()
}