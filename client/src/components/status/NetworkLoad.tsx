import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import blockchainService from "@/services/blockchain.service";

export default function NetworkLoad() {
  const [networkLoad, setNetworkLoad] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const load = await blockchainService.getNetworkLoad();
        setNetworkLoad(load);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch network load");
        console.error("Error fetching network load:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const data = [
    { name: "Used", value: networkLoad },
    { name: "Available", value: 100 - networkLoad },
  ];

  const COLORS = ["#3b82f6", "#1f2937"];

  const getLoadStatus = (load: number) => {
    if (load < 30) return { status: "Low", color: "text-green-500" };
    if (load < 70) return { status: "Medium", color: "text-yellow-500" };
    return { status: "High", color: "text-red-500" };
  };

  const { status, color } = getLoadStatus(networkLoad);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Network Load</CardTitle>
        <CardDescription>Current network capacity utilization</CardDescription>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="h-80 flex items-center justify-center">
            <p className="text-gray-400">Loading network load data...</p>
          </div>
        ) : error ? (
          <div className="h-80 flex items-center justify-center">
            <p className="text-red-500">{error}</p>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Load Indicator */}
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 mb-2">Current Load</p>
                <div className="flex items-baseline gap-2">
                  <p className="text-4xl font-bold">{networkLoad.toFixed(1)}</p>
                  <p className="text-gray-400">%</p>
                </div>
                <p className={`text-sm font-semibold mt-2 ${color}`}>{status} Load</p>
              </div>

              {/* Pie Chart */}
              <ResponsiveContainer width="50%" height={200}>
                <PieChart>
                  <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1a1a1a",
                      border: "1px solid #333",
                      borderRadius: "8px",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Load Bar */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <p className="text-xs text-gray-400">Capacity Usage</p>
                <p className="text-xs font-semibold">{networkLoad.toFixed(1)}%</p>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-3">
                <div
                  className={`h-3 rounded-full transition-all duration-300 ${
                    networkLoad < 30
                      ? "bg-green-500"
                      : networkLoad < 70
                        ? "bg-yellow-500"
                        : "bg-red-500"
                  }`}
                  style={{ width: `${networkLoad}%` }}
                />
              </div>
            </div>

            {/* Status Info */}
            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-gray-700">
              <div>
                <p className="text-xs text-gray-400">Recommended Threshold</p>
                <p className="text-sm font-semibold">70%</p>
              </div>
              <div>
                <p className="text-xs text-gray-400">Available Capacity</p>
                <p className="text-sm font-semibold">{(100 - networkLoad).toFixed(1)}%</p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
