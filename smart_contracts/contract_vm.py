"""
Φ-Chain Smart Contract Virtual Machine (ΦSVM)

A lightweight, efficient virtual machine for executing smart contracts
on the Φ-Chain blockchain. Features include:

- Stack-based bytecode execution
- Gas metering for resource management
- State management and persistence
- Contract deployment and invocation
- Built-in contract functions
- Security sandboxing
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
from datetime import datetime


class OpCode(Enum):
    """Smart contract operation codes."""
    # Stack operations
    PUSH = 0x01
    POP = 0x02
    DUP = 0x03
    SWAP = 0x04
    
    # Arithmetic operations
    ADD = 0x10
    SUB = 0x11
    MUL = 0x12
    DIV = 0x13
    MOD = 0x14
    
    # Comparison operations
    EQ = 0x20
    LT = 0x21
    GT = 0x22
    LTE = 0x23
    GTE = 0x24
    
    # Logical operations
    AND = 0x30
    OR = 0x31
    NOT = 0x32
    
    # Control flow
    JMP = 0x40
    JMPIF = 0x41
    CALL = 0x42
    RETURN = 0x43
    
    # Storage operations
    SSTORE = 0x50  # Store to contract storage
    SLOAD = 0x51   # Load from contract storage
    MSTORE = 0x52  # Store to memory
    MLOAD = 0x53   # Load from memory
    
    # State operations
    SENDER = 0x60  # Get transaction sender
    VALUE = 0x61   # Get transaction value
    TIMESTAMP = 0x62  # Get block timestamp
    BLOCKHASH = 0x63  # Get block hash
    
    # Contract operations
    CREATE = 0x70  # Create new contract
    CALL_CONTRACT = 0x71  # Call another contract
    SELFDESTRUCT = 0x72  # Destroy contract
    
    # Special
    HALT = 0xFF


@dataclass
class ContractState:
    """Represents the state of a deployed contract."""
    address: str
    code: bytes
    storage: Dict[str, Any] = field(default_factory=dict)
    balance: float = 0.0
    creator: str = ""
    created_at: int = 0
    nonce: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "address": self.address,
            "code": self.code.hex(),
            "storage": self.storage,
            "balance": self.balance,
            "creator": self.creator,
            "created_at": self.created_at,
            "nonce": self.nonce
        }


@dataclass
class ExecutionContext:
    """Context for contract execution."""
    sender: str
    value: float
    timestamp: int
    block_hash: str
    gas_limit: int
    gas_used: int = 0
    memory: Dict[int, Any] = field(default_factory=dict)
    stack: List[Any] = field(default_factory=list)
    return_value: Any = None
    reverted: bool = False
    revert_reason: str = ""


class PhiSmartContractVM:
    """
    Φ-Chain Smart Contract Virtual Machine
    
    Executes smart contracts with gas metering, state management,
    and security sandboxing.
    """
    
    def __init__(self, max_stack_size: int = 1024, max_memory_size: int = 1024 * 1024):
        """Initialize the VM."""
        self.contracts: Dict[str, ContractState] = {}
        self.max_stack_size = max_stack_size
        self.max_memory_size = max_memory_size
        self.gas_costs = self._init_gas_costs()
    
    def _init_gas_costs(self) -> Dict[OpCode, int]:
        """Initialize gas costs for operations."""
        return {
            OpCode.PUSH: 3,
            OpCode.POP: 2,
            OpCode.DUP: 3,
            OpCode.SWAP: 3,
            OpCode.ADD: 3,
            OpCode.SUB: 3,
            OpCode.MUL: 5,
            OpCode.DIV: 5,
            OpCode.MOD: 5,
            OpCode.EQ: 3,
            OpCode.LT: 3,
            OpCode.GT: 3,
            OpCode.AND: 3,
            OpCode.OR: 3,
            OpCode.NOT: 3,
            OpCode.JMP: 8,
            OpCode.JMPIF: 10,
            OpCode.CALL: 40,
            OpCode.SSTORE: 20000,  # Expensive storage operation
            OpCode.SLOAD: 200,
            OpCode.MSTORE: 3,
            OpCode.MLOAD: 3,
            OpCode.CREATE: 32000,
            OpCode.CALL_CONTRACT: 40,
            OpCode.SELFDESTRUCT: 5000,
        }
    
    def deploy_contract(
        self,
        code: bytes,
        creator: str,
        initial_balance: float = 0.0,
        timestamp: int = 0
    ) -> str:
        """
        Deploy a new contract to the blockchain.
        
        Args:
            code: Compiled contract bytecode
            creator: Address of contract creator
            initial_balance: Initial balance for contract
            timestamp: Deployment timestamp
            
        Returns:
            Contract address
        """
        # Generate contract address from code and creator
        contract_hash = hashlib.sha256(
            (code.hex() + creator).encode()
        ).hexdigest()[:40]
        contract_address = f"0x{contract_hash}"
        
        # Create contract state
        contract = ContractState(
            address=contract_address,
            code=code,
            balance=initial_balance,
            creator=creator,
            created_at=timestamp
        )
        
        self.contracts[contract_address] = contract
        return contract_address
    
    def execute(
        self,
        contract_address: str,
        function_name: str,
        args: List[Any],
        context: ExecutionContext
    ) -> Tuple[bool, Any, str]:
        """
        Execute a contract function.
        
        Args:
            contract_address: Address of contract to execute
            function_name: Name of function to call
            args: Function arguments
            context: Execution context
            
        Returns:
            Tuple of (success, return_value, error_message)
        """
        if contract_address not in self.contracts:
            return False, None, f"Contract not found: {contract_address}"
        
        contract = self.contracts[contract_address]
        
        try:
            # Execute bytecode
            result = self._execute_bytecode(
                contract.code,
                args,
                contract,
                context
            )
            
            if context.reverted:
                return False, None, context.revert_reason
            
            return True, result, ""
            
        except Exception as e:
            return False, None, str(e)
    
    def _execute_bytecode(
        self,
        bytecode: bytes,
        args: List[Any],
        contract: ContractState,
        context: ExecutionContext
    ) -> Any:
        """
        Execute bytecode with stack-based VM.
        
        Args:
            bytecode: Contract bytecode to execute
            args: Function arguments
            contract: Contract state
            context: Execution context
            
        Returns:
            Return value from execution
        """
        pc = 0  # Program counter
        context.stack = list(args)  # Initialize stack with arguments
        
        while pc < len(bytecode):
            # Check gas limit
            if context.gas_used >= context.gas_limit:
                raise RuntimeError("Out of gas")
            
            # Fetch opcode
            opcode_byte = bytecode[pc]
            try:
                opcode = OpCode(opcode_byte)
            except ValueError:
                raise RuntimeError(f"Invalid opcode: {opcode_byte}")
            
            # Charge gas
            if opcode in self.gas_costs:
                context.gas_used += self.gas_costs[opcode]
            
            # Execute opcode
            pc = self._execute_opcode(
                opcode,
                bytecode,
                pc,
                context,
                contract
            )
            
            if opcode == OpCode.HALT or context.reverted:
                break
        
        return context.return_value
    
    def _execute_opcode(
        self,
        opcode: OpCode,
        bytecode: bytes,
        pc: int,
        context: ExecutionContext,
        contract: ContractState
    ) -> int:
        """
        Execute a single opcode.
        
        Args:
            opcode: Operation to execute
            bytecode: Full bytecode
            pc: Program counter
            context: Execution context
            contract: Contract state
            
        Returns:
            New program counter value
        """
        stack = context.stack
        
        # Stack operations
        if opcode == OpCode.PUSH:
            pc += 1
            value = bytecode[pc]
            stack.append(value)
        
        elif opcode == OpCode.POP:
            if stack:
                stack.pop()
        
        elif opcode == OpCode.DUP:
            if stack:
                stack.append(stack[-1])
        
        elif opcode == OpCode.SWAP:
            if len(stack) >= 2:
                stack[-1], stack[-2] = stack[-2], stack[-1]
        
        # Arithmetic operations
        elif opcode == OpCode.ADD:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        
        elif opcode == OpCode.SUB:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
        
        elif opcode == OpCode.MUL:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
        
        elif opcode == OpCode.DIV:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                if b != 0:
                    stack.append(a // b)
                else:
                    raise RuntimeError("Division by zero")
        
        elif opcode == OpCode.MOD:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                if b != 0:
                    stack.append(a % b)
                else:
                    raise RuntimeError("Division by zero")
        
        # Comparison operations
        elif opcode == OpCode.EQ:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(1 if a == b else 0)
        
        elif opcode == OpCode.LT:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(1 if a < b else 0)
        
        elif opcode == OpCode.GT:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(1 if a > b else 0)
        
        # Storage operations
        elif opcode == OpCode.SSTORE:
            if len(stack) >= 2:
                key = stack.pop()
                value = stack.pop()
                contract.storage[str(key)] = value
        
        elif opcode == OpCode.SLOAD:
            if stack:
                key = stack.pop()
                value = contract.storage.get(str(key), 0)
                stack.append(value)
        
        # State operations
        elif opcode == OpCode.SENDER:
            stack.append(context.sender)
        
        elif opcode == OpCode.VALUE:
            stack.append(context.value)
        
        elif opcode == OpCode.TIMESTAMP:
            stack.append(context.timestamp)
        
        # Control flow
        elif opcode == OpCode.RETURN:
            if stack:
                context.return_value = stack.pop()
            return len(bytecode)  # End execution
        
        elif opcode == OpCode.HALT:
            return len(bytecode)  # End execution
        
        return pc + 1
    
    def get_contract(self, address: str) -> Optional[ContractState]:
        """Get contract state by address."""
        return self.contracts.get(address)
    
    def get_contract_storage(self, address: str, key: str) -> Any:
        """Get value from contract storage."""
        contract = self.contracts.get(address)
        if contract:
            return contract.storage.get(key)
        return None
    
    def set_contract_storage(self, address: str, key: str, value: Any) -> bool:
        """Set value in contract storage."""
        contract = self.contracts.get(address)
        if contract:
            contract.storage[key] = value
            return True
        return False
    
    def get_contract_balance(self, address: str) -> float:
        """Get contract balance."""
        contract = self.contracts.get(address)
        if contract:
            return contract.balance
        return 0.0
    
    def transfer_to_contract(self, address: str, amount: float) -> bool:
        """Transfer funds to contract."""
        contract = self.contracts.get(address)
        if contract:
            contract.balance += amount
            return True
        return False


class SmartContractCompiler:
    """
    Compile high-level smart contract code to bytecode.
    
    Supports a simple Φ-Script language for contract development.
    """
    
    def __init__(self):
        """Initialize compiler."""
        self.opcodes = {name: member.value for name, member in OpCode.__members__.items()}
    
    def compile(self, source_code: str) -> bytes:
        """
        Compile Φ-Script source code to bytecode.
        
        Args:
            source_code: High-level contract code
            
        Returns:
            Compiled bytecode
        """
        bytecode = bytearray()
        
        # Simple tokenization
        tokens = source_code.split()
        
        for token in tokens:
            if token in self.opcodes:
                bytecode.append(self.opcodes[token])
            elif token.isdigit():
                bytecode.append(OpCode.PUSH.value)
                bytecode.append(int(token))
            elif token == "HALT":
                bytecode.append(OpCode.HALT.value)
        
        return bytes(bytecode)


# Example Φ-Script language:
# PUSH 10
# PUSH 5
# ADD
# RETURN
# This would push 10, push 5, add them, and return 15
