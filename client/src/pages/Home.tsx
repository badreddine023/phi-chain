import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ChevronDown, Database, FileText, Globe, Layers, Package } from "lucide-react";
import { useState } from "react";

/**
 * Phi-Chain Repository Analysis Dashboard
 * Design Philosophy: Modern Technical Minimalism with Sophisticated Data Visualization
 * Color Scheme: Deep blues (#0f172a, #1e3a8a) with teals (#06b6d4) for accents
 * Typography: Geist Sans - clean, technical, professional
 */

export default function Home() {
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Navigation Header */}
      <header className="sticky top-0 z-50 border-b border-slate-800/50 bg-slate-950/80 backdrop-blur-md">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
              <Package className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-xl font-bold text-white">Phi-Chain Analysis</h1>
          </div>
          <nav className="hidden md:flex gap-6 text-sm">
            <a href="#structure" className="text-slate-300 hover:text-cyan-400 transition-colors">Structure</a>
            <a href="#documentation" className="text-slate-300 hover:text-cyan-400 transition-colors">Documentation</a>
            <a href="#web-assets" className="text-slate-300 hover:text-cyan-400 transition-colors">Web Assets</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-6 z-10">
              <div className="space-y-2">
                <h2 className="text-sm font-semibold text-cyan-400 uppercase tracking-widest">Repository Analysis</h2>
                <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight">
                  Phi-Chain
                  <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">Architecture</span>
                </h1>
              </div>
              <p className="text-lg text-slate-300 leading-relaxed max-w-lg">
                A comprehensive structural analysis and organizational review of the badreddine023/phi-chain blockchain repository, revealing its modular architecture and technical sophistication.
              </p>
              <div className="flex gap-4 pt-4">
                <Button className="bg-cyan-500 hover:bg-cyan-600 text-white px-8">Explore Analysis</Button>
                <Button variant="outline" className="border-slate-600 text-slate-300 hover:bg-slate-800">View Repository</Button>
              </div>
            </div>

            {/* Right Hero Image */}
            <div className="relative h-96 md:h-full min-h-96 rounded-xl overflow-hidden">
              <img
                src="/images/hero-blockchain.jpg"
                alt="Blockchain Network Visualization"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-l from-transparent via-transparent to-slate-950"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Repository Structure Overview */}
      <section id="structure" className="py-20 border-t border-slate-800/50">
        <div className="container mx-auto px-4">
          <div className="mb-12">
            <h2 className="text-4xl font-bold text-white mb-3">Repository Structure</h2>
            <p className="text-slate-400 text-lg">The phi-chain project is organized into distinct functional modules, each serving a specific purpose in the blockchain ecosystem.</p>
          </div>

          <Tabs defaultValue="core" className="w-full">
            <TabsList className="grid w-full grid-cols-3 md:grid-cols-5 bg-slate-800/50 border border-slate-700">
              <TabsTrigger value="core" className="text-xs md:text-sm">Core</TabsTrigger>
              <TabsTrigger value="consensus" className="text-xs md:text-sm">Consensus</TabsTrigger>
              <TabsTrigger value="network" className="text-xs md:text-sm">Network</TabsTrigger>
              <TabsTrigger value="crypto" className="text-xs md:text-sm">Crypto</TabsTrigger>
              <TabsTrigger value="storage" className="text-xs md:text-sm">Storage</TabsTrigger>
            </TabsList>

            <TabsContent value="core" className="mt-6 space-y-4">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-cyan-400">
                    <Layers className="w-5 h-5" />
                    Core Components
                  </CardTitle>
                  <CardDescription className="text-slate-400">Fundamental building blocks and business logic</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4 text-slate-300">
                  <p>The core directory contains the essential data structures and business logic of the blockchain, including block definitions, transaction processing, and state management.</p>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">phi_chain_core.py</p>
                      <p className="text-xs text-slate-400 mt-1">Main core logic</p>
                    </div>
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Block Management</p>
                      <p className="text-xs text-slate-400 mt-1">Block creation & validation</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="consensus" className="mt-6 space-y-4">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-cyan-400">
                    <Database className="w-5 h-5" />
                    Consensus Mechanism
                  </CardTitle>
                  <CardDescription className="text-slate-400">Network agreement and validation protocol</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4 text-slate-300">
                  <p>Implements the algorithm governing how nodes agree on the state of the ledger. This is a critical security component that ensures network integrity and prevents double-spending.</p>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Validator Nodes</p>
                      <p className="text-xs text-slate-400 mt-1">Network validators</p>
                    </div>
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Agreement Protocol</p>
                      <p className="text-xs text-slate-400 mt-1">Consensus rules</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="network" className="mt-6 space-y-4">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-cyan-400">
                    <Globe className="w-5 h-5" />
                    P2P Networking
                  </CardTitle>
                  <CardDescription className="text-slate-400">Peer discovery and communication</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4 text-slate-300">
                  <p>Manages node discovery, communication protocols, and transaction/block propagation across the network. Essential for maintaining network connectivity and data synchronization.</p>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Node Discovery</p>
                      <p className="text-xs text-slate-400 mt-1">Peer identification</p>
                    </div>
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Message Propagation</p>
                      <p className="text-xs text-slate-400 mt-1">Data distribution</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="crypto" className="mt-6 space-y-4">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-cyan-400">
                    <Package className="w-5 h-5" />
                    Cryptography
                  </CardTitle>
                  <CardDescription className="text-slate-400">Security primitives and key management</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4 text-slate-300">
                  <p>Provides secure functions for hashing, digital signatures, and key management. Essential for data integrity, user authentication, and transaction verification.</p>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Hashing</p>
                      <p className="text-xs text-slate-400 mt-1">Data integrity</p>
                    </div>
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Digital Signatures</p>
                      <p className="text-xs text-slate-400 mt-1">Authentication</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="storage" className="mt-6 space-y-4">
              <Card className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-cyan-400">
                    <Database className="w-5 h-5" />
                    Data Persistence
                  </CardTitle>
                  <CardDescription className="text-slate-400">Blockchain data storage layer</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4 text-slate-300">
                  <p>Handles the reading and writing of blockchain data (blocks, state database) to a persistent medium. Ensures data durability and efficient retrieval.</p>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">Block Storage</p>
                      <p className="text-xs text-slate-400 mt-1">Ledger persistence</p>
                    </div>
                    <div className="p-3 bg-slate-700/30 rounded-lg border border-slate-600">
                      <p className="text-sm font-semibold text-cyan-300">State Database</p>
                      <p className="text-xs text-slate-400 mt-1">Account state</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Documentation Section */}
      <section id="documentation" className="py-20 border-t border-slate-800/50 bg-slate-900/30">
        <div className="container mx-auto px-4">
          <div className="mb-12">
            <h2 className="text-4xl font-bold text-white mb-3">Documentation & Reports</h2>
            <p className="text-slate-400 text-lg">Comprehensive technical documentation grounding the project in theory and implementation details.</p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {[
              { title: "WHITEPAPER.md", desc: "Foundational document detailing vision, economic model, and high-level technology", icon: FileText },
              { title: "TECHNICAL_REPORT.md", desc: "Detailed explanation of system architecture, algorithms, and implementation specifics", icon: FileText },
              { title: "SYSTEM_OVERVIEW.md", desc: "Concise, high-level summary of entire system components and interactions", icon: Layers },
              { title: "MATH_OF_PHI.md", desc: "Explores mathematical principles (Golden Ratio, Fibonacci) informing the chain's design", icon: FileText },
            ].map((doc, idx) => {
              const IconComponent = doc.icon;
              return (
                <Card key={idx} className="bg-slate-800/50 border-slate-700 hover:border-cyan-500/50 transition-colors cursor-pointer">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-white">
                      <IconComponent className="w-5 h-5 text-cyan-400" />
                      {doc.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-400 text-sm">{doc.desc}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Web Assets Section */}
      <section id="web-assets" className="py-20 border-t border-slate-800/50">
        <div className="container mx-auto px-4">
          <div className="mb-12">
            <h2 className="text-4xl font-bold text-white mb-3">Web Interface & Visualization</h2>
            <p className="text-slate-400 text-lg">Suite of web-based tools for monitoring, simulation, and user interaction with the blockchain.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { name: "Dashboard", desc: "Real-time network statistics and node health monitoring", icon: Globe },
              { name: "Wallet Interface", desc: "Web-based key management and transaction signing", icon: Package },
              { name: "Consensus Monitor", desc: "Visual tracking of network consensus progress", icon: Database },
            ].map((asset, idx) => {
              const IconComponent = asset.icon;
              return (
                <Card key={idx} className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border-slate-700 hover:border-cyan-500/50 transition-colors">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-white">
                      <IconComponent className="w-5 h-5 text-cyan-400" />
                      {asset.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-400 text-sm">{asset.desc}</p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Organization Recommendations */}
      <section className="py-20 border-t border-slate-800/50 bg-slate-900/30">
        <div className="container mx-auto px-4">
          <div className="mb-12">
            <h2 className="text-4xl font-bold text-white mb-3">Proposed Organization</h2>
            <p className="text-slate-400 text-lg">Recommended restructuring to enhance clarity and maintainability.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { dir: "code/", items: ["core/", "consensus/", "network/", "crypto/", "tests/", "setup.py"], color: "from-blue-500" },
              { dir: "docs/", items: ["WHITEPAPER.md", "TECHNICAL_REPORT.md", "SYSTEM_OVERVIEW.md", "README.md"], color: "from-cyan-500" },
              { dir: "web/", items: ["index.html", "dashboard.html", "wallet.html", "js/", "styles.css"], color: "from-purple-500" },
            ].map((org, idx) => (
              <Card key={idx} className="bg-slate-800/50 border-slate-700">
                <CardHeader>
                  <CardTitle className={`text-white bg-gradient-to-r ${org.color} to-transparent bg-clip-text text-transparent`}>
                    {org.dir}
                  </CardTitle>
                  <CardDescription className="text-slate-400">Application logic and configuration</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {org.items.map((item, i) => (
                      <li key={i} className="text-slate-300 text-sm flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/50 py-12 bg-slate-950/50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-semibold text-white mb-4">Analysis</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><a href="#structure" className="hover:text-cyan-400 transition-colors">Repository Structure</a></li>
                <li><a href="#documentation" className="hover:text-cyan-400 transition-colors">Documentation</a></li>
                <li><a href="#web-assets" className="hover:text-cyan-400 transition-colors">Web Assets</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-4">Resources</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><a href="#" className="hover:text-cyan-400 transition-colors">GitHub Repository</a></li>
                <li><a href="#" className="hover:text-cyan-400 transition-colors">Technical Report</a></li>
                <li><a href="#" className="hover:text-cyan-400 transition-colors">Whitepaper</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-4">Project</h3>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><a href="#" className="hover:text-cyan-400 transition-colors">About Phi-Chain</a></li>
                <li><a href="#" className="hover:text-cyan-400 transition-colors">Contributing</a></li>
                <li><a href="#" className="hover:text-cyan-400 transition-colors">License</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-4">Analysis</h3>
              <p className="text-slate-400 text-sm">Comprehensive structural analysis of the phi-chain blockchain repository by Manus AI.</p>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-slate-500 text-sm">© 2025 Phi-Chain Repository Analysis. All rights reserved.</p>
            <p className="text-slate-500 text-sm mt-4 md:mt-0">Analyzed with Manus AI</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
