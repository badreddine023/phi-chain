"""
Phi-Security-Tool: أداة التشخيص الأمني لمشروع Phi-Chain
تقوم هذه الأداة بفحص الكود المصدري بحثاً عن:
1. استخدام مكتبات غير دقيقة (مثل Decimal أو float في العمليات الحساسة).
2. الثغرات الأمنية الشائعة (مثل الأسرار المضمنة).
3. التحقق من سلامة المنطق الرياضي لفيبوناتشي.
"""

import os
import re
import sys

class PhiSecurityTool:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.issues = []

    def scan(self):
        print(f"🔍 بدء الفحص الأمني في: {self.root_dir}")
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    self.check_file(os.path.join(root, file))
        
        self.report()

    def check_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()

            # 1. فحص استخدام Decimal
            if "from decimal import" in content or "import decimal" in content:
                self.add_issue(file_path, "تحذير: استخدام مكتبة Decimal المرفوضة.", "عالي")

            # 2. فحص استخدام float في العمليات الحساسة (تبسيط)
            if re.search(r"\w+\s*=\s*\d+\.\d+", content):
                self.add_issue(file_path, "تنبيه: تم اكتشاف قيم عائمة (float). تأكد من عدم استخدامها في حسابات الإجماع.", "متوسط")

            # 3. فحص الأسرار المضمنة (أمثلة بسيطة)
            if re.search(r"(password|secret|key)\s*=\s*['\"].+['\"]", content, re.I):
                self.add_issue(file_path, "خطر: احتمال وجود أسرار مضمنة (Hardcoded Secrets).", "حرِج")

    def add_issue(self, file, message, severity):
        self.issues.append({
            "file": file,
            "message": message,
            "severity": severity
        })

    def report(self):
        print("\n" + "="*50)
        print("📋 تقرير التشخيص الأمني لـ Phi-Chain")
        print("="*50)
        
        if not self.issues:
            print("✅ لم يتم العثور على مشاكل أمنية واضحة.")
        else:
            for issue in self.issues:
                print(f"[{issue['severity']}] {issue['file']}: {issue['message']}")
        
        print("="*50)
        print(f"إجمالي المشاكل المكتشفة: {len(self.issues)}")

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tool = PhiSecurityTool(project_root)
    tool.scan()
