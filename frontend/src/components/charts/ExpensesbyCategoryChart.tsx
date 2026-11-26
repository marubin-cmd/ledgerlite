import {
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Sector,
  ResponsiveContainer,
  LabelList
} from 'recharts'

import type { Category } from '../../services/categoryService'
import type { Transaction } from '../../services/transactionService'


type ExpensesByCategoryChartProps = {
    transactions: Transaction[]
    categories: Category[]
}


function ExpensesByCategoryChart({ transactions, categories }: ExpensesByCategoryChartProps) {

    const colors = [
        '#D4AF37',
        '#6B6B6B',
        '#A68A3D',
        '#9B9B9B',
        '#D8CBA5',
    ]

    const data = categories
        .filter(category => category.category_type === "expense")
        .map((category, index) => {
            const amount = transactions
                .filter(transaction =>
                    transaction.category_id === category.id &&
                    transaction.transaction_type === "expense"
                )
                .reduce(
                    (total, transaction) => total + Number(transaction.amount),
                    0
                )

            return {
                category: category.name,
                amount,
                fill: colors[index % colors.length],
            }
        })
        .filter(category => category.amount > 0)

    const uncategorizedAmount = transactions
    .filter(transaction =>
        transaction.transaction_type === "expense" &&
        transaction.category_id === null
    )
    .reduce(
        (total, transaction) => total + Number(transaction.amount),
        0
    )

    if (uncategorizedAmount > 0) {
        data.push({
            category: "Uncategorized",
            amount: uncategorizedAmount,
            fill: "#D8CBA5",
        })
    }

    const totalExpenses = data.reduce(
        (total, item) => total + item.amount,
        0
    )

    const chartData = data.map((item) => ({
        ...item,
        percentage: totalExpenses > 0
            ? `${((item.amount / totalExpenses) * 100).toFixed(0)}%`
            : "0%",
    }))
  


  return (
    <div className="donut-chart-container">
        <ResponsiveContainer width="100%" height={320}>

            <PieChart>
            <Pie
                data={chartData}
                dataKey="amount"
                nameKey="category"
                cx="50%"
                cy="50%"
                innerRadius={75}
                outerRadius={110}
                paddingAngle={3}
                labelLine={false}
                label={({ percent }: { percent?: number }) =>
                    `${((percent ?? 0) * 100).toFixed(0)}%`
                }
                

                shape={(props) => (
                    <Sector
                        {...props}
                        fill={props.payload.fill}
                    />
                )}


            />

            <LabelList
                dataKey="percentage"
                position="inside"
                fill="#FFFFFF"
                fontSize={12}
                fontWeight={600}
            />

            <Tooltip
                wrapperStyle={{ zIndex: 100 }}
                contentStyle={{
                    backgroundColor: '#FFFFFF',
                    border: '1px solid #E5E1D7',
                    borderRadius: '8px',
                    padding: '10px 14px',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
                }}
                labelStyle={{
                    color: '#171717',
                    fontWeight: 600,
                    marginBottom: '4px',
                }}
                itemStyle={{
                    color: '#6B6B6B',
                    fontSize: '13px',
                }}
                formatter={(value, name) => {
                    const amount = Number(value)
                    const percentage = (amount / totalExpenses) * 100

                    return [
                    `₱${amount.toLocaleString('en-PH', {
                        minimumFractionDigits: 2,
                    })} (${percentage.toFixed(1)}%)`,
                     name,
                    ]
                }}
            />

            <Legend
                iconType="circle"
                iconSize={8}
                wrapperStyle={{
                paddingTop: '20px',
                fontSize: '13px',
                color: '#6B6B6B',
                }}
            />
            </PieChart>
        </ResponsiveContainer>

        <div className="donut-chart-center">
            <span>Total Expenses</span>
            <strong>
                ₱{totalExpenses.toLocaleString('en-PH', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                })}
            </strong>
            <small>
                Across {data.length} categories
            </small>
        </div>

    </div>
  )
}

export default ExpensesByCategoryChart