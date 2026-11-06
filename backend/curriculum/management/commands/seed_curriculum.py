"""
Seed command — Stage 0 ও Stage 1 (HTML)-এর পাঠ database-এ ঢোকায়।
Idempotent: data থাকলে skip করে।

চালানোর পদ্ধতি:
  python manage.py seed_curriculum
  python manage.py seed_curriculum --clear   (সব মুছে নতুন করে)
"""
from django.core.management.base import BaseCommand
from curriculum.models import Stage, Module, Lesson

# ════════════════════════════════════════════════════════
# LESSON CONTENT — Markdown, Bengali + English mixed
# ════════════════════════════════════════════════════════

DAY01_CONTENT = """## 🎯 আজকের লক্ষ্য (Learning Objective)

আজ তুমি শিখবে:
- কম্পিউটারে একটি web project folder কীভাবে তৈরি করতে হয়
- VS Code-এ folder কীভাবে খুলতে হয়
- প্রথম HTML ফাইল তৈরি ও browser-এ দেখতে হয়

**কেন শিখব?** প্রতিটি web project একটি folder থেকে শুরু হয়। আজ তুমি যে folder তৈরি করবে, সেটিই তোমার "developer-portfolio" — তোমার প্রথম real project!

---

## 📖 Concept

**HTML কী?**

HTML-এর পূর্ণরূপ **HyperText Markup Language**। এটি কোনো programming language নয় — এটি একটি **markup language**।

তুমি যখন কোনো ওয়েবসাইট দেখো, সেই পাতার "কাঠামো" বা structure তৈরি হয় HTML দিয়ে।

মনে করো একটি বাড়ি বানাচ্ছো:
- **HTML** = বাড়ির কাঠামো (দেয়াল, ছাদ, দরজা)
- **CSS** = রঙ, সজ্জা, ডিজাইন (পরে শিখব)
- **JavaScript** = বাড়ির কার্যকারিতা যেমন আলো জ্বালা, দরজা খোলা (পরে শিখব)

---

## 🌍 Real-world Example

তুমি এখন যে browser-এ ওয়েবসাইট দেখছো, সেটি HTML ফাইল পড়ে সুন্দর করে দেখাচ্ছে। Facebook, YouTube, Wikipedia — সবকিছুর ভিত্তিতে HTML আছে।

Browser-এ যেকোনো পাতায় **Right Click → "View Page Source"** চাপলে সেই পাতার HTML কোড দেখতে পাবে।

---

## 💻 Code Demonstration

প্রথম HTML ফাইল এরকম দেখতে:

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
</head>

<body>
    <h1>Welcome to My Portfolio</h1>
    <p>I am learning Web Development.</p>
</body>

</html>
```

**প্রতিটি অংশ কী করে:**
| Tag | কাজ |
|-----|-----|
| `<!DOCTYPE html>` | Browser-কে বলে "এটি HTML5 ফাইল" |
| `<html>` | পুরো পাতার শুরু ও শেষ |
| `<head>` | পাতার তথ্য (screen-এ দেখায় না) |
| `<title>` | Browser-এর tab-এ যা দেখায় |
| `<body>` | যা screen-এ দেখায় |
| `<h1>` | সবচেয়ে বড় Heading |
| `<p>` | Paragraph |

---

## 🤝 Guided Practice

**ধাপে ধাপে করো:**

1. Desktop-এ বা যেকোনো সুবিধাজনক জায়গায় নতুন folder তৈরি করো, নাম দাও: `developer-portfolio`
2. VS Code খোলো
3. File → Open Folder → `developer-portfolio` folder select করো
4. VS Code-এর বাম Explorer panel-এ folder দেখতে পাবে
5. New File বোতামে click করো, নাম দাও: `index.html`
6. উপরের Code Demonstration-এর code **নিজে টাইপ করো** (copy করো না!)
7. Ctrl+S দিয়ে save করো
8. `index.html` ফাইলটি browser-এ drag করো অথবা VS Code-এ Live Server extension থাকলে সেটি ব্যবহার করো

---

## 🏆 Independent Challenge

এখন **নিজে থেকে** করো (hint ছাড়া):

1. `<h1>` tag-এর ভেতরের লেখা পরিবর্তন করো — তোমার নিজের **নাম** লেখো
2. `<p>` tag-এ তোমার নিজের **পরিচয়** লেখো
3. নতুন একটি `<p>` tag যোগ করো — কেন web developer হতে চাও তা লেখো
4. আরেকটি `<p>` tag যোগ করো — তোমার learning goal লেখো
5. Save করো এবং browser-এ refresh করো

**সফলতার চিহ্ন:** Browser-এ তোমার নাম ও পরিচয় দেখা যাচ্ছে।

---

## ✅ Day 01 Checklist

- [ ] `developer-portfolio` folder তৈরি হয়েছে
- [ ] VS Code-এ folder open হয়েছে
- [ ] `index.html` ফাইল তৈরি হয়েছে
- [ ] HTML code নিজে টাইপ করেছো (copy নয়)
- [ ] Browser-এ page দেখা যাচ্ছে
- [ ] নিজের নাম ও পরিচয় যোগ করেছো
- [ ] Learning goal লিখেছো

---

## 📝 জমা দেওয়ার নির্দেশ

তোমার `index.html`-এর **সম্পূর্ণ code** এই পাতায় paste করো এবং নিচের প্রশ্নগুলোর উত্তর দাও:

1. `<!DOCTYPE html>` কেন লিখতে হয়?
2. `<head>` ও `<body>`-এর মধ্যে পার্থক্য কী?
3. তুমি কোন অংশটি বুঝতে পারোনি বা কঠিন মনে হয়েছে?

> ⚠️ **সতর্কতা:** জমা দেওয়ার সময় কোনো password, API key বা ব্যক্তিগত তথ্য লিখবে না।
"""

