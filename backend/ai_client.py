"""
সব Gemini API call এই একটি ফাইলে থাকবে।
SDK-এর উপর নির্ভর না করে সরাসরি REST API ব্যবহার করা হচ্ছে।
"""
import io
import json
import mimetypes
import time
import logging
import base64
import requests as _requests
from django.conf import settings

logger = logging.getLogger(__name__)

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def _api_key():
    return settings.GEMINI_API_KEY or ''


FALLBACK_MODELS = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']


def _model():
    return settings.GEMINI_MODEL or 'gemini-2.5-flash'


def _generate(contents, max_retries=3):
    """Gemini REST API call — model unavailable হলে fallback করে।"""
    models_to_try = [_model()] + [m for m in FALLBACK_MODELS if m != _model()]

    for model in models_to_try:
        url = f"{GEMINI_BASE}/{model}:generateContent?key={_api_key()}"
        payload = {"contents": contents}

        for attempt in range(max_retries):
            try:
                resp = _requests.post(url, json=payload, timeout=60)
                if resp.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                if resp.status_code == 404:
                    # এই model নেই — পরের model চেষ্টা করো
                    break
                if not resp.ok:
                    err = resp.json() if resp.content else {}
                    msg = err.get('error', {}).get('message', resp.text[:200])
                    # model deprecated হলে পরেরটা চেষ্টা করো
                    if 'no longer available' in msg or 'deprecated' in msg.lower():
                        break
                    return None, f"AI error: {msg}"
                data = resp.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                return text, None
            except Exception as e:
                logger.error("Gemini REST error: %s", e)
                return None, str(e)

    return None, "Gemini API কাজ করছে না। Render-এ GEMINI_MODEL ও GEMINI_API_KEY যাচাই করো।"


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

**Rubric:** concept: ০–২০, independent_coding: ০–৩০, debugging: ০–২০, project_quality: ০–২০, explanation: ০–১০

নিচের JSON format-এ উত্তর দাও (অন্য কোনো text নয়):
{{"scores": {{"concept": 0, "independent_coding": 0, "debugging": 0, "project_quality": 0, "explanation": 0}}, "total": 0, "what_is_correct": ["..."], "what_is_wrong": ["..."], "hints": ["..."], "next_step": "...", "status": "In Progress | Needs Revision | Completed"}}"""


def evaluate_submission(lesson, submission, max_retries=3):
    """Text submission মূল্যায়ন করো।"""
    if not _api_key():
        return _mock_evaluation()

    prompt = EVALUATION_PROMPT.format(
        lesson_title=lesson.title,
        day_number=lesson.day_number,
        code=submission.code[:3000],
        explanation=submission.explanation[:500] if submission.explanation else "(কোনো ব্যাখ্যা দেওয়া হয়নি)",
    )

    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    raw, err = _generate(contents, max_retries)
    if err:
        return _error_evaluation(err)
    return _parse_eval(raw)


def evaluate_any_file(lesson, file_bytes, filename, explanation, max_retries=3):
    """যেকোনো ফাইল (image/PDF/audio/video) মূল্যায়ন করো — inline base64।"""
    if not _api_key():
        return _mock_evaluation()

    mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    b64 = base64.b64encode(file_bytes).decode('utf-8')

    prompt_text = f"""তুমি একজন Web Development Mentor। ফাইলটি দেখে মূল্যায়ন করো।

**পাঠ:** {lesson.title} (Day {lesson.day_number})
**ফাইল:** {filename}
**শিক্ষার্থীর ব্যাখ্যা:** {explanation or '(দেওয়া হয়নি)'}

Rubric: concept:০–২০, independent_coding:০–৩০, debugging:০–২০, project_quality:০–২০, explanation:০–১০

JSON format-এ উত্তর দাও:
{{"scores":{{"concept":0,"independent_coding":0,"debugging":0,"project_quality":0,"explanation":0}},"total":0,"what_is_correct":["..."],"what_is_wrong":["..."],"hints":["..."],"next_step":"...","status":"In Progress | Needs Revision | Completed"}}"""

    contents = [{
        "role": "user",
        "parts": [
            {"inline_data": {"mime_type": mime_type, "data": b64}},
            {"text": prompt_text},
        ],
    }]

    raw, err = _generate(contents, max_retries)
    if err:
        return _error_evaluation(err)
    return _parse_eval(raw)


def generate_daily_log(submissions):
    """আজকের submissions থেকে daily log তৈরি করো।"""
    if not submissions:
        return "আজকে কোনো submission করা হয়নি।"

    summary = "\n".join(
        f"- Day {s.lesson.day_number}: {s.lesson.title} — Score: "
        f"{getattr(s, 'evaluation', None) and s.evaluation.total_score or 'N/A'}%"
        for s in submissions
    )

    if not _api_key():
        from datetime import date
        return f"# Daily Log — {date.today()}\n\n{summary}\n"

    prompt = f"নিচের তথ্য দিয়ে একটি সংক্ষিপ্ত Daily Learning Report তৈরি করো (বাংলায়, Markdown):\n\n{summary}\n\nReport-এ: আজকের বিষয়, কী শিখেছি, দুর্বলতা, পরের পাঠ।"
    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    raw, err = _generate(contents)
    if err:
        from datetime import date
        return f"# Daily Log — {date.today()}\n\n{summary}\n"
    return raw


def _parse_eval(raw):
    try:
        text = raw.strip()
        if text.startswith("```"):
            parts = text.split("```")
            text = parts[1] if len(parts) > 1 else text
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text.strip())
        return _normalize_eval(data, raw)
    except json.JSONDecodeError:
        return _error_evaluation("AI-র উত্তর parse করা যায়নি।")


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
    return {
        'scores': {'concept': 15, 'independent_coding': 20, 'debugging': 15, 'project_quality': 15, 'explanation': 5},
        'total_score': 70,
        'what_is_correct': ['HTML structure ঠিক আছে।'],
        'what_is_wrong': ['Gemini API key সেট করা নেই — test mode চলছে।'],
        'hints': ['Render-এ GEMINI_API_KEY যোগ করো।'],
        'next_step': 'API key যোগ করো এবং আবার submit করো।',
        'status': 'In Progress',
        'raw_response': 'mock',
    }
