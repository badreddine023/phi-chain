"""
قلب ابتكار Φ-Chain: النواة العكسية الزمنية
تمكين السلسلة المزدوجة (أمامية/خلفية) مع تماثل رياضي كامل
"""

import hashlib
import time
from typing import Tuple, List, Optional
from .phi_math import golden_ratio, fibonacci

class ReversibleBlock:
    """كتلة واحدة في السلسلة العكسية الزمنية"""
    
    def __init__(self, 
                 data: str, 
                 timestamp: float = None,
                 direction: str = "forward",  # "forward" أو "backward"
                 previous_hash: str = None):
        
        self.data = data
        self.direction = direction
        self.timestamp = timestamp or time.time()
        self.previous_hash = previous_hash
        self.nonce = 0
        self.phi_hash = self._calculate_phi_hash()
        self.mirror_hash = self._calculate_mirror_hash()
        
    def _calculate_phi_hash(self) -> str:
        """
        تجزئة φ: H_φ(x) = φ × SHA3-256(x) mod 2²⁵⁶
        
        تعتمد على النسبة الذهبية لإنتاج تجزئة غير عشوائية
        """
        phi = float(golden_ratio(30))
        data_bytes = self.data.encode('utf-8')
        
        # تجزئة أساسية
        base_hash = hashlib.sha3_256(data_bytes).digest()
        base_int = int.from_bytes(base_hash, 'big')
        
        # تطبيق φ
        phi_int = int(base_int * phi) % (2**256)
        
        # تحويل للتمثيل الستعشري
        return hex(phi_int)[2:].zfill(64)
    
    def _calculate_mirror_hash(self) -> str:
        """
        حساب التجزئة العكسية (المرآتية)
        
        للكتل في الاتجاه الخلفي، نستخدم φ² بدلاً من φ
        φ² = φ + 1 = 2.618...
        """
        if self.direction == "forward":
            return self.phi_hash
            
        # للاتجاه الخلفي: H_mirror(x) = φ² × SHA3-256(x) mod 2²⁵⁶
        phi_squared = float(golden_ratio(30)) ** 2
        data_bytes = self.data.encode('utf-8')
        base_hash = hashlib.sha3_256(data_bytes).digest()
        base_int = int.from_bytes(base_hash, 'big')
        
        mirror_int = int(base_int * phi_squared) % (2**256)
        return hex(mirror_int)[2:].zfill(64)
    
    def validate_symmetry(self, paired_block: 'ReversibleBlock') -> bool:
        """
        التحقق من التماثل الزمني بين كتلتين متقابلتين
        
        يجب أن يحققا: hash_forward × hash_backward ≈ φ mod 2²⁵⁶
        """
        if self.direction == paired_block.direction:
            return False
            
        forward_hash = self.phi_hash if self.direction == "forward" else paired_block.phi_hash
        backward_hash = self.mirror_hash if self.direction == "backward" else paired_block.mirror_hash
        
        # تحويل للتكامل
        forward_int = int(forward_hash, 16)
        backward_int = int(backward_hash, 16)
        
        # حساب النسبة (يجب أن تكون قريبة من φ)
        if backward_int == 0:
            return False
            
        ratio = forward_int / backward_int
        phi = float(golden_ratio(10))
        
        # هامش خطأ 0.1% (لأخطاء التقريب)
        return abs(ratio - phi) / phi < 0.001
    
    def __str__(self) -> str:
        return f"ReversibleBlock({self.direction[:3]}, data={self.data[:20]}..., hash={self.phi_hash[:16]}...)"


