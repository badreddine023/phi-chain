/**
 * Blockchain Service
 * Handles all blockchain-related operations including node health, network status, and performance metrics
 */

export interface NodeHealth {
  id: string;
  status: "healthy" | "degraded" | "offline";
  uptime: number;
  blockHeight: number;
  syncStatus: number;
  peers: number;
  lastUpdate: Date;
}

export interface NetworkMetrics {
  totalNodes: number;
  activeNodes: number;
  averageBlockTime: number;
  transactionThroughput: number;
  networkLoad: number;
  timestamp: Date;
}

export interface PerformanceData {
  timestamp: Date;
  blockTime: number;
  gasUsed: number;
  transactions: number;
  validatorCount: number;
}

class BlockchainService {
  private baseUrl: string;

  constructor(baseUrl: string = "/api") {
    this.baseUrl = baseUrl;
  }

  /**
   * Fetch health status of a specific node
   */
  async getNodeHealth(nodeId: string): Promise<NodeHealth> {
    try {
      const response = await fetch(`${this.baseUrl}/nodes/${nodeId}/health`);
      if (!response.ok) throw new Error("Failed to fetch node health");
      return await response.json();
    } catch (error) {
      console.error("Error fetching node health:", error);
      throw error;
    }
  }

  /**
   * Fetch health status of all nodes
   */
  async getAllNodesHealth(): Promise<NodeHealth[]> {
    try {
      const response = await fetch(`${this.baseUrl}/nodes/health`);
      if (!response.ok) throw new Error("Failed to fetch nodes health");
      return await response.json();
    } catch (error) {
      console.error("Error fetching all nodes health:", error);
      throw error;
    }
  }

  /**
   * Fetch current network metrics
   */
  async getNetworkMetrics(): Promise<NetworkMetrics> {
    try {
      const response = await fetch(`${this.baseUrl}/network/metrics`);
      if (!response.ok) throw new Error("Failed to fetch network metrics");
      return await response.json();
    } catch (error) {
      console.error("Error fetching network metrics:", error);
      throw error;
    }
  }

  /**
   * Fetch performance data for a specific time range
   */
  async getPerformanceData(
    startTime: Date,
    endTime: Date
  ): Promise<PerformanceData[]> {
    try {
      const params = new URLSearchParams({
        startTime: startTime.toISOString(),
        endTime: endTime.toISOString(),
      });
      const response = await fetch(
        `${this.baseUrl}/performance?${params.toString()}`
      );
      if (!response.ok) throw new Error("Failed to fetch performance data");
      return await response.json();
    } catch (error) {
      console.error("Error fetching performance data:", error);
      throw error;
    }
  }

  /**
   * Fetch block time history
   */
  async getBlockTimeHistory(limit: number = 100): Promise<PerformanceData[]> {
    try {
      const response = await fetch(
        `${this.baseUrl}/blocks/time-history?limit=${limit}`
      );
      if (!response.ok) throw new Error("Failed to fetch block time history");
      return await response.json();
    } catch (error) {
      console.error("Error fetching block time history:", error);
      throw error;
    }
  }

  /**
   * Fetch network load data
   */
  async getNetworkLoad(): Promise<number> {
    try {
      const response = await fetch(`${this.baseUrl}/network/load`);
      if (!response.ok) throw new Error("Failed to fetch network load");
      const data = await response.json();
      return data.load;
    } catch (error) {
      console.error("Error fetching network load:", error);
      throw error;
    }
  }

  /**
   * Subscribe to real-time node health updates using WebSocket
   */
  subscribeToNodeHealth(
    nodeId: string,
    callback: (health: NodeHealth) => void
  ): WebSocket | null {
    try {
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const ws = new WebSocket(
        `${protocol}//${window.location.host}/api/nodes/${nodeId}/health/stream`
      );

      ws.onmessage = (event) => {
        const health = JSON.parse(event.data);
        callback(health);
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      return ws;
    } catch (error) {
      console.error("Error subscribing to node health:", error);
      return null;
    }
  }

  /**
   * Subscribe to real-time network metrics updates using WebSocket
   */
  subscribeToNetworkMetrics(
    callback: (metrics: NetworkMetrics) => void
  ): WebSocket | null {
    try {
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const ws = new WebSocket(
        `${protocol}//${window.location.host}/api/network/metrics/stream`
      );

      ws.onmessage = (event) => {
        const metrics = JSON.parse(event.data);
        callback(metrics);
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      return ws;
    } catch (error) {
      console.error("Error subscribing to network metrics:", error);
      return null;
    }
  }
}

export default new BlockchainService();
