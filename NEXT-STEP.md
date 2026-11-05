# NEXT-STEP — পরের Session-এ কোথা থেকে শুরু

## পরের session-এ প্রথমে করবে

ব্যবহারকারী Python install ও `.env` setup করে নিচের commands চালাবেন:

```
cd "W:\Web Woks\My Wbsite\Learning App\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# .env ফাইল তৈরি করো (নির্দেশ নিচে আছে)
python manage.py makemigrations curriculum learning users
python manage.py migrate
python manage.py seed_curriculum
python manage.py createsuperuser
python manage.py runserver
```

## পরের session-এ আমার কাজ

1. Stage 1 Module 3 (Semantic HTML) — Day 06-07 পাঠ seed-এ যোগ করা
2. Stage 1 Module 4 (Forms) — Day 08-10
3. Stage 1 Module 5 (Tables & Meta) — Day 11-12
4. Stage 1 Projects — Day 13-15
5. ব্যবহারকারী যদি নেওয়ান: Neon setup ও ধাপ ২ শুরু
