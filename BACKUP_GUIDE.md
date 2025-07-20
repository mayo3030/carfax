# 🚀 دليل سريع للنسخ الاحتياطية

## 📁 مجلد `backup/`

جميع أدوات النسخ الاحتياطية موجودة في مجلد `backup/` منظم ومرتب.

## ⚡ الاستخدام السريع

### من المجلد الرئيسي:
```powershell
# الطريقة الأسهل
.\backup\backup_final.ps1

# أو باستخدام Python
python backup\backup_script.py
```

### من داخل مجلد backup:
```powershell
# انتقل إلى مجلد backup
cd backup

# استخدم السكريبت السريع
.\quick_backup.ps1

# أو استخدم أي سكريبت آخر
.\backup_final.ps1
```

## 📋 محتويات مجلد `backup/`

### 🎯 السكريبتات الموصى بها:
- **`backup_final.ps1`** - الأسهل والأسرع
- **`quick_backup.ps1`** - للاستخدام من داخل مجلد backup

### 🐍 سكريبتات Python:
- **`backup_script.py`** - متقدم ومفصل

### 💻 سكريبتات PowerShell:
- **`backup_ps.ps1`** - متوسط
- **`backup_simple.ps1`** - مفصل
- **`backup.ps1`** - متقدم

### 📚 ملفات التوثيق:
- **`README.md`** - دليل شامل
- **`BACKUP_README.md`** - دليل مفصل
- **`BACKUP_SUMMARY.md`** - ملخص نهائي

## ✨ المميزات

- **تسمية تلقائية** بالتاريخ والوقت
- **استبعاد الملفات غير الضرورية**
- **معلومات مفصلة** عن النسخة الاحتياطية
- **سهولة الاستخدام** من أي مكان

## 📁 موقع النسخ الاحتياطية
```
C:\test\project\backup_YYYYMMDD_HHMMSS\
```

## 💡 نصائح سريعة

1. **للاستخدام اليومي**: استخدم `backup_final.ps1`
2. **للتحكم المتقدم**: استخدم `backup_script.py`
3. **من داخل مجلد backup**: استخدم `quick_backup.ps1`

## 🔧 استكشاف الأخطاء

### مشكلة: لا يمكن تشغيل السكريبت
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### مشكلة: خطأ في المسار
```powershell
# تأكد من أنك في المجلد الصحيح
cd "C:\test\project\Project Carfax org - Copy"
```

---
**جميع الأدوات منظمة في مجلد `backup/` للسهولة والتنظيم** 📁✨ 