DAY02_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- HTML document structure-এর প্রতিটি অংশ গভীরভাবে বুঝতে
- `<head>`-এর ভেতরে কী থাকে ও কেন লাগে
- Attribute কী এবং কীভাবে ব্যবহার করতে হয়

**কেন গুরুত্বপূর্ণ?** এই ভিত্তিগত জ্ঞান না থাকলে পরবর্তী সব বিষয় কঠিন হয়ে যাবে।

---

## 📖 Concept

### HTML Element vs Tag

**Tag** হলো `<html>` বা `</html>` — angle bracket দিয়ে ঘেরা।

**Element** হলো opening tag + content + closing tag মিলে:
```
<p>এটি একটি paragraph।</p>
```
- `<p>` = opening tag
- `এটি একটি paragraph।` = content
- `</p>` = closing tag

### Self-closing Tags

কিছু tag-এর closing tag নেই:
```html
<meta charset="UTF-8">
<br>
<img src="photo.jpg" alt="ছবি">
```

### Attribute

Tag-এর ভেতরে **attribute** দিয়ে অতিরিক্ত তথ্য দেওয়া হয়:
```html
<html lang="bn">
       ^^^  ^^^^
       name  value
```

---

## 🌍 Real-world Example

`<meta charset="UTF-8">` না থাকলে বাংলা, আরবি বা চীনা অক্ষর ভুল দেখাবে। আর `<meta name="viewport">` না থাকলে মোবাইলে ওয়েবসাইট ছোট হয়ে দেখাবে।

---

## 💻 Code Demonstration

```html
<!DOCTYPE html>
<html lang="bn">

<head>
    <!-- Character encoding — বাংলাসহ সব ভাষার জন্য জরুরি -->
    <meta charset="UTF-8">

    <!-- Mobile-এ সঠিক size-এ দেখানোর জন্য -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Search engine-এ যা দেখায় -->
    <meta name="description" content="Faridur-এর portfolio — Web Developer">

    <!-- Browser tab-এ title -->
    <title>Faridur | Web Developer</title>
</head>

<body>
    <h1>আমার Portfolio</h1>
    <p>আমি Web Development শিখছি।</p>
</body>

</html>
```

**Comment কী?**
`<!-- এটি একটি comment -->` — browser এটি দেখায় না, শুধু code পড়ার সময় বোঝার জন্য লেখা হয়।

---

## 🤝 Guided Practice

তোমার Day 01-এর `index.html` খোলো এবং:

1. `<html lang="en">` পরিবর্তন করে `<html lang="bn">` করো (কারণ তোমার content বাংলায়)
2. `<meta name="description">` যোগ করো তোমার নিজের বর্ণনা দিয়ে
3. `<title>` পরিবর্তন করো তোমার নামে
4. `<body>`-এর ভেতরে দুটি comment যোগ করো বাংলায়

---

## 🏆 Independent Challenge

একটি নতুন ফাইল তৈরি করো `about.html` নামে। সেখানে:
- Proper HTML structure থাকবে (DOCTYPE, html, head, body)
- `<title>` হবে "আমার সম্পর্কে"
- `<body>`-তে তোমার পরিচয়, শখ ও লক্ষ্য থাকবে
- অন্তত দুটি comment থাকবে

---

## 📝 জমা দেওয়ার নির্দেশ

