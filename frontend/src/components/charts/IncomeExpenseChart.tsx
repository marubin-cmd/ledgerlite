import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

import type { Transaction } from "../../services/transactionService"

type IncomeExpenseChartProps = {
    transactions: Transaction[]
}



function IncomeExpenseChart({ transactions }: IncomeExpenseChartProps) {

    const data = transactions.reduce((acc, transaction) => {
        const date = new Date(transaction.transaction_date)

        const month = date.toLocaleString("en-PH", {
            month: "short",
        })

        let monthData = acc.find(item => item.month === month)

        if (!monthData) {
            monthData = {
                month,
                income: 0,
                expenses: 0,
            }

            acc.push(monthData)
        }

        if (transaction.transaction_type === "income") {
            monthData.income += Number(transaction.amount)
        } else {
            monthData.expenses += Number(transaction.amount)
        }

        return acc
    }, [] as { month: string; income: number; expenses: number }[])

    data.reverse()

    return (
        <div>
        <ResponsiveContainer width="100%" height={320}>
            <BarChart
            data={data}
            margin={{ top: 10, right: 10, left: 10, bottom: 0 }}
            barGap={8}
            >
            <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
                stroke="#E5E1D7"
            />

            <XAxis
                dataKey="month"
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6B6B6B', fontSize: 12 }}
            />

            <YAxis
                axisLine={false}
                tickLine={false}
                tick={{ fill: '#6B6B6B', fontSize: 12 }}
                tickFormatter={(value) => {
                    if (value === 0) return '₱0'

                    return `₱${value / 1000}k`
                }}
            />

            <Tooltip
            contentStyle={{
                backgroundColor: '#FFFFFF',
                border: '1px solid #E5E1D7',
                borderRadius: '10px',
                padding: '12px 16px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
            }}
            labelStyle={{
                color: '#171717',
                fontWeight: 600,
                marginBottom: '6px',
            }}
            itemStyle={{
                fontSize: '15px',
            }}
            formatter={(value) =>
                `₱${Number(value).toLocaleString('en-PH', {
                minimumFractionDigits: 2,
                })}`
            }
            />

            <Legend
            verticalAlign="bottom"
            align="center"
            iconType="circle"
            iconSize={8}
            wrapperStyle={{
                paddingTop: '20px',
                fontSize: '15px',
                color: '#6B6B6B',
            }}
            />
            
            <Bar
                dataKey="expenses"
                name="Expenses"
                fill="#6B6B6B"
                radius={[5, 5, 0, 0]}
                maxBarSize={28}
            />

            <Bar
                dataKey="income"
                name="Income"
                fill="#D4AF37"
                radius={[5, 5, 0, 0]}
                maxBarSize={28}
            />


            </BarChart>
        </ResponsiveContainer>
        </div>
    )
}

export default IncomeExpenseChart