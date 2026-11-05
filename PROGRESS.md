# PROGRESS — Learning Mentor App

## ✅ সম্পন্ন (Session 1)

### ধাপ ১ — Backend ও Curriculum (আংশিক)
- [x] Project folder structure তৈরি
- [x] .gitignore, requirements.txt, .env.example
- [x] Django project: config/settings.py, urls.py, wsgi.py
- [x] Database models: Stage, Module, Lesson (curriculum app)
- [x] Database models: LessonProgress, Submission, Evaluation, SkillTracker, DailyLog (learning app)
- [x] Admin: curriculum ও learning app-এর admin.py
- [x] Serializers: curriculum ও learning
- [x] API Views: TodayLesson, SubmissionCreate, Progress, DailyLog
- [x] URL patterns: stages/, lessons/, today/, submissions/, progress/
- [x] Users app: LoginView (JWT)
- [x] ai_client.py (stub — Gemini integration ready, mock fallback আছে)
- [x] Seed command: Stage 0 (Day 01) + Stage 1 Module 1-2 (Day 02-05)
- [x] Render-এর জন্য Procfile ও build.sh

## 🔄 চলমান / বাকি

### ধাপ ১ — সম্পূর্ণ করতে হবে
- [ ] Stage 1 Module 3–5 ও Project-এর পাঠ seed করা (Day 06-17)
- [ ] Neon PostgreSQL সংযোগ ও migration চালানো
- [ ] superuser তৈরি ও admin-এ যাচাই

### ধাপ ২ — AI মূল্যায়ন
- [ ] Gemini API key সেট করে test submission
- [ ] ai_client.py পূর্ণাঙ্গ করা

### ধাপ ৩ — React Frontend
### ধাপ ৪ — Deployment

## 📊 Acceptance Criteria (ধাপ ১)
- [ ] লোকালে admin-এ Curriculum দেখা যায়
- [ ] Day 01 পাঠ সঠিকভাবে আছে
