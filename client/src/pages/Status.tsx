import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, CheckCircle, Clock, TrendingUp } from "lucide-react";
import blockchainService, { NodeHealth } from "@/services/blockchain.service";
import BlockTimeChart from "@/components/charts/BlockTimeChart";

export default function Status() {
  const [nodesHealth, setNodesHealth] = useState<NodeHealth[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const nodes = await blockchainService.getAllNodesHealth();
        setNodesHealth(nodes);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch status data");
        console.error("Error fetching status data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "healthy":
        return <Badge className="bg-green-500">Healthy</Badge>;
      case "degraded":
        return <Badge className="bg-yellow-500">Degraded</Badge>;
      case "offline":
        return <Badge className="bg-red-500">Offline</Badge>;
      default:
        return <Badge>Unknown</Badge>;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "healthy":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "degraded":
        return <AlertCircle className="h-5 w-5 text-yellow-500" />;
      case "offline":
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const formatUptime = (uptime: number) => {
    const days = Math.floor(uptime / (24 * 60 * 60));
    const hours = Math.floor((uptime % (24 * 60 * 60)) / (60 * 60));
    const minutes = Math.floor((uptime % (60 * 60)) / 60);
    return `${days}d ${hours}h ${minutes}m`;
  };

  const formatSyncStatus = (syncStatus: number) => {
    return `${(syncStatus * 100).toFixed(2)}%`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Network Status</h1>
        <p className="text-gray-400 mt-2">Detailed status and health information for all nodes</p>
      </div>

      {/* Error Alert */}
      {error && (
        <Card className="border-red-500 bg-red-500/10">
          <CardContent className="pt-6 flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-red-500" />
            <span className="text-red-500">{error}</span>
          </CardContent>
        </Card>
      )}

      {/* Block Time Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Block Time Trends</CardTitle>
          <CardDescription>Historical block time data</CardDescription>
        </CardHeader>
        <CardContent>
          <BlockTimeChart />
        </CardContent>
      </Card>

      {/* Nodes Status Table */}
      <Card>
        <CardHeader>
          <CardTitle>Node Status Details</CardTitle>
          <CardDescription>Real-time information about each node in the network</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8">
              <p className="text-gray-400">Loading node status...</p>
            </div>
          ) : nodesHealth.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Node ID</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Status</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Uptime</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Block Height</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Sync Status</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Peers</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-300">Last Update</th>
                  </tr>
                </thead>
                <tbody>
                  {nodesHealth.map((node) => (
                    <tr key={node.id} className="border-b border-gray-700 hover:bg-gray-800/50">
                      <td className="py-3 px-4">
                        <code className="text-xs bg-gray-800 px-2 py-1 rounded">
                          {node.id.substring(0, 8)}...
                        </code>
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          {getStatusIcon(node.status)}
                          {getStatusBadge(node.status)}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-300">{formatUptime(node.uptime)}</td>
                      <td className="py-3 px-4 text-gray-300">{node.blockHeight}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-700 rounded-full h-2">
                            <div
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${node.syncStatus * 100}%` }}
                            />
                          </div>
                          <span className="text-xs text-gray-400">{formatSyncStatus(node.syncStatus)}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-300">{node.peers}</td>
                      <td className="py-3 px-4 text-gray-400 text-xs">
                        {new Date(node.lastUpdate).toLocaleTimeString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-400">No nodes available</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
