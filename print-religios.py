import csv
import os
from datetime import date, datetime, timedelta


# بدست آوردن مسیر دایرکتوری جاری
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'daily-event.csv')
audio_file_path = os.path.join(current_directory, 'azan.mp3')  # مسیر فایل صوتی

# خواندن اوقات شرعی امروز از فایل CSV
today_date = date.today().isoformat()

with open(file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['Date'] == today_date:
            print(f"اوقات شرعی امروز ({today_date}) کاشان:")
            print(f"اذان صبح: {row['Fajr']}")
            print(f"طلوع آفتاب: {row['Sunrise']}")
            print(f"اذان ظهر: {row['Dhuhr']}")
            print(f"اذان عصر: {row['Asr']}")
            
            # افزودن 2 دقیقه به زمان مغرب
            maghrib_time = row['Maghrib']
            maghrib_time_obj = datetime.strptime(maghrib_time, '%H:%M').time()
            new_maghrib_time = (datetime.combine(date.today(), maghrib_time_obj) + timedelta(minutes=2)).time()
            new_maghrib_time_str = new_maghrib_time.strftime('%H:%M')
            
            print(f"غروب آفتاب: {new_maghrib_time_str}")
            print(f"اذان مغرب: {new_maghrib_time_str}")
            print(f"اذان عشاء: {row['Isha']}")
            print(f"نیمه‌شب شرعی: {row['Midnight']}")
            

            break
    else:
        print("اطلاعات مربوط به امروز در فایل یافت نشد.")