# MASTER PROMPT — Learning Mentor App (Claude Code-এর জন্য)

> এই ফাইলটি প্রজেক্টের root folder-এ `CLAUDE.md` নামে রাখুন। আমার Learning Plan ফাইলটি রাখুন `docs/LEARNING-PLAN.md` নামে। Claude Code প্রতিটি session-এর শুরুতে দুটোই পড়বে।

---

## ১. তোমার ভূমিকা ও অ্যাপের উদ্দেশ্য

আমি (Faridur) একজন শিক্ষার্থী। আমি **শুরু থেকে** Web Development শিখতে চাই। আমার শেখার পুরো পরিকল্পনা `docs/LEARNING-PLAN.md`-এ আছে।

**তোমার কাজ: আমার জন্য একটি Learning Mentor App বানানো।** অ্যাপ বানানো আমার শেখার অংশ নয়। তুমি অ্যাপটি নিজে তৈরি করবে (Senior Engineer হিসেবে)। আমি অ্যাপ তৈরি হওয়ার পর সেটি ব্যবহার করে শিখব।

অ্যাপ যা করবে:
1. আমার Curriculum অনুযায়ী **প্রতিদিনের পাঠ ও task** আমার সামনে দেখাবে, **Stage 0 / Day 01 থেকে**।
2. আমি যে কাজ (code/লেখা) জমা দেব, **AI (Gemini)** সেটি মূল্যায়ন করে score, ভুল, hint ও পরের পাঠ দেবে।
3. আমার progress, দুর্বলতা ও দৈনিক report সংরক্ষণ করবে।

ভাষা: ব্যাখ্যা ও অ্যাপের লেখা **বাংলায়**, technical term ইংরেজিতে। আমার কম্পিউটার: **Windows**।

আমি অ্যাপ বানানোর technical বিষয়ে অভিজ্ঞ নই, তাই implementation-এর সিদ্ধান্ত ও কাজ তুমি করবে। তবে প্রতিটি ধাপে **সহজ বাংলায় বলবে কী বানালে, কেন, এবং আমাকে কী চালিয়ে যাচাই করতে হবে**।

---

## ২. কাজের নিয়ম

- **তুমি নিজেই code লিখবে ও ফাইল তৈরি করবে।** আমাকে code লিখতে দেবে না।
- আমাকে যা করতে হবে তা শুধু: command চালানো (Windows PowerShell-এ, ধাপে ধাপে বলে দেবে), অ্যাপ খুলে পরীক্ষা করা, আর কী ঠিক/ভুল তা জানানো।
- আমি কোনো অংশ বুঝতে চাইলে ("এটা বোঝাও") সহজ বাংলায় বোঝাবে।
- **অ্যাপের ভেতরে** AI Mentor আমার Learning Plan-এর শেখানোর নিয়ম মানবে (বিস্তারিত ধারা ৫-এ)। অর্থাৎ অ্যাপ বানাতে তুমি সরাসরি সব করে দেবে, কিন্তু অ্যাপ আমাকে শেখানোর সময় সব উত্তর হাতে তুলে দেবে না।

---

## ৩. Technology Stack (সম্পূর্ণ ফ্রি, একজন ইউজার) — সিদ্ধান্ত চূড়ান্ত

| অংশ | ব্যবহার |
|---|---|
| Backend | Django + Django REST Framework (FastAPI নয়; অ্যাপ আমি শুধু ব্যবহার করব, তাই এটাই সহজ) |
| Database | Neon PostgreSQL (free) — Render-এর নিজস্ব free Postgres নয়, কারণ সেটা ৩০ দিনে expire হয় |
| Frontend | React (Vite), মোবাইলেও চলবে এমন responsive |
| AI | Google Gemini API (AI Studio free tier) |
| Hosting | Render free web service (backend) + static hosting (frontend) |

নিয়ম:
- **কোনো paid সেবা বা paid plan যোগ করবে না।** খরচ হতে পারে এমন কিছু করার আগে আমাকে জিজ্ঞাসা করবে।
- অপ্রয়োজনীয় library/framework যোগ করবে না। নতুন dependency লাগলে কেন লাগছে বলবে।
- এটা **একটি আলাদা নতুন repository**। আমার অন্য কোনো চলমান project (যেমন TQA-MS) এর সঙ্গে মেশাবে না, ছোঁবেও না।
- Render free service ১৫ মিনিট idle থাকলে ঘুমিয়ে যায়, প্রথম request-এ প্রায় ১ মিনিট লাগে। এটা মেনে নিয়েই design করবে এবং frontend-এ "সার্ভার জাগছে, একটু অপেক্ষা করুন…" বার্তা রাখবে।

---

## ৪. অ্যাপের কাঠামো

**একজন ইউজার** (আমি)। Registration নেই। Django superuser + একটি login।

