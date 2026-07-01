class PhiChain:
    def __init__(self, genesis_config: Optional[Dict] = None):
        # Default genesis (fallback)
        if genesis_config is None:
            genesis_config = {
                "block_time": 1.618033988749895,
                "initial_validators": 13,
                "shard_count": 21,
                "consensus_threshold": 0.618033988749895,
                "token_supply": 1618033988749895,
                "genesis_hash": "0x0000000000000000000000000000000000000000000000000000000000000000"
            }

        self.genesis = genesis_config
        self.state_vector = np.array([1, 1])
        self.q_matrix = np.array([[1, 1], [1, 0]])
        self.block_time_phi = genesis_config["block_time"]  # φ seconds

        # Create genesis block using the config
        self.chain = [self._create_genesis_block()]
        self.pending_transactions = []
        self.balances = self._init_balances_from_config()
        self.validators = self._init_validators_from_config()

    def _create_genesis_block(self) -> Block:
        genesis_block = Block(
            index=0,
            previous_hash=self.genesis["genesis_hash"],
            transactions=[],
            validator="Genesis",
            f_vector=(1, 1)
        )
        genesis_block.timestamp = 0  # start of time
        genesis_block.hash = self.genesis["genesis_hash"]  # fixed
        return genesis_block

    def _init_balances_from_config(self) -> Dict:
        # From your config example: visionary + core team each get 1% of token_supply
        total_supply = self.genesis["token_supply"]
        one_percent = total_supply * 0.01
        return {
            "0xPhiVisionaryAddress...": one_percent,
            "0xPhiArchitectAddress...": one_percent
        }

    def _init_validators_from_config(self) -> Dict:
        # Use the validator set from config
        validators = {}
        for v in self.genesis.get("initial_validators_set", []):
            validators[v["address"]] = {
                "stake": v["stake"],
                "coherence": self.genesis["consensus_threshold"],  # φ⁻¹ as starting coherence
                "blocks": 0,
                "entanglement_zone": v["entanglement_zone"]
            }
        return validators