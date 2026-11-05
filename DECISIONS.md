# DECISIONS — সিদ্ধান্ত ও কারণ

## 2026-11-05

### SQLite fallback যোগ করা হয়েছে
**সিদ্ধান্ত:** DATABASE_URL না থাকলে SQLite ব্যবহার করো।
**কারণ:** ব্যবহারকারী Neon setup করার আগেও locally test করতে পারবেন।

### ai_client.py-তে mock evaluation রাখা হয়েছে
**সিদ্ধান্ত:** Gemini API key না থাকলে mock response দাও।
**কারণ:** ধাপ ১-এ backend test করার সময় AI না থাকলেও submission flow test করা যাবে।

### Responsive Web App (React Vite) নির্বাচন
**সিদ্ধান্ত:** Native mobile app (React Native) নয়, Responsive Web App।
**কারণ:** ব্যবহারকারী এটি confirm করেছেন। Browser-এ চলে, install লাগে না, সহজ deploy।

### Django backend (FastAPI নয়)
**সিদ্ধান্ত:** App backend Django+DRF।
**কারণ:** CLAUDE.md-এ explicitly লেখা আছে। FastAPI curriculum-এ পরে শেখা হবে।

### Seed ফাইলে Day 01-05 রাখা হয়েছে প্রথম session-এ
**সিদ্ধান্ত:** পুরো Stage 0+1 (17 দিন) পরের session-এ সম্পূর্ণ করা হবে।
**কারণ:** ব্যবহারকারী বললেন "কিছু কাজ করে চালাতে দেখাবে" — তাই runnable state-এ রাখা হয়েছে।