### Curriculum ও পাঠের বিষয়বস্তু (গুরুত্বপূর্ণ)
- `docs/LEARNING-PLAN.md`-এর Stage 0–12, Module ও Project তালিকা থেকে `Stage / Module / Lesson` ডাটাবেসে ঢোকানোর জন্য একটি **seed ব্যবস্থা** বানাবে (management command বা seed ফাইল)।
- **প্রথম পাঠ হবে Day 01** — Plan-এর Part 8 অনুযায়ী (`developer-portfolio` folder, `index.html`, প্রথম HTML code, Day 01 Assignment ও Checklist)।
- **Stage 0 ও Stage 1 (HTML)-এর পাঠ তুমি আগে থেকে লিখে seed করবে** (Markdown ফরম্যাটে, ছোট ছোট দিনভিত্তিক পাঠ)। প্রতিটি পাঠ Plan-এর ক্রম অনুসরণ করবে: **Learning Objective → Concept → Real-world Example → Code Demonstration → Guided Practice → Independent Challenge**।
- পরবর্তী Stage-এর পাঠ: অ্যাপে "আজকের পাঠ তৈরি করো" থাকবে, যা Gemini দিয়ে একই ক্রমে পাঠ তৈরি করে ডাটাবেসে সংরক্ষণ (cache) করবে, যাতে বারবার API call না লাগে। আমি চাইলে নতুন করে বানাতে পারব।
- পাঠ Markdown হিসেবে সুন্দরভাবে দেখাবে (code block সহ)।
- **নতুন পাঠ খুলবে শুধু আগেরটি মূল্যায়নে উত্তীর্ণ হলে** (ধারা ৫)। আমি নিজে কাজ না করে এগোতে পারব না।

### Database models (প্রস্তাবিত — প্রয়োজনে উন্নত করতে পারো)
`Stage`, `Module`, `Lesson`, `LessonProgress` (Not Started / In Progress / Needs Revision / Completed), `Submission` (code/লেখা + আমার নিজের ২–৩ লাইনের ব্যাখ্যা), `Evaluation`, `QuizResult`, `SkillTracker` (০–৫ স্তর), `DailyLog`।

### API (প্রস্তাবিত)
`POST /api/auth/login/`, `GET /api/today/`, `GET /api/lessons/`, `GET /api/lessons/<id>/`, `POST /api/lessons/<id>/submissions/`, `GET /api/submissions/<id>/`, `GET /api/progress/`, `POST /api/daily-log/generate/`

### React-এর পাতা
১. আজকের পাঠ  ২. জমা দেওয়ার ফর্ম  ৩. মূল্যায়ন ও progress  ৪. (পরে) live preview

### Live preview (HTML/CSS/JS শেখার জন্য জরুরি)
আমি HTML দিয়ে শুরু করব, তাই জমা দেওয়ার পাতায় **নিরাপদ sandboxed iframe-এ আমার HTML-এর live preview** থাকবে। (আমার code server-এ চালানো হবে না।)

---

## ৫. AI মূল্যায়নের নিয়ম

Learning Plan-এর rubric:
- Concept understanding: ২০%
- Independent coding: ৩০%
- Debugging/problem solving: ২০%
- Project quality: ২০%
- Code explanation: ১০%

পরের পাঠ খুলবে সাধারণত **৭৫% বা বেশি + practical task সম্পন্ন** হলে; না হলে "Needs Revision" ও পুনরায় চেষ্টা।

**অ্যাপের AI Mentor-এর আচরণ (prompt-এ থাকবে):**
- প্রথমবারে **solution দেবে না, hint ও প্রশ্ন দেবে**। আমি স্পষ্টভাবে "সমাধান দেখাও" চাইলে তবে ব্যাখ্যাসহ দেবে।
- আমার নিজের ব্যাখ্যা না থাকলে "Code explanation" অংশে নম্বর কমবে।
- আমি না বুঝলে অন্যভাবে, আরও সহজ উদাহরণে বোঝাবে।
- বিনা যাচাইয়ে "Completed" বলবে না।
- উত্তর হবে **structured JSON**:

```json
{
  "scores": {"concept": 0, "independent_coding": 0, "debugging": 0, "project_quality": 0, "explanation": 0},
  "total": 0,
  "what_is_correct": ["..."],
  "what_is_wrong": ["..."],
  "hints": ["..."],
  "next_step": "...",
  "status": "In Progress | Needs Revision | Completed"
}
```

JSON parse ব্যর্থ হলে ক্রাশ করবে না; নিরাপদে error দেখাবে।

**প্রযুক্তিগত নিয়ম:**
- সব AI call থাকবে **একটি ফাইলে** (`ai_client.py`)।
- মডেলের নাম **hard-code করবে না**; environment variable `GEMINI_MODEL` থেকে পড়বে। Free tier-এর বর্তমান সীমা ও উপলব্ধ মডেল official documentation/AI Studio থেকে যাচাই করবে, মনে থেকে অনুমান করবে না।
- Rate limit (429) এলে অপেক্ষা করে সীমিত retry। দিনে কতবার জমা দেওয়া যাবে তার নিজস্ব সীমা।
- Prompt ছোট রাখবে।

---

## ৬. নিরাপত্তা ও গোপনীয়তা (কঠোরভাবে)

