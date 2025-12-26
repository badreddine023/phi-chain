import hashlib
from core.phi_integer_math import PhiIntegerMath, PHI_NUMERATOR

class PhiAddressSystem:
    """
    Pure PHI Address System: PHI[xxxx-xxxx-xxxx-xxxx][CRC][Golden-Check]
    """
    
    @staticmethod
    def generate_phi_address(public_key_hex: str) -> str:
        """
        Generate a PHI address from a public key.
        """
        # 1. Convert to integer
        key_int = int(public_key_hex, 16)
        
        # 2. Apply Phi transformation
        transformed = PhiIntegerMath.phi_multiply(key_int, PHI_NUMERATOR)
        
        # 3. Extract 64-bit identifier
        identifier = transformed & ((1 << 64) - 1)
        
        # 4. Format as PHI-XXXX-XXXX-XXXX-XXXX
        segments = []
        for i in range(4):
            segment = (identifier >> (16 * (3 - i))) & 0xFFFF
            segments.append(f"{segment:04X}")
        
        # 5. Calculate Golden CRC
        golden_crc = PhiAddressSystem.calculate_golden_crc(identifier)
        
        # 6. Generate Math Check
        math_check = PhiAddressSystem.generate_phi_math_check(identifier)
        
        address = f"PHI[{'-'.join(segments)}][{golden_crc:04X}][{math_check:04X}]"
        return address

    @staticmethod
    def calculate_golden_crc(value: int) -> int:
        """Calculate CRC using the Phi algorithm."""
        crc = 0xFFFFFFFF
        phi_poly = 0xEDB88320  # Modified Phi polynomial
        
        for i in range(64):
            bit = (value >> i) & 1
            crc_bit = (crc ^ bit) & 1
            
            if crc_bit:
                crc = (crc >> 1) ^ phi_poly
            else:
                crc = crc >> 1
        
        return crc & 0xFFFF

    @staticmethod
    def generate_phi_math_check(identifier: int) -> int:
        """Generate a mathematical proof using Phi."""
        # GF(identifier % 100) for mathematical proof
        fib_check = PhiIntegerMath.golden_fibonacci(identifier % 100)
        
        # Convert to 16-bit
        return fib_check & 0xFFFF

    @staticmethod
    def validate_address(address: str) -> bool:
        """Validate a PHI address."""
        try:
            # Basic format check: PHI[XXXX-XXXX-XXXX-XXXX][XXXX][XXXX]
            if not (address.startswith("PHI[") and address.endswith("]")):
                return False
            
            parts = address[4:-1].split("][")
            if len(parts) != 3:
                return False
            
            segments_str, crc_str, check_str = parts
            segments = segments_str.split("-")
            if len(segments) != 4:
                return False
            
            # Reconstruct identifier
            identifier = 0
            for i, seg in enumerate(segments):
                identifier |= (int(seg, 16) << (16 * (3 - i)))
            
            # Verify CRC
            expected_crc = PhiAddressSystem.calculate_golden_crc(identifier)
            if f"{expected_crc:04X}" != crc_str:
                return False
            
            # Verify Math Check
            expected_check = PhiAddressSystem.generate_phi_math_check(identifier)
            if f"{expected_check:04X}" != check_str:
                return False
                
            return True
        except Exception:
            return False

if __name__ == "__main__":
    # Test address generation
    pub_key = hashlib.sha256(b"test_key").hexdigest()
    addr = PhiAddressSystem.generate_phi_address(pub_key)
    print(f"Generated Address: {addr}")
    print(f"Is Valid? {PhiAddressSystem.validate_address(addr)}")
    print(f"Is 'Invalid' Valid? {PhiAddressSystem.validate_address('PHI[0000-0000-0000-0000][0000][0000]')}")
