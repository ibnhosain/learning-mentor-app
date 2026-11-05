"""
সব Gemini API call এই একটি ফাইলে থাকবে।
ধাপ ২-এ এটি পূর্ণাঙ্গ করা হবে।
"""
import json
import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    _model = genai.GenerativeModel(settings.GEMINI_MODEL)
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False
    _model = None


EVALUATION_PROMPT = """তুমি একজন Web Development Mentor। একজন Beginner শিক্ষার্থীর কাজ মূল্যায়ন করো।

**পাঠ:** {lesson_title} (Day {day_number})

**শিক্ষার্থীর কাজ:**
{code}

**শিক্ষার্থীর ব্যাখ্যা:**
{explanation}

**মূল্যায়নের নিয়ম:**
- প্রথমবারে সরাসরি solution দেবে না — hint ও প্রশ্ন দেবে।
- ব্যাখ্যা না থাকলে explanation score শূন্য।
- ৭৫% বা বেশি এবং practical task সম্পন্ন হলে "Completed"।

**Rubric:**
- concept: ০–২০
- independent_coding: ০–৩০
- debugging: ০–২০
- project_quality: ০–২০
- explanation: ০–১০

নিচের JSON format-এ উত্তর দাও (অন্য কোনো text নয়):
{{
  "scores": {{"concept": 0, "independent_coding": 0, "debugging": 0, "project_quality": 0, "explanation": 0}},
  "total": 0,
  "what_is_correct": ["..."],
  "what_is_wrong": ["..."],
  "hints": ["..."],
  "next_step": "...",
  "status": "In Progress | Needs Revision | Completed"
}}"""


def evaluate_submission(lesson, submission, max_retries=3):
    """Submission মূল্যায়ন করো। ব্যর্থ হলে None return করো।"""
    if not GEMINI_AVAILABLE or not settings.GEMINI_API_KEY:
        logger.warning("Gemini API available নয়।")
        return _mock_evaluation()

    prompt = EVALUATION_PROMPT.format(
        lesson_title=lesson.title,
        day_number=lesson.day_number,
        code=submission.code[:3000],  # prompt ছোট রাখো
        explanation=submission.explanation[:500] if submission.explanation else "(কোনো ব্যাখ্যা দেওয়া হয়নি)",
    )

    for attempt in range(max_retries):
        try:
            response = _model.generate_content(prompt)
            raw = response.text.strip()
            # Markdown code block সরাও যদি থাকে
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw)
            return _normalize_eval(data, raw)
        except json.JSONDecodeError:
            logger.error("Gemini JSON parse ব্যর্থ: %s", raw[:200])
            return _error_evaluation("AI-র উত্তর parse করা যায়নি।")
        except Exception as e:
            err_str = str(e)
            if '429' in err_str or 'quota' in err_str.lower():
                wait = 2 ** attempt
                logger.warning("Rate limit — %ds অপেক্ষা করছি...", wait)
                time.sleep(wait)
            else:
                logger.error("Gemini error: %s", err_str)
                return _error_evaluation(f"AI error: {err_str[:100]}")

    return _error_evaluation("Rate limit — পরে আবার চেষ্টা করো।")


def generate_daily_log(submissions):
    """আজকের submissions থেকে daily log তৈরি করো।"""
    if not submissions:
        return "আজকে কোনো submission করা হয়নি।"

    summary = "\n".join(
        f"- Day {s.lesson.day_number}: {s.lesson.title} — Score: "
        f"{getattr(s, 'evaluation', None) and s.evaluation.total_score or 'N/A'}%"
        for s in submissions
    )

    if not GEMINI_AVAILABLE or not settings.GEMINI_API_KEY:
        from datetime import date
        return f"# Daily Log — {date.today()}\n\n## আজকের কাজ\n{summary}\n"

    prompt = f"""নিচের তথ্য দিয়ে একটি সংক্ষিপ্ত Daily Learning Report তৈরি করো (বাংলায়, Markdown format-এ):

{summary}

Report-এ থাকবে: আজকের বিষয়, কী শিখেছি, দুর্বলতা, পরের পাঠ।"""

    try:
        response = _model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error("Daily log generate ব্যর্থ: %s", e)
        from datetime import date
        return f"# Daily Log — {date.today()}\n\n{summary}\n"


def _normalize_eval(data, raw):
    scores = data.get('scores', {})
    total = data.get('total', sum(scores.values()))
    return {
        'scores': scores,
        'total_score': min(100, max(0, int(total))),
        'what_is_correct': data.get('what_is_correct', []),
        'what_is_wrong': data.get('what_is_wrong', []),
        'hints': data.get('hints', []),
        'next_step': data.get('next_step', ''),
        'status': data.get('status', 'In Progress'),
        'raw_response': raw,
    }


def _error_evaluation(message):
    return {
        'scores': {'concept': 0, 'independent_coding': 0, 'debugging': 0, 'project_quality': 0, 'explanation': 0},
        'total_score': 0,
        'what_is_correct': [],
        'what_is_wrong': [message],
        'hints': ['একটু পরে আবার জমা দিয়ে চেষ্টা করো।'],
        'next_step': '',
        'status': 'In Progress',
        'raw_response': message,
    }


def _mock_evaluation():
    """Gemini API না থাকলে test-এর জন্য।"""
    return {
        'scores': {'concept': 15, 'independent_coding': 20, 'debugging': 15, 'project_quality': 15, 'explanation': 5},
        'total_score': 70,
        'what_is_correct': ['HTML structure ঠিক আছে।'],
        'what_is_wrong': ['Gemini API key সেট করা নেই — এটি test mode।'],
        'hints': ['.env ফাইলে GEMINI_API_KEY যোগ করো।'],
        'next_step': 'API key যোগ করো এবং আবার submit করো।',
        'status': 'In Progress',
        'raw_response': 'mock',
    }
