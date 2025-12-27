import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity, AlertCircle, CheckCircle, Zap } from "lucide-react";
import blockchainService, { NetworkMetrics, NodeHealth } from "@/services/blockchain.service";
import PerformanceChart from "@/components/charts/PerformanceChart";
import NodeHealth from "@/components/status/NodeHealth";
import NetworkLoad from "@/components/status/NetworkLoad";

export default function Dashboard() {
  const [networkMetrics, setNetworkMetrics] = useState<NetworkMetrics | null>(null);
  const [nodesHealth, setNodesHealth] = useState<NodeHealth[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [metrics, nodes] = await Promise.all([
          blockchainService.getNetworkMetrics(),
          blockchainService.getAllNodesHealth(),
        ]);
        setNetworkMetrics(metrics);
        setNodesHealth(nodes);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch data");
        console.error("Error fetching dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Subscribe to real-time updates
    const metricsWs = blockchainService.subscribeToNetworkMetrics((metrics) => {
      setNetworkMetrics(metrics);
    });

    return () => {
      if (metricsWs) metricsWs.close();
    };
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "bg-green-500";
      case "degraded":
        return "bg-yellow-500";
      case "offline":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  const healthyNodes = nodesHealth.filter((n) => n.status === "healthy").length;
  const degradedNodes = nodesHealth.filter((n) => n.status === "degraded").length;
  const offlineNodes = nodesHealth.filter((n) => n.status === "offline").length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Blockchain Dashboard</h1>
        <p className="text-gray-400 mt-2">Monitor network health and performance metrics in real-time</p>
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

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">Active Nodes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{networkMetrics?.activeNodes || 0}</div>
            <p className="text-xs text-gray-500 mt-1">of {networkMetrics?.totalNodes || 0} total</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">Avg Block Time</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{networkMetrics?.averageBlockTime.toFixed(2) || 0}s</div>
            <p className="text-xs text-gray-500 mt-1">milliseconds</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">Throughput</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{networkMetrics?.transactionThroughput.toFixed(0) || 0}</div>
            <p className="text-xs text-gray-500 mt-1">tx/sec</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">Network Load</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(networkMetrics?.networkLoad || 0).toFixed(1)}%</div>
            <p className="text-xs text-gray-500 mt-1">capacity used</p>
          </CardContent>
        </Card>
      </div>

      {/* Node Status Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Node Status Summary</CardTitle>
          <CardDescription>Current health status of all nodes in the network</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <div>
                <p className="text-sm text-gray-400">Healthy</p>
                <p className="text-2xl font-bold">{healthyNodes}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-yellow-500" />
              <div>
                <p className="text-sm text-gray-400">Degraded</p>
                <p className="text-2xl font-bold">{degradedNodes}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-red-500" />
              <div>
                <p className="text-sm text-gray-400">Offline</p>
                <p className="text-2xl font-bold">{offlineNodes}</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Charts and Components */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PerformanceChart />
        <NetworkLoad />
      </div>

      {/* Nodes List */}
      <div>
        <h2 className="text-xl font-bold mb-4">Node Details</h2>
        <div className="grid grid-cols-1 gap-4">
          {loading ? (
            <Card>
              <CardContent className="pt-6">
                <p className="text-gray-400">Loading node data...</p>
              </CardContent>
            </Card>
          ) : nodesHealth.length > 0 ? (
            nodesHealth.map((node) => (
              <NodeHealth key={node.id} node={node} />
            ))
          ) : (
            <Card>
              <CardContent className="pt-6">
                <p className="text-gray-400">No nodes available</p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
