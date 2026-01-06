import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, AlertCircle, Clock } from "lucide-react";
import { NodeHealth as NodeHealthType } from "@/services/blockchain.service";

interface NodeHealthProps {
  node: NodeHealthType;
}

export default function NodeHealth({ node }: NodeHealthProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "bg-green-500/20 border-green-500";
      case "degraded":
        return "bg-yellow-500/20 border-yellow-500";
      case "offline":
        return "bg-red-500/20 border-red-500";
      default:
        return "bg-gray-500/20 border-gray-500";
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
    <Card className={`border-2 ${getStatusColor(node.status)}`}>
      <CardContent className="pt-6">
        <div className="space-y-4">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              {getStatusIcon(node.status)}
              <div>
                <p className="font-mono text-sm text-gray-400">Node ID</p>
                <p className="font-mono font-semibold">{node.id.substring(0, 16)}...</p>
              </div>
            </div>
            {getStatusBadge(node.status)}
          </div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-gray-400 mb-1">Uptime</p>
              <p className="font-semibold">{formatUptime(node.uptime)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 mb-1">Block Height</p>
              <p className="font-semibold">{node.blockHeight.toLocaleString()}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 mb-1">Sync Status</p>
              <p className="font-semibold">{formatSyncStatus(node.syncStatus)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 mb-1">Peers Connected</p>
              <p className="font-semibold">{node.peers}</p>
            </div>
          </div>

          {/* Sync Progress Bar */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <p className="text-xs text-gray-400">Synchronization Progress</p>
              <p className="text-xs font-semibold">{formatSyncStatus(node.syncStatus)}</p>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${node.syncStatus * 100}%` }}
              />
            </div>
          </div>

          {/* Last Update */}
          <div className="flex justify-between items-center text-xs text-gray-500">
            <span>Last updated</span>
            <span>{new Date(node.lastUpdate).toLocaleTimeString()}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
