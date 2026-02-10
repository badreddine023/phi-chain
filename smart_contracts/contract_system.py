"""
Φ-Chain Smart Contract System

Complete smart contract management system including:
- Contract deployment
- Contract invocation
- State management
- Event logging
- Contract verification
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
from datetime import datetime
from .contract_vm import PhiSmartContractVM, ExecutionContext, SmartContractCompiler


class ContractStatus(Enum):
    """Contract deployment status."""
    PENDING = "pending"
    DEPLOYED = "deployed"
    FAILED = "failed"
    DESTROYED = "destroyed"


@dataclass
class ContractEvent:
    """Represents a contract event."""
    contract_address: str
    event_name: str
    parameters: Dict[str, Any]
    block_number: int
    transaction_hash: str
    timestamp: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "contract_address": self.contract_address,
            "event_name": self.event_name,
            "parameters": self.parameters,
            "block_number": self.block_number,
            "transaction_hash": self.transaction_hash,
            "timestamp": self.timestamp
        }


@dataclass
class ContractDeployment:
    """Represents a contract deployment."""
    contract_address: str
    creator: str
    code_hash: str
    status: ContractStatus
    block_number: int
    transaction_hash: str
    timestamp: int
    gas_used: int
    initial_balance: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "contract_address": self.contract_address,
            "creator": self.creator,
            "code_hash": self.code_hash,
            "status": self.status.value,
            "block_number": self.block_number,
            "transaction_hash": self.transaction_hash,
            "timestamp": self.timestamp,
            "gas_used": self.gas_used,
            "initial_balance": self.initial_balance
        }


class SmartContractSystem:
    """
    Φ-Chain Smart Contract System
    
    Manages contract deployment, execution, and state management.
    """
    
    def __init__(self, blockchain=None):
        """
        Initialize smart contract system.
        
        Args:
            blockchain: Reference to blockchain instance
        """
        self.vm = PhiSmartContractVM()
        self.compiler = SmartContractCompiler()
        self.blockchain = blockchain
        self.deployments: Dict[str, ContractDeployment] = {}
        self.events: List[ContractEvent] = []
        self.call_history: List[Dict[str, Any]] = []
    
    def deploy_contract(
        self,
        source_code: str,
        creator: str,
        initial_balance: float = 0.0,
        block_number: int = 0,
        transaction_hash: str = "",
        timestamp: int = 0
    ) -> Tuple[bool, str, str]:
        """
        Deploy a new smart contract.
        
        Args:
            source_code: Contract source code (Φ-Script)
            creator: Address of contract creator
            initial_balance: Initial contract balance
            block_number: Block number of deployment
            transaction_hash: Transaction hash
            timestamp: Deployment timestamp
            
        Returns:
            Tuple of (success, contract_address, error_message)
        """
        try:
            # Compile contract code
            bytecode = self.compiler.compile(source_code)
            
            # Calculate code hash
            code_hash = hashlib.sha256(bytecode).hexdigest()
            
            # Deploy to VM
            contract_address = self.vm.deploy_contract(
                bytecode,
                creator,
                initial_balance,
                timestamp
            )
            
            # Record deployment
            deployment = ContractDeployment(
                contract_address=contract_address,
                creator=creator,
                code_hash=code_hash,
                status=ContractStatus.DEPLOYED,
                block_number=block_number,
                transaction_hash=transaction_hash,
                timestamp=timestamp,
                gas_used=len(bytecode) * 10,  # Approximate gas usage
                initial_balance=initial_balance
            )
            
            self.deployments[contract_address] = deployment
            
            return True, contract_address, ""
            
        except Exception as e:
            return False, "", str(e)
    
    def call_contract(
        self,
        contract_address: str,
        function_name: str,
        args: List[Any],
        caller: str,
        value: float = 0.0,
        block_number: int = 0,
        block_hash: str = "",
        timestamp: int = 0,
        gas_limit: int = 1000000
    ) -> Tuple[bool, Any, str, int]:
        """
        Call a contract function.
        
        Args:
            contract_address: Address of contract
            function_name: Function name to call
            args: Function arguments
            caller: Address of caller
            value: Value to send with call
            block_number: Current block number
            block_hash: Current block hash
            timestamp: Current timestamp
            gas_limit: Gas limit for execution
            
        Returns:
            Tuple of (success, return_value, error_message, gas_used)
        """
        try:
            # Create execution context
            context = ExecutionContext(
                sender=caller,
                value=value,
                timestamp=timestamp,
                block_hash=block_hash,
                gas_limit=gas_limit
            )
            
            # Execute contract
            success, result, error = self.vm.execute(
                contract_address,
                function_name,
                args,
                context
            )
            
            # Record call
            call_record = {
                "contract_address": contract_address,
                "function_name": function_name,
                "caller": caller,
                "args": args,
                "return_value": result,
                "success": success,
                "gas_used": context.gas_used,
                "timestamp": timestamp,
                "block_number": block_number
            }
            self.call_history.append(call_record)
            
            return success, result, error, context.gas_used
            
        except Exception as e:
            return False, None, str(e), 0
    
    def emit_event(
        self,
        contract_address: str,
        event_name: str,
        parameters: Dict[str, Any],
        block_number: int,
        transaction_hash: str,
        timestamp: int
    ) -> None:
        """
        Emit a contract event.
        
        Args:
            contract_address: Contract address
            event_name: Event name
            parameters: Event parameters
            block_number: Block number
            transaction_hash: Transaction hash
            timestamp: Event timestamp
        """
        event = ContractEvent(
            contract_address=contract_address,
            event_name=event_name,
            parameters=parameters,
            block_number=block_number,
            transaction_hash=transaction_hash,
            timestamp=timestamp
        )
        self.events.append(event)
    
    def get_contract_state(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """Get contract state."""
        contract = self.vm.get_contract(contract_address)
        if contract:
            return {
                "address": contract.address,
                "balance": contract.balance,
                "storage": contract.storage,
                "creator": contract.creator,
                "created_at": contract.created_at,
                "nonce": contract.nonce
            }
        return None
    
    def get_contract_storage(self, contract_address: str, key: str) -> Any:
        """Get value from contract storage."""
        return self.vm.get_contract_storage(contract_address, key)
    
    def get_contract_balance(self, contract_address: str) -> float:
        """Get contract balance."""
        return self.vm.get_contract_balance(contract_address)
    
    def get_contract_events(
        self,
        contract_address: str,
        event_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get contract events."""
        events = [
            e for e in self.events
            if e.contract_address == contract_address
        ]
        
        if event_name:
            events = [e for e in events if e.event_name == event_name]
        
        return [e.to_dict() for e in events]
    
    def get_contract_calls(self, contract_address: str) -> List[Dict[str, Any]]:
        """Get contract call history."""
        return [
            c for c in self.call_history
            if c["contract_address"] == contract_address
        ]
    
    def get_deployment_info(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """Get contract deployment information."""
        deployment = self.deployments.get(contract_address)
        if deployment:
            return deployment.to_dict()
        return None
    
    def list_contracts(self) -> List[Dict[str, Any]]:
        """List all deployed contracts."""
        return [
            {
                "address": contract.address,
                "creator": contract.creator,
                "balance": contract.balance,
                "created_at": contract.created_at,
                "nonce": contract.nonce
            }
            for contract in self.vm.contracts.values()
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get smart contract system statistics."""
        return {
            "total_contracts": len(self.vm.contracts),
            "total_deployments": len(self.deployments),
            "total_events": len(self.events),
            "total_calls": len(self.call_history),
            "total_gas_used": sum(c.get("gas_used", 0) for c in self.call_history),
            "total_contract_balance": sum(
                c.balance for c in self.vm.contracts.values()
            ),
            "deployments_by_status": {
                status.value: sum(
                    1 for d in self.deployments.values()
                    if d.status == status
                )
                for status in ContractStatus
            }
        }


class ContractLibrary:
    """
    Standard library of pre-built contracts for Φ-Chain.
    
    Provides common contract templates and utilities.
    """
    
    @staticmethod
    def create_token_contract(
        name: str,
        symbol: str,
        total_supply: float,
        decimals: int = 18
    ) -> str:
        """
        Create a standard token contract.
        
        Args:
            name: Token name
            symbol: Token symbol
            total_supply: Total supply
            decimals: Decimal places
            
        Returns:
            Contract source code
        """
        return f"""
        // Φ-Chain Token Contract
        // Name: {name}
        // Symbol: {symbol}
        // Total Supply: {total_supply}
        
        PUSH {int(total_supply)}
        PUSH {decimals}
        SSTORE
        HALT
        """
    
    @staticmethod
    def create_voting_contract() -> str:
        """Create a voting contract."""
        return """
        // Φ-Chain Voting Contract
        PUSH 0
        SSTORE
        HALT
        """
    
    @staticmethod
    def create_multisig_contract(required_signatures: int) -> str:
        """Create a multi-signature contract."""
        return f"""
        // Φ-Chain Multi-Signature Contract
        // Required Signatures: {required_signatures}
        PUSH {required_signatures}
        SSTORE
        HALT
        """
