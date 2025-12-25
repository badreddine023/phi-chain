"""
phi_math.py - اللبنة الرياضية الأساسية لـ Φ-Chain باستخدام الحسابات الصحيحة الثابتة
حساب φ (النسبة الذهبية) ومتتالية فيبوناتشي بدقة عالية بدون استخدام مكتبة Decimal.
"""

import math

class PhiMath:
    # استخدام عامل قياس كبير للحفاظ على الدقة (10^18 يشبه Wei في Ethereum)
    PRECISION_POWER = 18
    SCALE = 10 ** PRECISION_POWER
    
    @staticmethod
    def sqrt_int(n: int, precision: int = 18) -> int:
        """
        حساب الجذر التربيعي لعدد صحيح مع دقة ثابتة.
        sqrt(n) * 10^precision
        """
        if n < 0:
            raise ValueError("لا يمكن حساب الجذر التربيعي لعدد سالب")
        if n == 0:
            return 0
        
        # قياس n بـ 10^(2 * precision) للحصول على 10^precision في النتيجة
        scaled_n = n * (10**(2 * precision))
        
        # طريقة نيوتن للجذر التربيعي الصحيح
        x = scaled_n
        y = (x + 1) // 2
        while y < x:
            x = y
            y = (x + scaled_n // x) // 2
        return x

    @staticmethod
    def get_phi(precision: int = 18) -> int:
        """
        حساب النسبة الذهبية (φ) كعدد صحيح ثابت.
        φ = (1 + sqrt(5)) / 2
        يعيد φ * 10^precision
        """
        scale = 10**precision
        sqrt5 = PhiMath.sqrt_int(5, precision)
        phi = (scale + sqrt5) // 2
        return phi

    @staticmethod
    def get_phi_inv(precision: int = 18) -> int:
        """
        حساب مقلوب النسبة الذهبية (1/φ) كعدد صحيح ثابت.
        1/φ = φ - 1
        يعيد (1/φ) * 10^precision
        """
        phi = PhiMath.get_phi(precision)
        return phi - 10**precision

    @staticmethod
    def to_fixed(value: float, precision: int = 18) -> int:
        """تحويل قيمة عائمة إلى عدد صحيح ثابت."""
        return int(value * (10**precision))

    @staticmethod
    def from_fixed(value: int, precision: int = 18) -> float:
        """تحويل عدد صحيح ثابت إلى قيمة عائمة (للعرض فقط)."""
        return value / (10**precision)

def fibonacci(n: int) -> int:
    """
    حساب رقم فيبوناتشي مع دعم كامل للقيم السالبة (F(-n))
    """
    if n == 0:
        return 0
    if abs(n) <= 2:
        return 1 if n > 0 else (-1 if abs(n) % 2 == 0 else 1)
    
    a, b = 1, 1
    target = abs(n)
    for _ in range(3, target + 1):
        a, b = b, a + b
    
    result = b
    if n < 0:
        result *= (-1) ** (target + 1)
    
    return result

def generate_fibonacci_sequence(start: int, end: int) -> list:
    """إنشاء متتالية فيبوناتشي من start إلى end"""
    return [fibonacci(i) for i in range(start, end + 1)]

def is_fibonacci_number(num: int) -> bool:
    """التحقق إذا كان الرقم ينتمي لمتتالية فيبوناتشي"""
    if num < 0:
        return False
    test1 = 5 * num * num + 4
    test2 = 5 * num * num - 4
    return is_perfect_square(test1) or is_perfect_square(test2)

def is_perfect_square(n: int) -> bool:
    """التحقق إذا كان الرقم مربعًا كاملًا"""
    if n < 0:
        return False
    root = math.isqrt(n)
    return root * root == n

def phi_power(n: int, precision: int = 18) -> int:
    """
    حساب φ^n (قوة النسبة الذهبية) باستخدام الحسابات الثابتة.
    """
    phi = PhiMath.get_phi(precision)
    scale = 10**precision
    
    if n == 0:
        return scale
    if n < 0:
        # φ^-n = (1/φ)^n
        phi_inv = PhiMath.get_phi_inv(precision)
        result = scale
        for _ in range(abs(n)):
            result = (result * phi_inv) // scale
        return result
    
    result = scale
    for _ in range(n):
        result = (result * phi) // scale
    return result

if __name__ == "__main__":
    print("🔬 اختبار الوحدة الرياضية الأساسية لـ Φ-Chain (بدون Decimal)")
    phi = PhiMath.get_phi(10)
    print(f"φ (بدقة 10 منازل): {PhiMath.from_fixed(phi, 10)}")
    print(f"F(10) = {fibonacci(10)}")
    print(f"F(-10) = {fibonacci(-10)}")
    
    p5 = phi_power(5, 10)
    print(f"φ^5 = {PhiMath.from_fixed(p5, 10)}")
    
    seq = generate_fibonacci_sequence(1, 10)
    print(f"F(1..10) = {seq}")