`index.html` ও `about.html` দুটির code জমা দাও এবং ব্যাখ্যা করো:
1. `lang="bn"` কেন দিয়েছো?
2. `viewport` meta tag না থাকলে কী সমস্যা হতো?
3. Comment কোন কাজে লাগে?
"""

DAY03_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- Heading (h1–h6) এবং কখন কোনটি ব্যবহার করবে
- Paragraph এবং line break
- Text formatting: bold, italic, underline
- HTML entities (বিশেষ চিহ্ন)

---

## 📖 Concept

### Headings: h1 থেকে h6

```html
<h1>সবচেয়ে বড় — শুধু একটি page-এ একবার</h1>
<h2>দ্বিতীয় স্তর — section heading</h2>
<h3>তৃতীয় স্তর — subsection</h3>
<h4>চতুর্থ স্তর</h4>
<h5>পঞ্চম স্তর</h5>
<h6>সবচেয়ে ছোট</h6>
```

**গুরুত্বপূর্ণ নিয়ম:** একটি পাতায় শুধু **একটি** `<h1>` থাকবে। এটি SEO ও accessibility-র জন্য জরুরি।

### Paragraph ও Line Break

```html
<p>এটি একটি paragraph। Browser এটিকে আলাদা block হিসেবে দেখায়।</p>

<p>এটি দ্বিতীয় paragraph।<br>এই line-এ br দিয়ে শুধু line break করা হয়েছে।</p>
```

### Text Formatting

```html
<strong>এটি গুরুত্বপূর্ণ — bold দেখায়</strong>
<em>এটি জোর দিয়ে বলা — italic দেখায়</em>
<mark>এটি highlight করা</mark>
<del>এটি মুছে ফেলা হয়েছে</del>
<small>এটি ছোট text</small>
```

---

## 🌍 Real-world Example

Wikipedia-র প্রতিটি article-এ `<h1>` হলো article-এর নাম, `<h2>` হলো প্রধান section, `<h3>` হলো subsection। এই hierarchy না থাকলে screen reader ব্যবহারকারীরা navigate করতে পারতেন না।

---

## 💻 Code Demonstration

```html
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>আমার Portfolio</title>
</head>
<body>
    <h1>Faridur Rahman</h1>

    <h2>আমার সম্পর্কে</h2>
    <p>আমি একজন <strong>Web Development</strong> শিক্ষার্থী।
    আমার লক্ষ্য একজন <em>Full-Stack Developer</em> হওয়া।</p>

    <h2>আমার লক্ষ্য</h2>
    <p>এই বছর আমি HTML, CSS ও JavaScript শিখব।</p>

    <h3>স্বল্পমেয়াদী লক্ষ্য</h3>
    <p>প্রথম ৩ মাসে <mark>HTML ও CSS</mark> শেষ করব।</p>

    <h3>দীর্ঘমেয়াদী লক্ষ্য</h3>
    <p>একটি সম্পূর্ণ <strong>Full-Stack Web Application</strong> তৈরি করব।</p>
</body>
</html>
```

---

## 🤝 Guided Practice

তোমার `index.html` update করো:
1. শুধু একটি `<h1>` রাখো (তোমার নাম)
2. "আমার সম্পর্কে" section-এ `<h2>` দাও
3. "আমার লক্ষ্য" section-এ `<h2>` দাও
4. গুরুত্বপূর্ণ শব্দে `<strong>` ব্যবহার করো
5. একটি জায়গায় `<em>` ব্যবহার করো

---

## 🏆 Independent Challenge

**নিজে থেকে করো:**

একটি "My Story" section যোগ করো যেখানে:
- `<h2>` heading থাকবে
- অন্তত ২টি `<p>` থাকবে
- একটি `<strong>` ও একটি `<em>` থাকবে
- একটি `<br>` ব্যবহার করো সঠিক জায়গায়

**চিন্তা করো:** `<br>` কোথায় ব্যবহার করা উচিত? কবিতায়? ঠিকানায়?

---

## 📝 জমা দেওয়ার নির্দেশ

তোমার আপডেট করা `index.html` জমা দাও এবং ব্যাখ্যা করো:
1. কেন একটি page-এ একটিই `<h1>` রাখতে হয়?
2. `<strong>` ও `<b>` কি এক? পার্থক্য কী?
3. `<br>` কোন ক্ষেত্রে ব্যবহার করা উচিত নয়?
"""

DAY04_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- Anchor tag দিয়ে link তৈরি করা
- Relative ও absolute URL-এর পার্থক্য
- এক page থেকে অন্য page-এ যাওয়া
- Internal page navigation (anchor link)

---

## 📖 Concept

### Anchor Tag — Link তৈরির উপায়

```html
<a href="URL">Link-এর text</a>
```

**href** মানে Hypertext Reference — এখানে destination লেখা হয়।

### Absolute URL vs Relative URL

```html
<!-- Absolute URL — সম্পূর্ণ web address -->
<a href="https://www.google.com">Google-এ যাও</a>

<!-- Relative URL — একই folder-এর ফাইল -->
<a href="about.html">আমার সম্পর্কে</a>

<!-- Relative URL — subfolder-এর ফাইল -->
<a href="pages/contact.html">যোগাযোগ</a>
```

### New Tab-এ খোলা

```html
<a href="https://www.google.com" target="_blank" rel="noopener noreferrer">
    Google (নতুন tab-এ)
</a>
```
`rel="noopener noreferrer"` — নিরাপত্তার জন্য জরুরি।

### Internal Navigation (Page-এর ভেতরে)

```html
<!-- Navigation link -->
<a href="#about">আমার সম্পর্কে</a>

<!-- Target section -->
<section id="about">
    <h2>আমার সম্পর্কে</h2>
    ...
</section>
```

---

## 🌍 Real-world Example

Portfolio website-এর navigation bar-এ সব link সাধারণত **internal navigation** — একই page-এর বিভিন্ন section-এ নিয়ে যায়। এটা single-page website-এর মূল কৌশল।

---

## 💻 Code Demonstration

```html
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>আমার Portfolio</title>
</head>
<body>

    <!-- Navigation -->
    <nav>
        <a href="#home">Home</a> |
        <a href="#about">আমার সম্পর্কে</a> |
        <a href="#goals">লক্ষ্য</a> |
        <a href="contact.html">যোগাযোগ</a>
    </nav>

    <!-- Sections -->
    <section id="home">
        <h1>Faridur Rahman</h1>
        <p>Web Developer হওয়ার পথে...</p>
    </section>

    <section id="about">
        <h2>আমার সম্পর্কে</h2>
        <p>আমি Web Development শিখছি।</p>
        <a href="https://github.com" target="_blank" rel="noopener noreferrer">
            আমার GitHub
        </a>
    </section>

    <section id="goals">
        <h2>আমার লক্ষ্য</h2>
        <p>Full-Stack Developer হওয়া।</p>
    </section>

</body>
</html>
```

