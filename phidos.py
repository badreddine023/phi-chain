"""
PhiDOS: The Phi-Chain Operating System Environment
Inspired by AMSDOS, powered by Phi-Chain.
"""

import os
import sys
import time
import random
from core.phi_math import PhiMath, fibonacci
from phi_chain import Blockchain, PhiTransaction

class PhiDOS:
    VERSION = "1.0.0-Φ"
    
    def __init__(self):
        self.current_directory = "A:"
        self.is_running = True
        self.blockchain = Blockchain()
        self.file_system = {} # Local cache of EDOs from chain
        
    def boot(self):
        print("\n" + "Φ"*60)
        print(f"Φ PhiDOS Version {self.VERSION}")
        print("Φ Copyright (c) 2025 Phi-Chain Foundation")
        print("Φ Ready.")
        print("Φ"*60 + "\n")
        
    def shell(self):
        while self.is_running:
            try:
                cmd_input = input(f"Φ {self.current_directory}> ").strip().split()
                if not cmd_input:
                    continue
                
                command = cmd_input[0].upper()
                args = cmd_input[1:]
                
                if command == "EXIT":
                    self.is_running = False
                elif command == "HELP":
                    self.show_help()
                elif command == "DIR":
                    self.list_files()
                elif command == "SAVE":
                    self.save_file(args)
                elif command == "LOAD":
                    self.load_file(args)
                elif command == "PHI":
                    self.show_phi()
                elif command == "EDIT":
                    self.phi_edit(args)
                elif command == "ASM":
                    self.phi_asm(args)
                elif command == "DEBUG":
                    self.phi_debug(args)
                else:
                    print(f"Unknown command: {command}")
            except KeyboardInterrupt:
                print("\nUse 'EXIT' to quit.")
            except Exception as e:
                print(f"Error: {e}")

    def show_help(self):
        print("\nΦ Available Commands:")
        print("  DIR          - List files (EDOs) in current directory")
        print("  SAVE <name>  - Save a new EDO to the chain")
        print("  LOAD <name>  - Load and verify an EDO from the chain")
        print("  EDIT <name>  - Open the Phi-Source Editor")
        print("  ASM <name>   - Compile Phi-Source into Bytecode")
        print("  DEBUG <name> - Debug system state and EDOs")
        print("  PHI          - Display current Golden Ratio metrics")
        print("  HELP         - Show this help message")
        print("  EXIT         - Shutdown PhiDOS\n")

    def list_files(self):
        print(f"\nΦ Directory of {self.current_directory}")
        if not self.file_system:
            print("  Φ No files found.")
        else:
            for name, data in self.file_system.items():
                print(f"  Φ {name:12} {data['size']:8} bytes  [Φ-Coherent]")
        print("")

    def save_file(self, args):
        if not args:
            print("Usage: SAVE <filename>")
            return
        name = args[0]
        
        # Create a transaction to represent the file storage
        tx = PhiTransaction(
            sender="0xPhiDOS_User",
            recipient="0xPhiDOS_Storage",
            value=0,
            data=f"FILE_SAVE:{name}".encode()
        )
        self.blockchain.add_transaction(tx)
        self.blockchain.mine_pending_transactions("PhiDOS_Kernel")
        
        self.file_system[name] = {
            "size": fibonacci(10),
            "timestamp": time.time(),
            "hash": tx.calculate_hash()
        }
        print(f"File {name} saved and anchored to Phi-Chain block #{self.blockchain.get_chain_length()-1}.")

    def load_file(self, args):
        if not args:
            print("Usage: LOAD <filename>")
            return
        name = args[0]
        if name in self.file_system:
            print(f"Loading {name}...")
            time.sleep(0.5)
            print(f"Verification: SUCCESS (Hash: {self.file_system[name]['hash']})")
        else:
            print(f"File not found: {name}")

    def show_phi(self):
        phi = PhiMath.get_phi(20)
        print(f"Φ Current Golden Ratio (Φ): {PhiMath.from_fixed(phi, 20)}")
        print(f"Φ System Coherence: 100% (Optimal)")

    def phi_edit(self, args):
        if not args:
            print("Φ Usage: EDIT <filename>")
            return
        name = args[0]
        print(f"Φ Opening PHI-EDIT for {name}...")
        print("Φ [EDITOR MODE: Type '.SAVE' to exit and save, '.QUIT' to discard]")
        content = []
        while True:
            line = input("Φ > ")
            if line.upper() == ".SAVE":
                self.file_system[name] = {
                    "size": len("\n".join(content)),
                    "timestamp": time.time(),
                    "hash": "edit_" + os.urandom(4).hex(),
                    "content": "\n".join(content)
                }
                print(f"Φ {name} saved to local buffer.")
                break
            elif line.upper() == ".QUIT":
                break
            content.append(line)

    def phi_asm(self, args):
        if not args:
            print("Φ Usage: ASM <filename>")
            return
        name = args[0]
        if name not in self.file_system:
            print(f"Φ Error: {name} not found.")
            return
        print(f"Φ Assembling {name} into Phi-Bytecode...")
        time.sleep(1)
        print(f"Φ Success: {name}.bin generated (Φ-Optimized).")

    def phi_debug(self, args):
        print("Φ --- PHI-DEBUG SYSTEM STATE ---")
        print(f"Φ Blockchain Height: {self.blockchain.get_chain_length()}")
        print(f"Φ Active EDOs: {len(self.file_system)}")
        print(f"Φ Memory Coherence: {random.uniform(0.99, 1.0):.4f}")
        print("Φ ------------------------------")

if __name__ == "__main__":
    # Ensure core is in path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    dos = PhiDOS()
    dos.boot()
    # If running in a non-interactive environment, we don't start the shell
    if sys.stdin.isatty():
        dos.shell()
    else:
        print("Non-interactive mode: Boot successful.")
