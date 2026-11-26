import API_BASE_URL from "./api";


export type Category = {
    id: number
    name: string
    description: string | null
    category_type: "income" | "expense"
}

export async function getCategories(): Promise<Category[]> {

    const response = await fetch(`${API_BASE_URL}/categories`)

    if (!response.ok) {
        throw new Error("Failed to fetch categories")
    }

    return response.json()

}