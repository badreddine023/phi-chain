/**
 * AI Oracle Module for Φ-Chain
 * Integrates OpenAI API for blockchain intelligence and analysis
 */

class AIOracle {
    constructor() {
        this.apiKey = null;
        this.model = 'gpt-4-mini';
        this.isLoading = false;
        this.conversationHistory = [];
        this.systemPrompt = `You are the Φ-Chain Oracle, an advanced AI assistant specialized in blockchain technology, 
        the golden ratio (Phi/Φ), and the Fibonacci Byzantine Agreement consensus mechanism. 
        You provide insightful analysis, predictions, and technical guidance for the Φ-Chain blockchain ecosystem.
        
        Key expertise areas:
        - Fibonacci Byzantine Agreement (FBA) consensus algorithm
        - Golden ratio applications in blockchain architecture
        - Reversible computing and energy efficiency
        - Quantum-resistant cryptography
        - Smart contract analysis and security
        - Network performance optimization
        
        Always provide accurate, technical responses grounded in blockchain principles and mathematical rigor.`;
        
        this.initializeAPI();
    }

    initializeAPI() {
        // Check if we're in a browser environment with backend support
        this.apiEndpoint = '/api/oracle';
        this.useBackend = true;
    }

    async queryOracle(userQuery) {
        if (!userQuery.trim()) {
            return "Veuillez entrer une question valide.";
        }

        this.isLoading = true;
        const responseElement = document.getElementById('oracle-response');
        const queryBtn = document.getElementById('query-oracle-btn');

        try {
            // Add user query to conversation history
            this.conversationHistory.push({
                role: 'user',
                content: userQuery
            });

            // Show loading state
            responseElement.textContent = '⏳ L\'Oracle réfléchit...\n\nTraitement de votre requête...';
            queryBtn.disabled = true;
            queryBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Interrogation en cours...';

            // Call the backend API
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: userQuery,
                    history: this.conversationHistory.slice(-10), // Keep last 10 messages for context
                    systemPrompt: this.systemPrompt
                })
            });

            if (!response.ok) {
                // Fallback to simulated response if backend is not available
                return await this.getSimulatedOracleResponse(userQuery);
            }

            const data = await response.json();
            const oracleResponse = data.response || data.message || 'Erreur: Pas de réponse reçue.';

            // Add oracle response to conversation history
            this.conversationHistory.push({
                role: 'assistant',
                content: oracleResponse
            });

            return oracleResponse;

        } catch (error) {
            console.error('Oracle API Error:', error);
            // Fallback to simulated response
            return await this.getSimulatedOracleResponse(userQuery);
        } finally {
            this.isLoading = false;
            queryBtn.disabled = false;
            queryBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Interroger l\'Oracle';
        }
    }

    async getSimulatedOracleResponse(query) {
        /**
         * Simulated Oracle responses for demonstration
         * In production, these would come from the OpenAI API via backend
         */
        
        const lowerQuery = query.toLowerCase();
        
        const responses = {
            fibonacci: `🔷 ANALYSE FIBONACCI 🔷

Le nombre d'or (Φ ≈ 1.618) est fondamental à l'architecture de Φ-Chain:

1. CONSENSUS FBA:
   - Les nœuds validateurs sont organisés selon les ratios de Fibonacci
   - Cela réduit exponentiellement la complexité du consensus
   - Exemple: Pour 100 nœuds, seuls ~62 sont nécessaires pour l'accord (ratio Φ)

2. STRUCTURE DE BLOC:
   - Taille de bloc: 4 MB (2^2 MB)
   - Temps de bloc: 15 secondes (nombre de Fibonacci)
   - Capacité: 1000+ TPS (transactions par seconde)

3. SÉCURITÉ QUANTIQUE:
   - Utilise des courbes elliptiques résistantes aux attaques quantiques
   - Longueur de clé: 256 bits (2^8)
   - Hachage: SHA-3 (Keccak)

Recommandation: Explorez la visualisation de Fibonacci pour une compréhension visuelle.`,

            oracle: `🧠 À PROPOS DE L'ORACLE IA 🧠

Je suis l'Oracle IA de Φ-Chain, spécialisé dans:

✓ Analyse de la blockchain et des transactions
✓ Prédictions de performance réseau
✓ Optimisation des smart contracts
✓ Sécurité et audit de consensus
✓ Conseils en architecture décentralisée

Mes capacités:
- Traitement du langage naturel (NLP)
- Analyse de données en temps réel
- Modélisation prédictive
- Recommandations intelligentes

Posez-moi des questions sur:
- Comment fonctionne le consensus FBA?
- Quelle est la sécurité de Φ-Chain?
- Comment optimiser mon smart contract?
- Quelles sont les tendances du marché?`,

            wallet: `💼 GESTION DE PORTEFEUILLE 💼

Φ-Chain supporte plusieurs portefeuilles:

1. METAMASK (Ethereum):
   - Connexion EVM-compatible
   - Support des tokens ERC-20
   - Transactions sécurisées

2. PHANTOM (Solana):
   - Portefeuille haute performance
   - Transactions rapides et bon marché
   - Intégration DeFi

3. WALLETCONNECT:
   - Solution universelle
   - Support multi-chaîne
   - Sécurité maximale

Conseils de sécurité:
- Conservez vos clés privées en sécurité
- Utilisez des portefeuilles matériels pour les gros montants
- Vérifiez toujours les adresses avant de transférer
- Activez l'authentification à deux facteurs`,

            simulator: `📊 SIMULATEURS & OUTILS 📊

Φ-Chain propose plusieurs simulateurs:

1. BLOCKCHAIN SIMULATOR:
   - Visualisez la création de blocs
   - Simulez des transactions
   - Analysez la propagation du réseau
   - Observez les confirmations en temps réel

2. CONSENSUS MONITOR:
   - Suivi en direct du consensus FBA
   - Statistiques de participation des nœuds
   - Analyse de la latence
   - Détection d'anomalies

3. FIBONACCI VISUALIZATION:
   - Représentation visuelle du ratio d'or
   - Structure de la chaîne
   - Distribution des nœuds
   - Patterns mathématiques

Utilisation:
- Cliquez sur les liens dans la section "Simulateurs & Outils"
- Explorez les données en temps réel
- Exportez les résultats pour analyse`,

            security: `🔒 SÉCURITÉ DE Φ-CHAIN 🔒

Architecture de sécurité multicouche:

1. NIVEAU CONSENSUS:
   - Algorithme FBA résistant aux attaques byzantines
   - Tolérance aux pannes: 1/3 des nœuds
   - Protection contre les attaques Sybil

2. NIVEAU CRYPTOGRAPHIE:
   - Signatures ECDSA (Elliptic Curve Digital Signature Algorithm)
   - Hachage Keccak-256
   - Résistance quantique (post-quantique)

3. NIVEAU SMART CONTRACT:
   - Vérification formelle
   - Audit de sécurité
   - Sandboxing des exécutions

4. NIVEAU RÉSEAU:
   - Chiffrement TLS 1.3
   - Authentification mutuelle
   - DDoS protection

Audit: Φ-Chain a été audité par des experts en sécurité blockchain.`,

            performance: `⚡ PERFORMANCE & SCALABILITÉ ⚡

Métriques de performance de Φ-Chain:

1. DÉBIT:
   - Capacité: 1000+ TPS
   - Temps de bloc: 15 secondes
   - Finalité: Immédiate après consensus

2. LATENCE:
   - Latence moyenne: 2-3 secondes
   - Latence P99: < 5 secondes
   - Temps de confirmation: 1 bloc

3. SCALABILITÉ:
   - Sharding horizontal: Jusqu'à 100 shards
   - Compression de bloc: Réduction de 40%
   - Pruning de l'état: Réduction de 60%

4. COÛTS:
   - Frais de transaction: < 0.001 Φ
   - Coût par transaction: < 0.01 USD
   - Frais de déploiement: Compétitifs

Comparaison:
- Bitcoin: 7 TPS, ~10 min de finalité
- Ethereum: 15 TPS, ~15 sec de finalité
- Φ-Chain: 1000+ TPS, ~15 sec de finalité`,

            default: `🌟 ORACLE DE Φ-CHAIN 🌟

Bienvenue! Je suis votre assistant IA pour Φ-Chain.

Vous pouvez me poser des questions sur:
📌 Fibonacci et le nombre d'or
📌 Consensus FBA et validation
📌 Portefeuilles et transactions
📌 Simulateurs et outils
📌 Sécurité et cryptographie
📌 Performance et scalabilité
📌 Smart contracts et DeFi

Exemples de questions:
- "Comment fonctionne le consensus FBA?"
- "Quelle est la sécurité de Φ-Chain?"
- "Comment créer un smart contract?"
- "Quelles sont les performances?"

Posez votre question ci-dessus pour commencer!`
        };

        // Match query to response category
        let response = responses.default;
        
        if (lowerQuery.includes('fibonacci') || lowerQuery.includes('phi') || lowerQuery.includes('nombre d\'or')) {
            response = responses.fibonacci;
        } else if (lowerQuery.includes('oracle') || lowerQuery.includes('ia') || lowerQuery.includes('intelligence')) {
            response = responses.oracle;
        } else if (lowerQuery.includes('wallet') || lowerQuery.includes('portefeuille') || lowerQuery.includes('metamask') || lowerQuery.includes('phantom')) {
            response = responses.wallet;
        } else if (lowerQuery.includes('simulator') || lowerQuery.includes('simulateur') || lowerQuery.includes('blockchain')) {
            response = responses.simulator;
        } else if (lowerQuery.includes('sécurité') || lowerQuery.includes('security') || lowerQuery.includes('cryptographie')) {
            response = responses.security;
        } else if (lowerQuery.includes('performance') || lowerQuery.includes('scalabilité') || lowerQuery.includes('tps')) {
            response = responses.performance;
        }

        return response;
    }

    clearHistory() {
        this.conversationHistory = [];
    }
}

// Initialize the Oracle
const aiOracle = new AIOracle();

// Function to query the Oracle from HTML
async function queryAIOracle() {
    const input = document.getElementById('oracle-input');
    const response = document.getElementById('oracle-response');
    const query = input.value.trim();

    if (!query) {
        alert('Veuillez entrer une question.');
        return;
    }

    const oracleResponse = await aiOracle.queryOracle(query);
    response.textContent = oracleResponse;
    input.value = '';
    input.focus();
}

// Allow Enter key to submit query
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('oracle-input');
    if (input) {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                queryAIOracle();
            }
        });
    }
});
