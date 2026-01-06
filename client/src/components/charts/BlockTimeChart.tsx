import { useEffect, useState } from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import blockchainService, { PerformanceData } from "@/services/blockchain.service";

export default function BlockTimeChart() {
  const [data, setData] = useState<PerformanceData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const blockTimeHistory = await blockchainService.getBlockTimeHistory(100);
        setData(blockTimeHistory);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch block time history");
        console.error("Error fetching block time history:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Refresh every 10 minutes
    const interval = setInterval(fetchData, 10 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const chartData = data.map((item) => ({
    timestamp: new Date(item.timestamp).toLocaleTimeString(),
    blockTime: item.blockTime,
  }));

  const avgBlockTime = data.length > 0 ? (data.reduce((sum, item) => sum + item.blockTime, 0) / data.length).toFixed(2) : 0;
  const minBlockTime = data.length > 0 ? Math.min(...data.map((item) => item.blockTime)).toFixed(2) : 0;
  const maxBlockTime = data.length > 0 ? Math.max(...data.map((item) => item.blockTime)).toFixed(2) : 0;

  return (
    <div className="space-y-4">
      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-sm text-gray-400">Average Block Time</p>
          <p className="text-2xl font-bold text-blue-400">{avgBlockTime}ms</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-sm text-gray-400">Min Block Time</p>
          <p className="text-2xl font-bold text-green-400">{minBlockTime}ms</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-sm text-gray-400">Max Block Time</p>
          <p className="text-2xl font-bold text-red-400">{maxBlockTime}ms</p>
        </div>
      </div>

      {/* Chart */}
      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <p className="text-gray-400">Loading block time data...</p>
        </div>
      ) : error ? (
        <div className="h-64 flex items-center justify-center">
          <p className="text-red-500">{error}</p>
        </div>
      ) : chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorBlockTime" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
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
            <Area
              type="monotone"
              dataKey="blockTime"
              stroke="#3b82f6"
              fillOpacity={1}
              fill="url(#colorBlockTime)"
              name="Block Time (ms)"
            />
          </AreaChart>
        </ResponsiveContainer>
      ) : (
        <div className="h-64 flex items-center justify-center">
          <p className="text-gray-400">No block time data available</p>
        </div>
      )}
    </div>
  );
}
