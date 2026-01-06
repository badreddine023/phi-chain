import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import blockchainService, { PerformanceData } from "@/services/blockchain.service";

export default function PerformanceChart() {
  const [data, setData] = useState<PerformanceData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const endTime = new Date();
        const startTime = new Date(endTime.getTime() - 60 * 60 * 1000); // Last hour
        const performanceData = await blockchainService.getPerformanceData(startTime, endTime);
        setData(performanceData);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch performance data");
        console.error("Error fetching performance data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Refresh every 5 minutes
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const chartData = data.map((item) => ({
    timestamp: new Date(item.timestamp).toLocaleTimeString(),
    blockTime: item.blockTime,
    gasUsed: item.gasUsed / 1000000, // Convert to millions
    transactions: item.transactions,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Performance Metrics</CardTitle>
        <CardDescription>Last 60 minutes of network performance data</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="h-80 flex items-center justify-center">
            <p className="text-gray-400">Loading performance data...</p>
          </div>
        ) : error ? (
          <div className="h-80 flex items-center justify-center">
            <p className="text-red-500">{error}</p>
          </div>
        ) : chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="timestamp" stroke="#666" />
              <YAxis stroke="#666" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1a1a1a",
                  border: "1px solid #333",
                  borderRadius: "8px",
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="blockTime"
                stroke="#3b82f6"
                dot={false}
                name="Block Time (ms)"
              />
              <Line
                type="monotone"
                dataKey="gasUsed"
                stroke="#10b981"
                dot={false}
                name="Gas Used (M)"
              />
              <Line
                type="monotone"
                dataKey="transactions"
                stroke="#f59e0b"
                dot={false}
                name="Transactions"
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-80 flex items-center justify-center">
            <p className="text-gray-400">No performance data available</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
