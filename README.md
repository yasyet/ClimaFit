# ClimaFit — Project Spec (Markdown)

## 1) What ClimaFit Does

ClimaFit is a personal outfit recommendation system. It learns _your_ comfort response to weather by logging **weather + time + outfit + comfort outcomes** at fixed times (12:00, 16:00, 18:00, 20:00).  
Given current (or forecast) conditions, it evaluates a set of sensible outfit options and recommends the outfit(s) with the highest predicted comfort—minimizing **cold/heat discomfort**, **sweating**, and **wetness**.

ClimaFit does **not** predict the weather. It predicts **your comfort** for each clothing option and chooses the best one.

---

## 2) Core Idea (Decision Model)

**Context (weather + time) + Action (outfit) → Predicted Outcome (comfort)**  
Then a scoring/ranking layer picks the best outfit.

---

## 3) Outputs (What the User Gets)

- **Top-1 recommendation** (or **Top-3**) for the current conditions
- **Short explanation** (why it chose it)
- Optional: warnings (“high wind chill”, “rain likely → waterproof outer layer”)

---

## 4) Data Model

### 4.1 Required Logging Times

- 12:00, 16:00, 18:00, 20:00  
  Optional: extra logs for unusual events (heavy rain, long outdoor time, sports).

### 4.2 Logged Fields (MVP)

**Context**

- `timestamp` (ISO)
- `location` (city/station id)
- `temperature_c`
- `feels_like_c`
- `wind_kmh`
- `humidity_pct`
- `precip_mm` (or `precip_bool`)
- `cloud_pct` (optional)

**Action (Outfit)**

- `base_layer` (categorical)
- `mid_layer` (categorical)
- `outer_layer` (categorical)
- optional: `pants`, `addons`, `shoes`

**Labels (Outcomes)**

- `temp_discomfort` in `[-3..+3]` (required)
- `sweat_level` in `[0..3]` (required)
- `wetness_level` in `[0..3]` (required if rain)
- optional: `overall_comfort` in `[0..10]`

**Optional Context**

- `activity` (standing/walking/cycling/sport/commute)
- `time_outside_min`
- `notes` (short)

### 4.3 Storage

- Start: `CSV` (easy)
- Upgrade: `SQLite` (safer + scalable)
- Keep a strict vocabulary for categories to avoid label drift.

---

## 5) System Components (Subprojects)

### 5.1 Data Collection (Logging)

Build a logger that creates consistent entries at the required times.  
Goal: minimal friction, consistent fields, no missing labels.

Deliverables:

- Logging template (CSV/JSON)
- Quick input method (form / shortcut / CLI)

---

### 5.2 Weather Ingestion

Fetch weather data for the chosen location at logging time and at recommendation time.

Options:

- Manual entry (MVP)
- API-based (later): current conditions + optional forecast

Deliverables:

- `get_weather(location, timestamp)` module
- normalization (units, missing fields)

---

### 5.3 Schema + Validation

Enforce consistent categories and numeric ranges.

Deliverables:

- fixed category lists (base/mid/outer/addons)
- validators (range checks, required fields)
- automatic cleanup rules (e.g. unknown → reject)

---

### 5.4 Feature Engineering (Preprocessing)

Transform raw values into model-ready features:

- encode categories (one-hot or embeddings)
- time features (hour, month, season)
- derived weather features (wind chill relevance, rain flag)

Deliverables:

- preprocessing pipeline saved with the model
- versioned feature set

---

### 5.5 Model Training

Train a model to predict comfort outcomes from:
`(weather + time + outfit) → (temp_discomfort, sweat_level, wetness_level)`

Recommended model (tabular-friendly):

- Gradient boosted trees (CatBoost / LightGBM / XGBoost)

NN option (later):

- small MLP + embeddings for categorical outfit fields

Deliverables:

- training script/notebook
- evaluation report (by-date split)
- saved model artifact + preprocessing artifact

---

### 5.6 Scoring + Recommendation Engine

Generate sensible outfit candidates, predict outcomes, compute score, rank.

Example score:
`score = -abs(temp_discomfort) - α*sweat_level - β*wetness_level`

Deliverables:

- candidate generator (valid combos only)
- ranker (top-1/top-3)
- explanation generator (simple rules tied to features)

---

### 5.7 Baseline Rules (Safety Net)

Before enough data exists, use a rule-based baseline or blend baseline + model.

Deliverables:

- baseline thresholds (feels_like/wind/rain)
- blending strategy (e.g. model overrides only after N samples)

---

### 5.8 Analytics + Feedback Loop

Track performance and data coverage:

- where recommendations fail
- which weather zones have little data
- comfort trends over seasons

Deliverables:

- simple dashboard or reports (weekly/monthly)
- “data gaps” checklist (what to log more)

---

### 5.9 Deployment (User Interface)

Make ClimaFit usable day-to-day:

- CLI script, web dashboard, phone shortcut, or desktop widget

Deliverables:

- `recommend_now()` command
- saved model loading + fast inference
- retrain trigger (weekly or every N new samples)

---

## 6) Project Milestones

### Milestone A — MVP (1–2 weeks of logs)

- Manual logging template
- Basic baseline recommendations
- Minimal candidate set (e.g. 10–20 outfits)

### Milestone B — First Model (200–300 logs)

- Train first predictive model
- Top-3 recommendations + explanation
- Basic evaluation (date-based split)

### Milestone C — Reliable Tool (500–1000 logs)

- Better candidate generation
- Regular retraining
- Analytics + error tracking

---

## 7) Quality Targets

- Logging completeness: > 90% entries have all required fields
- Recommendation stability: no “nonsense combos”
- Comfort improvement: increasing average predicted and reported comfort over time

---

## 8) Directory Layout (Suggested)