---

## 🤝 Guided Practice

1. তোমার `index.html`-এ একটি `<nav>` section যোগ করো উপরে
2. `#home`, `#about`, `#goals` — এই তিনটি internal link যোগ করো
3. প্রতিটি section-এ সংশ্লিষ্ট `id` attribute যোগ করো
4. একটি external link যোগ করো (যেকোনো ওয়েবসাইট) `target="_blank"` সহ

---

## 🏆 Independent Challenge

তোমার `about.html` ফাইলে একটি link যোগ করো যা `index.html`-এ ফিরে যায়।
তারপর `index.html`-এ একটি link যোগ করো যা `about.html`-এ যায়।
এভাবে দুটি page-এর মধ্যে navigation তৈরি করো।

---

## 📝 জমা দেওয়ার নির্দেশ

আপডেট করা `index.html` ও `about.html` জমা দাও এবং ব্যাখ্যা করো:
1. `href="#about"` ও `href="about.html"` — এই দুটির পার্থক্য কী?
2. External link-এ `target="_blank"` দিলে কী হয়?
3. `rel="noopener noreferrer"` কেন লাগে?
"""

DAY05_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- HTML-এ image যোগ করা
- `alt` attribute কেন জরুরি
- Ordered ও unordered list তৈরি করা
- Nested list (list-এর ভেতরে list)

---

## 📖 Concept

### Image Tag

```html
<img src="images/photo.jpg" alt="Faridur-এর ছবি" width="300">
```

| Attribute | কাজ |
|-----------|-----|
| `src` | ছবির path বা URL |
| `alt` | ছবি না দেখালে যা দেখায়; screen reader-এর জন্য |
| `width` | ছবির প্রস্থ (pixel-এ) |

**`alt` সবসময় দিতে হবে।** কখনো ফাঁকা রাখবে না যদি ছবিটি meaningful হয়।

### Unordered List (বুলেট)

```html
<ul>
    <li>HTML</li>
    <li>CSS</li>
    <li>JavaScript</li>
</ul>
```

### Ordered List (নম্বর সহ)

```html
<ol>
    <li>প্রথমে HTML শিখব</li>
    <li>তারপর CSS</li>
    <li>তারপর JavaScript</li>
</ol>
```

### Nested List

```html
<ul>
    <li>Frontend
        <ul>
            <li>HTML</li>
            <li>CSS</li>
            <li>JavaScript</li>
        </ul>
    </li>
    <li>Backend
        <ul>
            <li>Python</li>
            <li>Django</li>
        </ul>
    </li>
</ul>
```

---

## 🌍 Real-world Example

Amazon-এর product page-এ feature list হলো `<ul>`, আর recipe page-এ step-by-step instructions হলো `<ol>`। Portfolio-র "Skills" section সাধারণত `<ul>` দিয়ে তৈরি।

---

## 💻 Code Demonstration

```html
<section id="skills">
    <h2>আমার Skills</h2>
    <ul>
        <li>HTML (শিখছি)</li>
        <li>CSS (শিখব)</li>
        <li>JavaScript (শিখব)</li>
        <li>React (শিখব)</li>
    </ul>
</section>

<section id="learning-plan">
    <h2>শেখার পরিকল্পনা</h2>
    <ol>
        <li>HTML শেষ করব</li>
        <li>CSS শিখব</li>
        <li>JavaScript শিখব</li>
        <li>React শিখব</li>
        <li>Full-Stack project বানাব</li>
    </ol>
</section>

<section id="profile">
    <h2>আমার Profile</h2>
    <img src="images/profile.jpg" alt="Faridur Rahman-এর ছবি" width="200">
    <p>আমার ছবি এখানে থাকবে।</p>
</section>
```

---

## 🤝 Guided Practice

তোমার portfolio-তে যোগ করো:
1. একটি "Skills" section — `<ul>` দিয়ে তোমার শেখা ও শিখতে চাওয়া skills
2. একটি "শেখার পরিকল্পনা" section — `<ol>` দিয়ে ক্রমিকভাবে
3. একটি `<img>` tag যোগ করো (ছবি না থাকলে placeholder URL ব্যবহার করো: `https://via.placeholder.com/200`)

---

## 🏆 Independent Challenge

**Nested list তৈরি করো:**

Frontend ও Backend দুটি category সহ তোমার শেখার পরিকল্পনার একটি nested list তৈরি করো। প্রতিটি category-র ভেতরে সংশ্লিষ্ট technology-র list থাকবে।

---

## 📝 জমা দেওয়ার নির্দেশ

আপডেট করা `index.html` জমা দাও এবং ব্যাখ্যা করো:
1. `alt` attribute কখন ফাঁকা রাখা যায়?
2. `<ul>` বনাম `<ol>` — কোন পরিস্থিতিতে কোনটি ব্যবহার করবে?
3. `<li>` tag কি `<ul>` বা `<ol>` ছাড়া ব্যবহার করা যায়?
"""


