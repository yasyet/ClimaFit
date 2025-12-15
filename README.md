# ClimaFit (Closed Project – Open Source Code)

ClimaFit is a **personal outfit comfort modeling system**.  
The repository contains **open-source code only**.  
The **service, data, and trained models are private and not publicly accessible**.

This project is currently in an **experimental / research phase** and is **not intended for public use**.

---

## Project Status

- 🔒 **Project access:** Private / closed
- 📂 **Code visibility:** Open source
- 📊 **Data:** Private (not included)
- 🤖 **Models:** Personal, not distributed
- 🚫 **No public API / app**

This repository exists to:

- document the system architecture,
- allow reproducibility of the approach,
- showcase engineering and ML design decisions.

---

## What ClimaFit Is

ClimaFit learns **how a specific person feels in specific weather conditions**, given what they are wearing.

It predicts **comfort**, not fashion and not weather.

**Input**

- Weather conditions (temperature, wind, rain, humidity, etc.)
- Time of day
- Outfit configuration (layers)

**Output**

- Predicted comfort (cold / heat, sweating, wetness)
- Ranked outfit recommendations (Top-1 / Top-3)

---

## Core Idea

(weather + time) + outfit → predicted comfort
The system evaluates multiple valid outfit options and selects the one with the **best predicted comfort outcome**.

---

## Repository Scope

This repository includes:

- data schema definitions
- logging & validation logic
- feature engineering pipeline
- model training and inference code
- recommendation and ranking logic

This repository does **not** include:

- personal datasets
- cloud credentials
- trained models
- deployment endpoints

---

## Data Handling Philosophy

- Data is **append-only**
- Data is **user-owned**
- Data is **never auto-shared**
- Data storage is **external to this repository**

The canonical dataset is stored as **CSV files in private cloud storage**.

---

## CSV-Based Dataset (Canonical Format)

ClimaFit uses CSV as the **single source of truth** for logged data.

Key principles:

- human-readable
- debuggable
- versionable
- cloud-compatible

The exact schema is documented in `/docs/data_schema.md`.

---

## Cloud Storage (High-Level)

The system is designed to work with:

- private cloud object storage
- monthly partitioned CSV files
- local caching + explicit sync

No cloud provider is hard-coded into the codebase.

---

## Why the Project Is Closed

ClimaFit is:

- highly personal
- based on subjective comfort data
- continuously evolving

Opening the _code_ improves quality.  
Keeping the _system_ closed preserves correctness, privacy, and control.

---

## License

Code is released under an open-source license (MIT recommended).  
**Data, trained models, and brand name are excluded from the license.**

---

## Disclaimer

This repository is provided for educational and technical reference.  
Running the code without adapting it to your own data and cloud setup will not produce meaningful results.
