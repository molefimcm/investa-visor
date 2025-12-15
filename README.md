# investa-visor
#### Video Demo:  <URL HERE>
#### Description:
AI-powered investing clarity without prompting.

InvestaVisor is a lightweight investment utility designed to help everyday users build clarity, discipline, and consistent habits—without needing to understand or write AI prompts. It generates high-level guidance, sanity checks, and daily routines based on simple user inputs, using a structured prompting engine behind the scenes.

InvestaVisor is not a financial advisor. It does not recommend buying or selling any assets. It is an educational and research-support tool that helps users focus, reflect, and stay disciplined.

🚀 Features

Zero-prompting experience — users never write prompts; InvestaVisor structures them automatically.

Daily investing plan including focus areas, discipline reminders, and educational insights.

AI-ready architecture — GPT integration can be enabled post-MVP.

Rule-based output for MVP — runs at zero cost with no external API calls.

C module for risk allocation — small native library for speed and teaching value.

Flask backend + SQLite database — simple, portable stack.

PWA-ready frontend — works on mobile, desktop, and web.

Privacy-first — no personal user data is sent to AI models.

🏗️ Tech Stack

Python (Flask) – backend REST API

HTML/CSS/JS – frontend

SQLite – persistent storage

C – risk allocation engine (via shared library)

OpenAI API (disabled for MVP) – optional future enhancement

PWA setup – for mobile/desktop installation

investa-visor/
├── app.py
├── config.py
├── db.py
├── schema.sql
├── c_core/
│   ├── risk_calc.c
│   └── Makefile
├── models/
│   ├── auth.py
│   ├── personal.py
│   ├── investment.py
│   ├── plans.py
│   └── analytics.py
├── services/
│   ├── prompt_builder.py
│   ├── risk_engine.py
│   ├── llm_client.py
│   └── events.py
├── templates/
│   └── index.html
└── static/
    ├── styles.css
    ├── main.js
    ├── manifest.json
    └── service-worker.js
