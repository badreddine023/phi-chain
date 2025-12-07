"""
اللبنة الرياضية الأساسية لـ Φ-Chain
حساب φ (النسبة الذهبية) ومتتالية فيبوناتشي مع دعم للزمن العكسي
"""

import math
from decimal import Decimal, getcontext

def fibonacci(n: int) -> int:
    """
    حساب رقم فيبوناتشي مع دعم كامل للقيم السالبة (F(-n))
    
    المعادلة: F(-n) = (-1)^(n+1) * F(n)
    """
    if n == 0:
        return 0
    if abs(n) <= 2:
        # F(1)=1, F(2)=1, F(-1)=1, F(-2)=-1
        return 1 if n > 0 else (-1 if abs(n) % 2 == 0 else 1)
    
    # حساب القيم الموجبة
    a, b = 1, 1
    target = abs(n)
    for _ in range(3, target + 1):
        a, b = b, a + b
    
    result = b
    # تطبيق الإشارة للقيم السالبة
    if n < 0:
        result *= (-1) ** (target + 1)
    
    return result

def golden_ratio(precision: int = 60) -> Decimal:
    """
    حساب النسبة الذهبية φ بدقة عالية
    
    φ = (1 + √5) / 2 ≈ 1.6180339887498948482...
    """
    getcontext().prec = precision + 10  # هامش أمان للدقة
    sqrt5 = Decimal(5).sqrt()
    phi = (Decimal(1) + sqrt5) / Decimal(2)
    
    # تقريب للدقة المطلوبة
    getcontext().prec = precision
    return +phi  # العمليات + تطبق الدقة الحالية

def generate_fibonacci_sequence(start: int, end: int) -> list:
    """
    إنشاء متتالية فيبوناتشي من start إلى end
    """
    return [fibonacci(i) for i in range(start, end + 1)]

def is_fibonacci_number(num: int) -> bool:
    """
    التحقق إذا كان الرقم ينتمي لمتتالية فيبوناتشي
    """
    if num < 0:
        return False
    
    # خاصية فيبوناتشي: 5n² ± 4 هو مربع كامل
    test1 = 5 * num * num + 4
    test2 = 5 * num * num - 4
    
    return is_perfect_square(test1) or is_perfect_square(test2)

def is_perfect_square(n: int) -> bool:
    """التحقق إذا كان الرقم مربعًا كاملًا"""
    if n < 0:
        return False
    root = int(math.isqrt(n))
    return root * root == n

def phi_power(n: int, precision: int = 30) -> Decimal:
    """
    حساب φ^n (قوة النسبة الذهبية)
    
    مهم لوزن المدققين في إجماع FBA: وزن ∝ φ^position
    """
    phi = golden_ratio(precision)
    getcontext().prec = precision + 10
    result = phi ** n
    getcontext().prec = precision
    return +result

def fibonacci_ratio(n: int) -> float:
    """
    حساب نسبة فيبوناتشي F(n+1)/F(n) التي تتقارب إلى φ
    """
    if n <= 0:
        return 0.0
    fn = fibonacci(n)
    fn1 = fibonacci(n + 1)
    return fn1 / fn if fn != 0 else 0.0

# اختبار سريع عند التشغيل المباشر
if __name__ == "__main__":
    print("🔬 اختبار الوحدة الرياضية الأساسية لـ Φ-Chain")
    print(f"φ (بدقة 10 منازل): {golden_ratio(10)}")
    print(f"F(10) = {fibonacci(10)}")
    print(f"F(-10) = {fibonacci(-10)}")
    print(f"F(15)/F(14) ≈ {fibonacci_ratio(14)} (يقترب من φ)")
    print(f"φ^5 = {phi_power(5, 10)}")
    
    # اختبار متتالية
    seq = generate_fibonacci_sequence(1, 10)
    print(f"F(1..10) = {seq}")
    
    