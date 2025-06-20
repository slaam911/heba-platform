from django.core.management.base import BaseCommand
from users.models import City

# قائمة موسعة لأهم المدن والمحافظات السعودية مع المنطقة
SAUDI_CITIES = [
    ("الرياض", "الرياض"), ("الدرعية", "الرياض"), ("الخرج", "الرياض"), ("الدلم", "الرياض"), ("حوطة بني تميم", "الرياض"),
    ("الحريق", "الرياض"), ("الأفلاج", "الرياض"), ("السليل", "الرياض"), ("وادي الدواسر", "الرياض"), ("الزلفي", "الرياض"),
    ("شقراء", "الرياض"), ("حوطة سدير", "الرياض"), ("تمير", "الرياض"), ("مرات", "الرياض"), ("رماح", "الرياض"),
    ("ثادق", "الرياض"), ("المجمعة", "الرياض"), ("الغاط", "الرياض"), ("عفيف", "الرياض"), ("ضرما", "الرياض"),
    ("المزاحمية", "الرياض"), ("القويعية", "الرياض"), ("ساجر", "الرياض"), ("الدوادمي", "الرياض"), ("نفي", "الرياض"),
    ("جدة", "مكة المكرمة"), ("مكة المكرمة", "مكة المكرمة"), ("الطائف", "مكة المكرمة"), ("رابغ", "مكة المكرمة"),
    ("الجموم", "مكة المكرمة"), ("خليص", "مكة المكرمة"), ("الليث", "مكة المكرمة"), ("القنفذة", "مكة المكرمة"),
    ("أضم", "مكة المكرمة"), ("العرضيات", "مكة المكرمة"), ("المويه", "مكة المكرمة"), ("ميسان", "مكة المكرمة"),
    ("الخرمة", "مكة المكرمة"), ("رنية", "مكة المكرمة"), ("تربة", "مكة المكرمة"), ("المدينة المنورة", "المدينة المنورة"),
    ("ينبع", "المدينة المنورة"), ("العلا", "المدينة المنورة"), ("الحناكية", "المدينة المنورة"), ("المهد", "المدينة المنورة"),
    ("بدر", "المدينة المنورة"), ("خيبر", "المدينة المنورة"), ("العيص", "المدينة المنورة"), ("الدمام", "المنطقة الشرقية"),
    ("الخبر", "المنطقة الشرقية"), ("الظهران", "المنطقة الشرقية"), ("الجبيل", "المنطقة الشرقية"), ("القطيف", "المنطقة الشرقية"),
    ("صفوى", "المنطقة الشرقية"), ("سيهات", "المنطقة الشرقية"), ("رأس تنورة", "المنطقة الشرقية"), ("حفر الباطن", "المنطقة الشرقية"),
    ("الخفجي", "المنطقة الشرقية"), ("بقيق", "المنطقة الشرقية"), ("الأحساء", "المنطقة الشرقية"), ("الهفوف", "المنطقة الشرقية"),
    ("العمران", "المنطقة الشرقية"), ("الجفر", "المنطقة الشرقية"), ("تبوك", "تبوك"), ("ضباء", "تبوك"), ("الوجه", "تبوك"),
    ("أملج", "تبوك"), ("حقل", "تبوك"), ("تيماء", "تبوك"), ("البدع", "تبوك"), ("حائل", "حائل"), ("بقعاء", "حائل"),
    ("الغزالة", "حائل"), ("الشنان", "حائل"), ("الحائط", "حائل"), ("الشملي", "حائل"), ("موقق", "حائل"), ("الحليفة", "حائل"),
    ("الروضة", "حائل"), ("سميراء", "حائل"), ("عرعر", "الحدود الشمالية"), ("رفحاء", "الحدود الشمالية"), ("العويقيلة", "الحدود الشمالية"),
    ("طريف", "الحدود الشمالية"), ("جازان", "جازان"), ("أبو عريش", "جازان"), ("صامطة", "جازان"), ("صبيا", "جازان"), ("بيش", "جازان"),
    ("الدرب", "جازان"), ("الحرث", "جازان"), ("الريث", "جازان"), ("فيفاء", "جازان"), ("الدائر", "جازان"), ("العيدابي", "جازان"),
    ("العارضة", "جازان"), ("ضمد", "جازان"), ("أحد المسارحة", "جازان"), ("نجران", "نجران"), ("حبونا", "نجران"), ("بدر الجنوب", "نجران"),
    ("يدمة", "نجران"), ("ثار", "نجران"), ("خباش", "نجران"), ("شرورة", "نجران"), ("الخرخير", "نجران"), ("الباحة", "الباحة"),
    ("بلجرشي", "الباحة"), ("المندق", "الباحة"), ("المخواة", "الباحة"), ("قلوة", "الباحة"), ("العقيق", "الباحة"), ("الحجرة", "الباحة"),
    ("غامة بني هلال", "الباحة"), ("بني حسن", "الباحة"), ("سكاكا", "الجوف"), ("دومة الجندل", "الجوف"), ("طبرجل", "الجوف"),
    ("القريات", "الجوف"), ("بريدة", "القصيم"), ("عنيزة", "القصيم"), ("الرس", "القصيم"), ("البدائع", "القصيم"), ("البكيرية", "القصيم"),
    ("رياض الخبراء", "القصيم"), ("عقلة الصقور", "القصيم"), ("النبهانية", "القصيم"), ("الأسياح", "القصيم"), ("عيون الجواء", "القصيم"),
    ("الشماسية", "القصيم"), ("ضرية", "القصيم"), ("المذنب", "القصيم"), ("أبها", "عسير"), ("خميس مشيط", "عسير"), ("بيشة", "عسير"),
    ("النماص", "عسير"), ("محايل عسير", "عسير"), ("سراة عبيدة", "عسير"), ("تثليث", "عسير"), ("بلقرن", "عسير"), ("ظهران الجنوب", "عسير"),
    ("رجال ألمع", "عسير"), ("تنومة", "عسير"), ("المجاردة", "عسير"), ("الحرجة", "عسير"), ("المضة", "عسير"), ("البرك", "عسير")
]

class Command(BaseCommand):
    help = 'إضافة جميع مدن ومحافظات السعودية مع المنطقة إلى جدول City'

    def handle(self, *args, **kwargs):
        added = 0
        for name, region in SAUDI_CITIES:
            obj, created = City.objects.get_or_create(name=name, defaults={"region": region})
            if not obj.region:
                obj.region = region
                obj.save()
            if created:
                added += 1
        self.stdout.write(self.style.SUCCESS(f'تمت إضافة أو تحديث {added} مدينة/محافظة بنجاح.')) 