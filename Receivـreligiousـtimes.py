import csv
import os
from datetime import date, timedelta
from praytimes import PrayTimes

# تنظیمات اولیه
location = (33.98, 51.43)  # مختصات جغرافیایی کاشان
timezone = 3.5  # منطقه زمانی ایران (GMT+3:30)
year = 2024

# ایجاد شیء PrayTimes با متد "Tehran" یا "Jafari"
# برای متد Tehran:
prayTimes = PrayTimes('Tehran')
# برای متد Jafari:
# prayTimes = PrayTimes('Jafari')

# بدست آوردن مسیر دایرکتوری جاری
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'daily-event.csv')

# محاسبه اوقات شرعی و ذخیره در فایل CSV برای دو سال متوالی
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Midnight'])
    
    start_date = date(year, 1, 1)
    end_date = date(year + 6, 12, 31)
    delta = timedelta(days=1)
    
    current_date = start_date
    while current_date <= end_date:
        times = prayTimes.getTimes(current_date, location, timezone)
        writer.writerow([
            current_date.isoformat(),
            times['fajr'],
            times['sunrise'],
            times['dhuhr'],
            times['asr'],
            times['maghrib'],
            times['isha'],
            times['midnight']
        ])
        current_date += delta

print('اوقات شرعی کاشان برای دو سال متوالی در فایل daily-event.csv ذخیره شد.')