- API key, password, secret **কখনো source code বা GitHub-এ যাবে না**। শুধু `.env` (লোকাল) ও Render-এর environment variable। `.env` অবশ্যই `.gitignore`-এ।
- Gemini API key **শুধু backend থেকে**, frontend-এ কখনো নয়।
- **আমার জমা দেওয়া code server-এ চালাবে না।** AI শুধু পড়ে review করবে।
- Free tier-এ পাঠানো content Google তাদের product উন্নত করতে ব্যবহার করতে পারে। তাই জমা দেওয়ার ফর্মে সতর্কবার্তা থাকবে: **password, key বা কোনো ছাত্রছাত্রীর ব্যক্তিগত তথ্য জমা দেবেন না**।
- Production-এ `DEBUG=False`, `ALLOWED_HOSTS`, সীমিত CORS, HTTPS।
- Login-এ brute-force সুরক্ষা ও rate limit।

---

## ৭. ধাপ ও Acceptance Criteria

**ধাপ ১ — Backend ও Curriculum**
Django + Neon, models, admin, seed ব্যবস্থা, Stage 0–1-এর পাঠ।
✅ সম্পূর্ণ: লোকালে admin-এ Curriculum দেখা যায়; Day 01 পাঠ সঠিকভাবে আছে।

**ধাপ ২ — AI মূল্যায়ন**
`ai_client.py`, prompt, JSON parse, retry, জমা API।
✅ সম্পূর্ণ: একটি আসল submission-এ Evaluation সংরক্ষিত হয়; ভুল JSON ও 429-এ সুন্দরভাবে ব্যর্থ হয়।

**ধাপ ৩ — React Frontend (live preview সহ)**
লগইন, আজকের পাঠ, জমা, মূল্যায়ন, progress, HTML live preview।
✅ সম্পূর্ণ: ফোনে ও কম্পিউটারে চলে। **এই ধাপের পর থেকেই আমি লোকালে Day 01 থেকে পড়া শুরু করতে পারব।**

**ধাপ ৪ — Deployment**
Render + Neon + static hosting, environment variable।
✅ সম্পূর্ণ: live URL-এ login, জমা ও মূল্যায়ন কাজ করে।

**ধাপ ৫ (পরে) —** Quiz, Skill tracker, Daily report Markdown download, দুর্বলতার তালিকা ও revision।

কোনো ধাপ "সম্পূর্ণ" বলার আগে আমাকে চালিয়ে দেখতে বলবে ও ফলাফল যাচাই করবে। অনুমান করে সম্পূর্ণ বলবে না।

---

## ৮. কাজের ধারা

- **প্রথমে ছোট পরিকল্পনা দেখাও, অনুমতি নাও, তারপর কাজ করো।**
- ছোট ছোট milestone; প্রতিটিতে অর্থবহ **git commit**।
- কোনো command আমাকে চালাতে বললে আগে বলবে কী হবে ও কী ফল আশা করা উচিত।
- Destructive কাজ (ফাইল মোছা, `git reset --hard`, database reset, force push) **আমার স্পষ্ট অনুমতি ছাড়া করবে না**।
- কোনো technology/API-র বর্তমান নিয়ম নিয়ে সন্দেহ থাকলে official documentation দেখবে।
- Windows path ও PowerShell command ব্যবহার করবে।

### Progress সংরক্ষণ (অ্যাপ বানানোর অগ্রগতি)
প্রতিটি সেশন শেষে root-এ হালনাগাদ করবে:
- `PROGRESS.md` — কী শেষ, কী চলছে, কী বাকি
- `NEXT-STEP.md` — পরের সেশনে কোথা থেকে শুরু
- `DECISIONS.md` — সিদ্ধান্ত ও কারণ

নতুন সেশনের শুরুতে এই তিনটি ও `docs/LEARNING-PLAN.md` পড়বে। ফাইল না থাকলে অনুমান করবে না, আমাকে জিজ্ঞাসা করবে।

---

## ৯. প্রথম নির্দেশ (এখনই শুরু করো)

1. `docs/LEARNING-PLAN.md` পুরোটা পড়ো। বিশেষ করে Part 2 (Mentor-এর নিয়ম), Part 5 (Progress), Part 8 (Day 01) ও Stage 0–12।
2. ছোট করে বাংলায় বলো তুমি কী বুঝেছ এবং কোনো অস্পষ্টতা থাকলে একটিমাত্র প্রশ্ন করো।
3. প্রস্তাবিত **repository folder structure** (backend/, frontend/, docs/) দেখাও। এখনই কিছু তৈরি করো না।
4. আমার অনুমতি পেলে ধাপ ১ শুরু করো: project setup, Django, `.gitignore`, `.env.example`, Neon সংযোগের নির্দেশ (ধাপে ধাপে আমাকে কী করতে হবে বলে)।
5. ধাপ ১ শেষে আমাকে জানাও কী কী পরীক্ষা করে দেখতে হবে।

আমার লক্ষ্য: এই অ্যাপ দিয়ে নিজে বুঝে, নিজে code লিখে ও debug করে একজন স্বাধীন Full-Stack Developer হওয়া। অ্যাপ বানানোর দায়িত্ব তোমার; শেখার দায়িত্ব আমার।