DAY06_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- HTML Table তৈরি করা
- Table-এর row, column ও header
- `colspan` ও `rowspan` দিয়ে cell merge করা
- কখন Table ব্যবহার করা উচিত (এবং কখন নয়)

---

## 📖 Concept

### Table-এর মূল কাঠামো

```html
<table>
    <thead>           <!-- Table header অংশ -->
        <tr>          <!-- Table row -->
            <th>নাম</th>    <!-- Table header cell -->
            <th>বয়স</th>
        </tr>
    </thead>
    <tbody>           <!-- Table body অংশ -->
        <tr>
            <td>Faridur</td>  <!-- Table data cell -->
            <td>২৫</td>
        </tr>
    </tbody>
</table>
```

### Cell Merge

```html
<!-- colspan: পাশাপাশি cells মেলানো -->
<td colspan="2">এটি দুটি column জুড়ে আছে</td>

<!-- rowspan: উপর-নিচের cells মেলানো -->
<td rowspan="3">এটি তিনটি row জুড়ে আছে</td>
```

### কখন Table ব্যবহার করবে?
✅ Tabular data: marks list, schedule, comparison chart
❌ Page layout-এর জন্য (এটা CSS-এর কাজ)

---

## 🌍 Real-world Example

Class routine, পরীক্ষার ফলাফল, pricing comparison — সব জায়গায় HTML table ব্যবহার হয়।

---

## 💻 Code Demonstration

```html
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>আমার Skills Table</title>
</head>
<body>

<h2>আমার শেখার অগ্রগতি</h2>

<table border="1">
    <thead>
        <tr>
            <th>বিষয়</th>
            <th>স্তর</th>
            <th>অবস্থা</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>HTML</td>
            <td>Basic</td>
            <td>শিখছি ✅</td>
        </tr>
        <tr>
            <td>CSS</td>
            <td>Basic</td>
            <td>পরে শিখব ⏳</td>
        </tr>
        <tr>
            <td colspan="2">মোট বিষয়</td>
            <td>২টি</td>
        </tr>
    </tbody>
</table>

</body>
</html>
```

---

## 🤝 Guided Practice

তোমার `index.html`-এ একটি "আমার Skills" section যোগ করো যেখানে:
1. `<table>` দিয়ে তোমার শেখা ও শিখতে চাওয়া skills দেখাবে
2. Column হবে: বিষয়, স্তর, অবস্থা
3. `<thead>` ও `<tbody>` আলাদা থাকবে

---

## 🏆 Independent Challenge

**Class Routine তৈরি করো:**

একটি নতুন `schedule.html` ফাইলে সপ্তাহের ৫ দিনের শেখার routine তৈরি করো। প্রতিটি row হবে একটি বিষয় এবং column হবে সোম–শুক্র। যেদিন পড়বে সেখানে ✅ এবং যেদিন পড়বে না সেখানে ⬜ লেখো।

---

## 📝 জমা দেওয়ার নির্দেশ

তোমার `index.html` ও `schedule.html` জমা দাও এবং ব্যাখ্যা করো:
1. `<th>` ও `<td>`-এর পার্থক্য কী?
2. `colspan="2"` মানে কী?
3. Table কি সবসময় layout-এর জন্য ব্যবহার করা যাবে? কেন বা কেন নয়?
"""

DAY07_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- HTML Form তৈরি করা
- বিভিন্ন input type: text, email, password, number, date, checkbox, radio
- `<select>` dropdown ও `<textarea>`
- Form submit ও `action`/`method` attribute

---

## 📖 Concept

### Form-এর কাঠামো

```html
<form action="/submit" method="POST">
    <!-- Form elements এখানে -->
    <button type="submit">জমা দাও</button>
</form>
```

- `action` — form জমা দিলে কোথায় যাবে
- `method` — GET (URL-এ data) বা POST (লুকিয়ে data)

### Input Types

```html
<input type="text"     name="name"     placeholder="তোমার নাম">
<input type="email"    name="email"    placeholder="ইমেইল">
<input type="password" name="pass"     placeholder="পাসওয়ার্ড">
<input type="number"   name="age"      min="1" max="100">
<input type="date"     name="birthday">
<input type="checkbox" name="agree"    value="yes"> একমত
<input type="radio"    name="gender"   value="male">  পুরুষ
<input type="radio"    name="gender"   value="female"> মহিলা
```

### Label — সবসময় দিতে হবে

```html
<label for="email">ইমেইল:</label>
<input type="email" id="email" name="email">
```
`for` ও `id` এক হলে label ক্লিক করলে input focus হয়।

---

## 💻 Code Demonstration

```html
<form>
    <div>
        <label for="name">তোমার নাম:</label><br>
        <input type="text" id="name" name="name"
               placeholder="পুরো নাম লেখো" required>
    </div>

    <div>
        <label for="email">ইমেইল:</label><br>
        <input type="email" id="email" name="email" required>
    </div>

    <div>
        <label>তুমি কোন বিষয় শিখতে চাও?</label><br>
        <input type="checkbox" name="topics" value="html"> HTML<br>
        <input type="checkbox" name="topics" value="css"> CSS<br>
        <input type="checkbox" name="topics" value="js"> JavaScript
    </div>

    <div>
        <label for="level">অভিজ্ঞতার স্তর:</label>
        <select id="level" name="level">
            <option value="">বেছে নাও</option>
            <option value="beginner">একদম নতুন</option>
            <option value="some">কিছুটা জানি</option>
            <option value="intermediate">মাঝারি</option>
        </select>
    </div>

    <div>
        <label for="message">তোমার লক্ষ্য:</label><br>
        <textarea id="message" name="message" rows="4"
                  placeholder="কেন web developer হতে চাও..."></textarea>
    </div>

    <button type="submit">জমা দাও</button>
    <button type="reset">মুছে ফেলো</button>
</form>
```

---

## 🤝 Guided Practice

একটি `contact.html` ফাইল তৈরি করো:
1. নাম, ইমেইল, বিষয় ও বার্তা field থাকবে
2. প্রতিটি input-এর `label` থাকবে
3. Submit button থাকবে
4. `index.html` থেকে link দাও

---

## 🏆 Independent Challenge

তোমার portfolio-র "Contact Me" section-এ একটি form যোগ করো। Form-এ:
- নাম, ইমেইল (required)
- বিষয়: `<select>` দিয়ে (Collaboration, Question, Other)
- বার্তা: `<textarea>`
- Submit ও Reset button

---

## 📝 জমা দেওয়ার নির্দেশ

তোমার `contact.html` জমা দাও এবং ব্যাখ্যা করো:
1. `<label for="email">` ও `<input id="email">` কীভাবে connected?
2. `required` attribute কী করে?
3. `method="GET"` ও `method="POST"`-এর পার্থক্য কী?
"""