class TemporalChain:
    """السلسلة الزمنية المزدوجة الكاملة"""
    
    def __init__(self):
        self.forward_chain: List[ReversibleBlock] = []
        self.backward_chain: List[ReversibleBlock] = []
        self.genesis_hash = "0" * 64
        
    def add_block(self, data: str, direction: str = "forward") -> Tuple[ReversibleBlock, bool]:
        """
        إضافة كتلة جديدة للاتجاه المحدد
        
        يُرجع: (الكتلة المضافة, نجاح العملية)
        """
        # تحديد السلسلة المناسبة
        target_chain = self.forward_chain if direction == "forward" else self.backward_chain
        previous_hash = self.genesis_hash if not target_chain else target_chain[-1].phi_hash
        
        # إنشاء الكتلة
        block = ReversibleBlock(
            data=data,
            direction=direction,
            previous_hash=previous_hash
        )
        
        # التحقق من التماثل إذا كانت هناك كتلة مقابلة
        if direction == "forward" and self.backward_chain:
            paired_block = self.backward_chain[-1]
            if not block.validate_symmetry(paired_block):
                return None, False
        elif direction == "backward" and self.forward_chain:
            paired_block = self.forward_chain[-1]
            if not block.validate_symmetry(paired_block):
                return None, False
        
        # إضافة للسلسلة
        target_chain.append(block)
        return block, True
    
    def get_temporal_state(self, position: int = -1) -> dict:
        """
        الحصول على حالة زمنية محددة (للأمام والخلف)
        
        position: -1 لأحدث حالة، 0 للأولى، إلخ
        """
        if position < 0:
            forward = self.forward_chain[position] if self.forward_chain else None
            backward = self.backward_chain[position] if self.backward_chain else None
        else:
            forward = self.forward_chain[position] if position < len(self.forward_chain) else None
            backward = self.backward_chain[position] if position < len(self.backward_chain) else None
        
        return {
            "forward": forward,
            "backward": backward,
            "is_symmetric": self._check_symmetry_at_position(position)
        }
    
    def _check_symmetry_at_position(self, position: int) -> bool:
        """التحقق من التماثل في موقع معين"""
        if not self.forward_chain or not self.backward_chain:
            return False
            
        if position < 0:
            forward = self.forward_chain[position]
            backward = self.backward_chain[position]
        else:
            if position >= len(self.forward_chain) or position >= len(self.backward_chain):
                return False
            forward = self.forward_chain[position]
            backward = self.backward_chain[position]
        
        return forward.validate_symmetry(backward)
    
    def rewind(self, steps: int = 1) -> List[ReversibleBlock]:
        """
        التراجع الزمني (إلغاء آخر كتل)
        
        يُرجع: الكتل التي تمت إزالتها
        """
        removed = []
        for _ in range(steps):
            if self.forward_chain:
                removed.append(self.forward_chain.pop())
            if self.backward_chain:
                removed.append(self.backward_chain.pop())
        return removed
    
    def get_stats(self) -> dict:
        """إحصائيات السلسلة"""
        return {
            "forward_blocks": len(self.forward_chain),
            "backward_blocks": len(self.backward_chain),
            "total_blocks": len(self.forward_chain) + len(self.backward_chain),
            "symmetry_score": self._calculate_symmetry_score(),
            "temporal_balance": self._calculate_temporal_balance()
        }
    
    def _calculate_symmetry_score(self) -> float:
        """حساب درجة التماثل الكلي"""
        if not self.forward_chain or not self.backward_chain:
            return 0.0
            
        min_length = min(len(self.forward_chain), len(self.backward_chain))
        symmetric_count = 0
        
        for i in range(min_length):
            if self.forward_chain[i].validate_symmetry(self.backward_chain[i]):
                symmetric_count += 1
        
        return symmetric_count / min_length if min_length > 0 else 0.0
    
    def _calculate_temporal_balance(self) -> float:
        """حساب التوازن الزمني (يجب أن يكون قريبًا من φ)"""
        forward_len = len(self.forward_chain)
        backward_len = len(self.backward_chain)
        
        if backward_len == 0:
            return float('inf')
        
        ratio = forward_len / backward_len
        phi = float(golden_ratio(10))
        
        # الانحراف عن φ (نسبة مئوية)
        return abs(ratio - phi) / phi


# مثال تشغيلي
if __name__ == "__main__":
    print("🧪 اختبار النواة العكسية الزمنية")
    
    # إنشاء سلسلة
    chain = TemporalChain()
    
    # إضافة كتل أمامية
    chain.add_block("المعاملة 1: إنشاء", "forward")
    chain.add_block("المعاملة 2: تحويل", "forward")
    
    # إضافة كتل خلفية
    chain.add_block("الحالة العكسية 1", "backward")
    chain.add_block("الحالة العكسية 2", "backward")
    
    # عرض الإحصائيات
    stats = chain.get_stats()
    print(f"📊 إحصائيات السلسلة: {stats}")
    
    # التحقق من التماثل
    state = chain.get_temporal_state(-1)
    print(f"🔄 أحدث حالة: {'متماثلة' if state['is_symmetric'] else 'غير متماثلة'}")

