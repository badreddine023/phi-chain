"""
Φ-Chain Smart Contracts Module

Provides smart contract functionality for the Φ-Chain blockchain.
"""

from .contract_vm import (
    PhiSmartContractVM,
    SmartContractCompiler,
    ContractState,
    ExecutionContext,
    OpCode
)
from .contract_system import (
    SmartContractSystem,
    ContractDeployment,
    ContractEvent,
    ContractStatus,
    ContractLibrary
)

__all__ = [
    "PhiSmartContractVM",
    "SmartContractCompiler",
    "ContractState",
    "ExecutionContext",
    "OpCode",
    "SmartContractSystem",
    "ContractDeployment",
    "ContractEvent",
    "ContractStatus",
    "ContractLibrary"
]