DAY08_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- Semantic HTML5 elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`
- Div vs Semantic elements — কোনটি কখন ব্যবহার করবে
- Semantic HTML কেন important (SEO ও accessibility)

---

## 📖 Concept

### Non-semantic vs Semantic

```html
<!-- পুরনো উপায় (avoid করো) -->
<div id="header">...</div>
<div id="nav">...</div>
<div id="content">...</div>

<!-- Semantic HTML5 (সঠিক উপায়) -->
<header>...</header>
<nav>...</nav>
<main>...</main>
```

### প্রধান Semantic Elements

| Element | কোথায় ব্যবহার করবে |
|---------|-----------------|
| `<header>` | পাতার বা section-এর শীর্ষে (logo, title) |
| `<nav>` | Navigation links |
| `<main>` | পাতার মূল content (শুধু একবার) |
| `<section>` | থিমের ভিত্তিতে ভাগ করা অংশ |
| `<article>` | স্বতন্ত্র content (blog post, news) |
| `<aside>` | পাশের অতিরিক্ত তথ্য (sidebar) |
| `<footer>` | পাতার নিচে (copyright, links) |

---

## 💻 Code Demonstration

```html
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Faridur | Portfolio</title>
</head>
<body>

    <header>
        <h1>Faridur Rahman</h1>
        <p>Aspiring Full-Stack Developer</p>
    </header>

    <nav>
        <a href="#about">আমার সম্পর্কে</a>
        <a href="#skills">Skills</a>
        <a href="#contact">যোগাযোগ</a>
    </nav>

    <main>
        <section id="about">
            <h2>আমার সম্পর্কে</h2>
            <p>আমি web development শিখছি...</p>
        </section>

        <section id="skills">
            <h2>আমার Skills</h2>
            <ul>
                <li>HTML ✅</li>
                <li>CSS (শিখছি)</li>
            </ul>
        </section>

        <section id="projects">
            <h2>আমার Projects</h2>
            <article>
                <h3>Developer Portfolio</h3>
                <p>আমার প্রথম HTML project।</p>
            </article>
        </section>
    </main>

    <aside>
        <h3>Quick Links</h3>
        <ul>
            <li><a href="https://github.com">GitHub</a></li>
        </ul>
    </aside>

    <footer>
        <p>&copy; 2024 Faridur Rahman. All rights reserved.</p>
    </footer>

</body>
</html>
```

---

## 🤝 Guided Practice

তোমার `index.html` সম্পূর্ণভাবে Semantic HTML দিয়ে নতুন করে লেখো:
1. `<div id="header">` → `<header>`
2. `<div id="nav">` → `<nav>`
3. Main content `<main>`-এর ভেতরে
4. প্রতিটি section `<section>` দিয়ে ভাগ করা
5. `<footer>`-এ copyright

---

## 🏆 Independent Challenge

**Blog Post Page তৈরি করো:**

`blog.html` নামে একটি ফাইল তৈরি করো। সেখানে তোমার "Web Development শেখার অভিজ্ঞতা" বিষয়ে একটি ছোট blog post লেখো। Semantic elements: `<article>`, `<header>`, `<main>`, `<footer>` ব্যবহার করো।

---

## 📝 জমা দেওয়ার নির্দেশ

আপডেট করা `index.html` ও `blog.html` জমা দাও এবং ব্যাখ্যা করো:
1. `<div>` ও `<section>`-এর পার্থক্য কী?
2. Semantic HTML SEO-এর জন্য কেন ভালো?
3. `<article>` কখন ব্যবহার করবে?
"""

DAY09_CONTENT = """## 🎯 আজকের লক্ষ্য

আজ তুমি শিখবে:
- HTML5 `<video>` ও `<audio>` element
- `<iframe>` দিয়ে YouTube video embed করা
- `<figure>` ও `<figcaption>`
- Responsive image ও `<picture>` element

---

## 📖 Concept

### Video

```html
<video width="640" height="360" controls>
    <source src="video.mp4" type="video/mp4">
    তোমার browser video support করে না।
