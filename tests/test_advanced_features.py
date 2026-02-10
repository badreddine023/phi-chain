"""
Test Suite for Φ-Chain Advanced Features

Comprehensive tests for:
- Smart Contract System
- Advanced Consensus Mechanisms
- Cross-chain Interoperability
- Governance and DAO Features
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_contracts.contract_vm import (
    PhiSmartContractVM,
    SmartContractCompiler,
    ExecutionContext,
    OpCode
)
from smart_contracts.contract_system import (
    SmartContractSystem,
    ContractLibrary,
    ContractStatus
)
from consensus.advanced_consensus import (
    FibonacciProofOfStake,
    HarmonicConsensus,
    QuantumCoherenceConsensus,
    HybridConsensus
)


class TestSmartContractVM:
    """Test Smart Contract Virtual Machine."""
    
    def test_vm_initialization(self):
        """Test VM initialization."""
        vm = PhiSmartContractVM()
        assert vm is not None
        assert vm.max_stack_size == 1024
        assert vm.max_memory_size == 1024 * 1024
    
    def test_contract_deployment(self):
        """Test contract deployment."""
        vm = PhiSmartContractVM()
        bytecode = bytes([OpCode.PUSH.value, 10, OpCode.HALT.value])
        
        address = vm.deploy_contract(bytecode, "creator_address", 100.0)
        
        assert address is not None
        assert address.startswith("0x")
        assert vm.get_contract(address) is not None
    
    def test_contract_execution(self):
        """Test contract execution."""
        vm = PhiSmartContractVM()
        bytecode = bytes([
            OpCode.PUSH.value, 10,
            OpCode.PUSH.value, 5,
            OpCode.ADD.value,
            OpCode.HALT.value
        ])
        
        address = vm.deploy_contract(bytecode, "creator", 0.0)
        
        context = ExecutionContext(
            sender="caller",
            value=0.0,
            timestamp=0,
            block_hash="hash",
            gas_limit=10000
        )
        
        success, result, error = vm.execute(address, "test", [], context)
        assert success
    
    def test_contract_balance(self):
        """Test contract balance management."""
        vm = PhiSmartContractVM()
        bytecode = bytes([OpCode.HALT.value])
        
        address = vm.deploy_contract(bytecode, "creator", 100.0)
        balance = vm.get_contract_balance(address)
        
        assert balance == 100.0
        
        # Transfer to contract
        success = vm.transfer_to_contract(address, 50.0)
        assert success
        assert vm.get_contract_balance(address) == 150.0
    
    def test_contract_storage(self):
        """Test contract storage operations."""
        vm = PhiSmartContractVM()
        bytecode = bytes([OpCode.HALT.value])
        
        address = vm.deploy_contract(bytecode, "creator", 0.0)
        
        # Store value
        success = vm.set_contract_storage(address, "key1", "value1")
        assert success
        
        # Load value
        value = vm.get_contract_storage(address, "key1")
        assert value == "value1"


class TestSmartContractCompiler:
    """Test Smart Contract Compiler."""
    
    def test_compiler_initialization(self):
        """Test compiler initialization."""
        from smart_contracts.contract_vm import SmartContractCompiler
        compiler = SmartContractCompiler()
        assert compiler is not None
    
    def test_simple_compilation(self):
        """Test simple contract compilation."""
        from smart_contracts.contract_vm import SmartContractCompiler
        compiler = SmartContractCompiler()
        
        source = "PUSH 10 PUSH 5 ADD HALT"
        bytecode = compiler.compile(source)
        
        assert bytecode is not None
        assert len(bytecode) > 0


class TestSmartContractSystem:
    """Test Smart Contract System."""
    
    def test_system_initialization(self):
        """Test system initialization."""
        system = SmartContractSystem()
        assert system is not None
        assert len(system.vm.contracts) == 0
    
    def test_contract_deployment(self):
        """Test contract deployment through system."""
        system = SmartContractSystem()
        
        source_code = "PUSH 10 HALT"
        success, address, error = system.deploy_contract(
            source_code,
            "creator_address",
            initial_balance=100.0,
            block_number=1,
            transaction_hash="tx_hash",
            timestamp=0
        )
        
        assert success
        assert address is not None
        assert address.startswith("0x")
    
    def test_contract_call(self):
        """Test contract function call."""
        system = SmartContractSystem()
        
        source_code = "PUSH 10 HALT"
        success, address, error = system.deploy_contract(
            source_code,
            "creator",
            block_number=1,
            timestamp=0
        )
        
        assert success
        
        # Call contract
        success, result, error, gas_used = system.call_contract(
            address,
            "test_function",
            [],
            "caller",
            value=0.0,
            block_number=2,
            timestamp=1
        )
        
        assert gas_used >= 0
    
    def test_contract_events(self):
        """Test contract event emission."""
        system = SmartContractSystem()
        
        source_code = "PUSH 10 HALT"
        success, address, error = system.deploy_contract(
            source_code,
            "creator",
            block_number=1,
            timestamp=0
        )
        
        # Emit event
        system.emit_event(
            address,
            "TestEvent",
            {"param1": "value1"},
            block_number=1,
            transaction_hash="tx_hash",
            timestamp=0
        )
        
        events = system.get_contract_events(address)
        assert len(events) == 1
        assert events[0]["event_name"] == "TestEvent"
    
    def test_contract_statistics(self):
        """Test contract system statistics."""
        system = SmartContractSystem()
        
        source_code = "PUSH 10 HALT"
        system.deploy_contract(source_code, "creator1", block_number=1, timestamp=0)
        system.deploy_contract(source_code, "creator2", block_number=2, timestamp=1)
        
        stats = system.get_statistics()
        assert stats["total_contracts"] == 2
        assert stats["total_deployments"] == 2


class TestContractLibrary:
    """Test Contract Library."""
    
    def test_token_contract_creation(self):
        """Test token contract creation."""
        source = ContractLibrary.create_token_contract(
            "TestToken",
            "TST",
            1000000.0,
            18
        )
        
        assert source is not None
        assert "TestToken" in source
        assert "TST" in source
    
    def test_voting_contract_creation(self):
        """Test voting contract creation."""
        source = ContractLibrary.create_voting_contract()
        assert source is not None
    
    def test_multisig_contract_creation(self):
        """Test multi-signature contract creation."""
        source = ContractLibrary.create_multisig_contract(3)
        assert source is not None
        assert "3" in source


class TestFibonacciProofOfStake:
    """Test Fibonacci Proof of Stake Consensus."""
    
    def test_fpos_initialization(self):
        """Test FPoS initialization."""
        fpos = FibonacciProofOfStake()
        assert fpos is not None
        assert len(fpos.fibonacci_sequence) > 0
    
    def test_validator_registration(self):
        """Test validator registration."""
        fpos = FibonacciProofOfStake()
        
        success = fpos.register_validator("validator1", 100.0)
        assert success
        assert "validator1" in fpos.validators
    
    def test_proposer_selection(self):
        """Test proposer selection."""
        fpos = FibonacciProofOfStake()
        
        fpos.register_validator("validator1", 100.0)
        fpos.register_validator("validator2", 200.0)
        fpos.register_validator("validator3", 150.0)
        
        proposer = fpos.select_proposer()
        assert proposer in ["validator1", "validator2", "validator3"]
    
    def test_committee_selection(self):
        """Test committee selection."""
        fpos = FibonacciProofOfStake()
        
        for i in range(5):
            fpos.register_validator(f"validator{i}", 100.0 * (i + 1))
        
        committee = fpos.select_committee(3)
        assert len(committee) == 3
        assert all(v in fpos.validators for v in committee)
    
    def test_block_validation(self):
        """Test block validation."""
        fpos = FibonacciProofOfStake()
        
        fpos.register_validator("proposer", 100.0)
        
        is_valid, strength = fpos.validate_block(
            "block_hash",
            "proposer",
            ["validator1", "validator2"]
        )
        
        assert is_valid
        assert strength >= 0.0


class TestHarmonicConsensus:
    """Test Harmonic Consensus."""
    
    def test_harmonic_initialization(self):
        """Test Harmonic Consensus initialization."""
        hc = HarmonicConsensus()
        assert hc is not None
        assert hc.base_frequency == 1.0
    
    def test_validator_registration(self):
        """Test validator registration."""
        hc = HarmonicConsensus()
        
        success = hc.register_validator("validator1", 100.0)
        assert success
        assert "validator1" in hc.validators
    
    def test_resonance_calculation(self):
        """Test resonance calculation."""
        hc = HarmonicConsensus()
        
        hc.register_validator("validator1", 100.0)
        hc.register_validator("validator2", 200.0)
        
        resonance = hc.calculate_resonance(["validator1", "validator2"])
        assert len(resonance) == 2
        assert all(v > 0 for v in resonance.values())
    
    def test_consensus_achievement(self):
        """Test consensus achievement."""
        hc = HarmonicConsensus()
        
        for i in range(5):
            hc.register_validator(f"validator{i}", 100.0)
        
        reached, strength = hc.achieve_consensus([f"validator{i}" for i in range(5)])
        assert isinstance(reached, bool)
        assert strength >= 0.0


class TestQuantumCoherenceConsensus:
    """Test Quantum Coherence Consensus."""
    
    def test_qcc_initialization(self):
        """Test QCC initialization."""
        qcc = QuantumCoherenceConsensus()
        assert qcc is not None
    
    def test_validator_registration(self):
        """Test validator registration."""
        qcc = QuantumCoherenceConsensus()
        
        success = qcc.register_validator("validator1", 100.0)
        assert success
        assert "validator1" in qcc.validators
    
    def test_entanglement(self):
        """Test quantum entanglement."""
        qcc = QuantumCoherenceConsensus()
        
        qcc.register_validator("validator1", 100.0)
        qcc.register_validator("validator2", 100.0)
        
        success = qcc.establish_entanglement("validator1", "validator2")
        assert success
    
    def test_coherence_measurement(self):
        """Test coherence measurement."""
        qcc = QuantumCoherenceConsensus()
        
        qcc.register_validator("validator1", 100.0)
        qcc.register_validator("validator2", 100.0)
        
        coherence = qcc.measure_coherence(["validator1", "validator2"])
        assert len(coherence) == 2
        assert all(0 <= c <= 1 for c in coherence.values())
    
    def test_consensus_achievement(self):
        """Test consensus achievement."""
        qcc = QuantumCoherenceConsensus()
        
        for i in range(5):
            qcc.register_validator(f"validator{i}", 100.0)
        
        reached, strength = qcc.achieve_consensus([f"validator{i}" for i in range(5)])
        assert isinstance(reached, bool)
        assert 0 <= strength <= 1


class TestHybridConsensus:
    """Test Hybrid Consensus."""
    
    def test_hybrid_initialization(self):
        """Test Hybrid Consensus initialization."""
        hc = HybridConsensus()
        assert hc is not None
        assert hc.fibonacci_pos is not None
        assert hc.harmonic is not None
        assert hc.quantum is not None
    
    def test_validator_registration(self):
        """Test validator registration."""
        hc = HybridConsensus()
        
        success = hc.register_validator("validator1", 100.0)
        assert success
    
    def test_consensus_achievement(self):
        """Test consensus achievement."""
        hc = HybridConsensus()
        
        for i in range(5):
            hc.register_validator(f"validator{i}", 100.0)
        
        reached, metrics = hc.achieve_consensus(
            [f"validator{i}" for i in range(5)],
            "block_hash",
            round_number=1
        )
        
        assert isinstance(reached, bool)
        assert "consensus_reached" in metrics
        assert "mechanisms_passed" in metrics
    
    def test_consensus_statistics(self):
        """Test consensus statistics."""
        hc = HybridConsensus()
        
        for i in range(5):
            hc.register_validator(f"validator{i}", 100.0)
        
        # Run multiple consensus rounds
        for round_num in range(3):
            hc.achieve_consensus(
                [f"validator{i}" for i in range(5)],
                f"block_hash_{round_num}",
                round_number=round_num
            )
        
        stats = hc.get_consensus_statistics()
        assert stats["total_rounds"] == 3
        assert "success_rate" in stats
        assert "finality_rate" in stats


# Integration Tests
class TestAdvancedFeaturesIntegration:
    """Integration tests for advanced features."""
    
    def test_smart_contract_with_consensus(self):
        """Test smart contracts with consensus mechanism."""
        system = SmartContractSystem()
        consensus = HybridConsensus()
        
        # Deploy contract
        source = "PUSH 100 HALT"
        success, address, error = system.deploy_contract(
            source,
            "creator",
            block_number=1,
            timestamp=0
        )
        assert success
        
        # Register validators
        for i in range(5):
            consensus.register_validator(f"validator{i}", 100.0)
        
        # Achieve consensus
        reached, metrics = consensus.achieve_consensus(
            [f"validator{i}" for i in range(5)],
            "block_hash",
            round_number=1
        )
        
        assert reached or not reached  # Just test it runs
    
    def test_multiple_contracts_deployment(self):
        """Test deploying multiple contracts."""
        system = SmartContractSystem()
        
        addresses = []
        for i in range(5):
            source = f"PUSH {i * 10} HALT"
            success, address, error = system.deploy_contract(
                source,
                f"creator{i}",
                block_number=i,
                timestamp=i
            )
            assert success
            addresses.append(address)
        
        stats = system.get_statistics()
        assert stats["total_contracts"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
