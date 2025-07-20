# 🔧 أدوات النسخ الاحتياطية - CARFAX Project

## 📋 نظرة عامة
أدوات متقدمة لإنشاء نسخ احتياطية من مشروع CARFAX مع تسمية تلقائية بالتاريخ والوقت.

## 🚀 الطرق المتاحة

### الطريقة الأولى: سكريبت Python
```bash
# تشغيل سكريبت Python
python backup_script.py
```

### الطريقة الثانية: سكريبت PowerShell (مُوصى به)
```powershell
# إنشاء نسخة احتياطية في المجلد الأب
.\backup.ps1

# إنشاء نسخة احتياطية في موقع محدد
.\backup.ps1 -Destination "C:\Backups"

# عرض المساعدة
.\backup.ps1 -Help
```

## ✨ المميزات

### 🎯 التسمية التلقائية
- تنسيق التاريخ: `YYYYMMDD_HHMMSS`
- مثال: `backup_20250719_230045`

### 🗂️ استبعاد الملفات غير الضرورية
- `__pycache__` - ملفات Python المؤقتة
- `.git` - مجلد Git
- `*.pyc`, `*.pyo` - ملفات Python المترجمة
- `*.log` - ملفات السجلات
- `node_modules` - مجلدات Node.js
- `.env`, `.venv`, `venv` - البيئات الافتراضية
- `.DS_Store`, `Thumbs.db` - ملفات النظام

### 📊 معلومات مفصلة
- حجم النسخة الاحتياطية
- عدد الملفات المنسوخة
- موقع النسخة الاحتياطية
- وقت إنشاء النسخة

## 📁 مواقع النسخ الاحتياطية

### النسخة الاحتياطية الافتراضية
```
C:\test\project\backup_YYYYMMDD_HHMMSS\
```

### النسخة الاحتياطية المخصصة
```
C:\Backups\backup_YYYYMMDD_HHMMSS\
```

## 🔧 التخصيص

### تعديل الملفات المستبعدة
يمكنك تعديل قائمة الملفات المستبعدة في السكريبتات:

**Python Script:**
```python
exclude_patterns = [
    '__pycache__',
    '.git',
    # أضف المزيد من الأنماط هنا
]
```

**PowerShell Script:**
```powershell
$excludePatterns = @(
    "__pycache__",
    ".git",
    # أضف المزيد من الأنماط هنا
)
```

### تغيير تنسيق التاريخ
**Python:**
```python
timestamp = now.strftime("%Y%m%d_%H%M%S")
```

**PowerShell:**
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
```

## 🛠️ استكشاف الأخطاء

### مشكلة: لا يمكن إنشاء النسخة الاحتياطية
```powershell
# تحقق من الصلاحيات
Get-Acl . | Format-List

# تحقق من المساحة المتاحة
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, FreeSpace
```

### مشكلة: خطأ في PowerShell
```powershell
# تفعيل تنفيذ السكريبتات
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# تشغيل PowerShell كمسؤول
Start-Process PowerShell -Verb RunAs
```

### مشكلة: خطأ في Python
```bash
# تثبيت المتطلبات
pip install pathlib

# تشغيل مع Python 3
python3 backup_script.py
```

## 📈 جدولة النسخ الاحتياطية

### باستخدام Task Scheduler (Windows)
1. افتح Task Scheduler
2. أنشئ مهمة جديدة
3. عيّن المسار: `powershell.exe`
4. عيّن المعاملات: `-File "C:\path\to\backup.ps1"`
5. عيّن الجدولة (يومياً، أسبوعياً، إلخ)

### باستخدام Cron (Linux/Mac)
```bash
# إضافة إلى crontab
0 2 * * * /usr/bin/python3 /path/to/backup_script.py
```

## 💡 نصائح مهمة

### 🔒 الأمان
- احتفظ بالنسخ الاحتياطية في موقع آمن
- استخدم التشفير للنسخ المهمة
- اختبر استعادة النسخ الاحتياطية بانتظام

### 💾 التخزين
- استخدم التخزين السحابي للنسخ المهمة
- احتفظ بنسخ متعددة في مواقع مختلفة
- احذف النسخ القديمة لتوفير المساحة

### ⏰ الجدولة
- أنشئ نسخ احتياطية يومية للمشاريع النشطة
- أنشئ نسخ أسبوعية للمشاريع المستقرة
- أنشئ نسخ قبل التحديثات الكبيرة

## 📞 الدعم

إذا واجهت أي مشاكل:
1. تحقق من الصلاحيات
2. تأكد من وجود مساحة كافية
3. تحقق من سجلات الأخطاء
4. اختبر السكريبت في مجلد تجريبي أولاً

---
**تم التطوير بـ ❤️ لحماية مشروعك** 🔒 