</video>
```

Attributes: `controls` (play/pause button), `autoplay`, `loop`, `muted`

### Audio

```html
<audio controls>
    <source src="audio.mp3" type="audio/mpeg">
    তোমার browser audio support করে না।
</audio>
```

### Iframe — YouTube Embed

```html
<iframe
    width="560"
    height="315"
    src="https://www.youtube.com/embed/VIDEO_ID"
    title="Video title"
    allowfullscreen>
</iframe>
```

### Figure ও Figcaption

```html
<figure>
    <img src="chart.png" alt="Progress chart">
    <figcaption>আমার শেখার অগ্রগতির chart</figcaption>
</figure>
```

---

## 💻 Code Demonstration

```html
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>Media Page</title>
</head>
<body>

    <section>
        <h2>YouTube Tutorial</h2>
        <iframe
            width="560" height="315"
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            title="Tutorial video"
            allowfullscreen>
        </iframe>
    </section>

    <section>
        <h2>আমার Project Screenshot</h2>
        <figure>
            <img src="https://via.placeholder.com/400x300"
                 alt="Project screenshot"
                 width="400">
            <figcaption>আমার প্রথম HTML project</figcaption>
        </figure>
    </section>

</body>
</html>
```

---

## 🤝 Guided Practice

তোমার portfolio-তে:
1. একটি YouTube tutorial-এর iframe embed করো (যেকোনো HTML tutorial)
2. একটি `<figure>` যোগ করো placeholder image ও caption সহ
3. `index.html` থেকে এই page-এ link দাও

---

## 🏆 Independent Challenge

`media.html` নামে একটি page তৈরি করো:
- দুটি YouTube video embed করো
- প্রতিটির নিচে `<figure>` ও `<figcaption>` দিয়ে ব্যাখ্যা দাও
- Semantic structure ব্যবহার করো

---

## 📝 জমা দেওয়ার নির্দেশ

`media.html` জমা দাও এবং ব্যাখ্যা করো:
1. `<video>` ও `<iframe>` — video দেখানোর দুটি উপায়। কোনটি কখন ব্যবহার করবে?
2. `<figure>` ও শুধু `<img>` — পার্থক্য কী?
3. `allowfullscreen` attribute কী করে?
"""

DAY10_CONTENT = """## 🎯 আজকের লক্ষ্য

🎉 **Stage 1 Project Day!**

আজ তুমি HTML-এ যা শিখেছো (Day 1–9) সব মিলিয়ে একটি সম্পূর্ণ **Personal Portfolio Website** তৈরি করবে।

---

## 📋 Project Specification

### তোমার Portfolio-তে কী কী থাকবে:

**`index.html` (Home Page)**
- `<header>`: তোমার নাম ও tagline
- `<nav>`: Home, About, Skills, Projects, Contact লিঙ্ক
- `<main>`:
  - `<section id="about">`: তোমার পরিচয় ও ছবি (`<figure>`)
  - `<section id="skills">`: দুটো list — শেখা skills ও শিখতে চাওয়া skills
  - `<section id="projects">`: তোমার project (এখন পর্যন্ত একটিই — এই portfolio!)
  - `<section id="contact">`: Contact form
- `<footer>`: Copyright

**`about.html`**
- তোমার বিস্তারিত পরিচয়
- তোমার শেখার journey ও লক্ষ্য

**`schedule.html`**
- সাপ্তাহিক শেখার routine (Table ব্যবহার করো)

---

## ✅ Checklist (প্রতিটি নিশ্চিত করো)

- [ ] Proper `<!DOCTYPE html>`, `<html lang="bn">`, `<head>`, `<body>`
- [ ] Meaningful `<title>` ও `<meta>` tags
- [ ] Semantic elements: header, nav, main, section, footer
- [ ] অন্তত একটি `<table>`
- [ ] একটি `<form>` (contact form)
- [ ] Image সহ `<figure>` ও `<figcaption>`
- [ ] Internal navigation (anchor links)
- [ ] External link (GitHub/LinkedIn) `target="_blank"` সহ
- [ ] সব pages-এ navigation link

---

## 💡 Tips

- এটি "perfect" হতে হবে না — এখনো CSS শিখোনি, তাই সুন্দর না দেখালে ঠিক আছে।
- প্রতিটি HTML element যেন সঠিক জায়গায় ব্যবহার হয়।
- নিজের আসল তথ্য দাও — এটি তোমার real portfolio!

---

## 📝 জমা দেওয়ার নির্দেশ

তোমার সম্পূর্ণ project **ZIP করে** জমা দাও এবং ব্যাখ্যা করো:
1. কোন অংশটি সবচেয়ে কঠিন মনে হয়েছে ও কীভাবে সমাধান করেছো?
2. তুমি কোন HTML element সবচেয়ে বেশি ব্যবহার করেছো ও কেন?
3. CSS না শিখলে কী কী সীমাবদ্ধতা অনুভব করলে?

> 🎯 **৭৫% বা বেশি পেলে CSS শেখা শুরু হবে!**
"""

# ════════════════════════════════════════════════════════
# CURRICULUM DATA STRUCTURE
# ════════════════════════════════════════════════════════

CURRICULUM = [
    {
        "stage": {"number": 0, "title": "Development Environment", "description": "কম্পিউটার সেটআপ, VS Code, Terminal ও প্রথম ওয়েবপেজ।", "order": 0},
        "modules": [
            {
                "number": 1,
                "title": "Development Environment Setup",
                "description": "Project folder, VS Code, browser — web development-এর প্রস্তুতি।",
                "order": 1,
                "lessons": [
                    {"day": 1, "title": "প্রথম HTML পাতা", "content": DAY01_CONTENT, "order": 1},
                ],
            }
        ],
    },
    {
        "stage": {"number": 1, "title": "HTML5: Web Structure", "description": "ওয়েবপেজের কাঠামো তৈরির সম্পূর্ণ ভাষা।", "order": 1},
        "modules": [
            {
                "number": 1,
                "title": "HTML Fundamentals",
                "description": "HTML document structure, elements, attributes ও text formatting।",
                "order": 1,
                "lessons": [
                    {"day": 2, "title": "HTML Document Structure", "content": DAY02_CONTENT, "order": 1},
                    {"day": 3, "title": "Headings, Paragraphs ও Text Formatting", "content": DAY03_CONTENT, "order": 2},
                ],
            },
            {
                "number": 2,
                "title": "Links, Media ও Lists",
                "description": "Anchor tag, images ও list তৈরি।",
                "order": 2,
                "lessons": [
                    {"day": 4, "title": "Links ও Navigation", "content": DAY04_CONTENT, "order": 1},
                    {"day": 5, "title": "Images ও Lists", "content": DAY05_CONTENT, "order": 2},
                ],
            },
            {
                "number": 3,
                "title": "Tables ও Forms",
                "description": "Data table তৈরি ও user input form।",
                "order": 3,
                "lessons": [
                    {"day": 6, "title": "HTML Tables", "content": DAY06_CONTENT, "order": 1},
                    {"day": 7, "title": "HTML Forms", "content": DAY07_CONTENT, "order": 2},
                ],
            },
            {
                "number": 4,
                "title": "Semantic HTML ও Media",
                "description": "HTML5 semantic elements, video, audio ও iframe।",
                "order": 4,
                "lessons": [
                    {"day": 8, "title": "Semantic HTML5", "content": DAY08_CONTENT, "order": 1},
                    {"day": 9, "title": "HTML5 Media (Video, Audio, Iframe)", "content": DAY09_CONTENT, "order": 2},
                ],
            },
            {
                "number": 5,
                "title": "Stage 1 Project",
                "description": "Personal Portfolio — সব HTML জ্ঞান একসাথে।",
                "order": 5,
                "lessons": [
                    {"day": 10, "title": "Personal Portfolio Website (HTML Project)", "content": DAY10_CONTENT, "order": 1},
                ],
            },
        ],
    },
]


# ════════════════════════════════════════════════════════
# MANAGEMENT COMMAND
# ════════════════════════════════════════════════════════

class Command(BaseCommand):
    help = 'Stage 0 ও Stage 1-এর পাঠ database-এ ঢোকায়।'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='সব ডেটা মুছে নতুন করে seed করো।',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Stage.objects.all().delete()
            self.stdout.write(self.style.WARNING('পুরোনো ডেটা মুছে ফেলা হয়েছে।'))

        total_lessons = 0
        for stage_data in CURRICULUM:
            stage, created = Stage.objects.get_or_create(
                number=stage_data['stage']['number'],
                defaults={
                    'title': stage_data['stage']['title'],
                    'description': stage_data['stage']['description'],
                    'order': stage_data['stage']['order'],
                },
            )
            if created:
                self.stdout.write(f'  ✓ Stage {stage.number}: {stage.title}')

            for mod_data in stage_data['modules']:
                module, _ = Module.objects.get_or_create(
                    stage=stage,
                    number=mod_data['number'],
                    defaults={
                        'title': mod_data['title'],
                        'description': mod_data.get('description', ''),
                        'order': mod_data['order'],
                    },
                )

                for lesson_data in mod_data['lessons']:
                    lesson, created = Lesson.objects.get_or_create(
                        day_number=lesson_data['day'],
                        defaults={
                            'module': module,
                            'title': lesson_data['title'],
                            'content': lesson_data['content'],
                            'is_seeded': True,
                            'order': lesson_data['order'],
                        },
                    )
                    if created:
                        total_lessons += 1
                        self.stdout.write(f'    → Day {lesson.day_number:02d}: {lesson.title}')

        if total_lessons:
            self.stdout.write(self.style.SUCCESS(
                f'\n✅ সফলভাবে {total_lessons}টি পাঠ যোগ হয়েছে।'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                '\nℹ️  সব পাঠ আগেই ছিল — কিছু পরিবর্তন হয়নি।'
            ))
        self.stdout.write('Admin: http://127.0.0.1:8000/admin/')
