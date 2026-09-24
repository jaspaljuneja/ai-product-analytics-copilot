# AI Product Analytics Copilot

**An AI-powered product analytics assistant that turns natural-language business questions into SQL-backed insights.**

## Overview

Product and business teams often need analysts to answer questions that require multiple steps:

1. Understand the business question
2. Identify the relevant data
3. Inspect the database schema
4. Write SQL
5. Execute the query
6. Analyze the results
7. Explain the business impact

The **AI Product Analytics Copilot** streamlines this workflow.

A business user can ask:

> **Why did conversion rate drop in August?**

The application uses an LLM to generate SQL, executes that SQL against a product analytics database, and then uses the query results to produce a concise, structured business explanation.

---

## Product Goal

Reduce **time-to-insight** for business users who need answers from structured analytics data but do not want to manually write SQL for every question.

### Target Users

* Business Analysts
* Product Managers
* Data Analysts
* Business Operations teams
* Product and business leaders

### Primary Persona

**Business Analyst**

A Business Analyst frequently receives ad-hoc questions from product and leadership teams and spends significant time translating those questions into SQL, validating results, and communicating findings.

The Copilot automates the repetitive analytical workflow while keeping the underlying SQL visible.

---

# How It Works

```text
┌─────────────────────┐
│      User           │
│ Business Question   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Streamlit UI     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Python Orchestrator │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│        LLM          │
│ Natural Language →  │
│        SQL          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   SQLite Database   │
│                     │
│ Users / Products /  │
│ Events / Orders     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Query Results    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│        LLM          │
│ Results → Business  │
│       Insight       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Business Explanation│
│ + Findings          │
│ + Possible Causes   │
│ + Confidence        │
└─────────────────────┘
```

The application deliberately separates **data retrieval** from **language generation**:

* SQL retrieves the quantitative data.
* The LLM interprets and communicates the results.
* The database remains the source of the numerical evidence.

---

# Core AI Workflow

## 1. Understand the Question

The user enters a natural-language business question.

Example:

```text
Why did conversion rate drop in August?
```

## 2. Inspect the Data

The application provides the LLM with:

* Database type
* Database schema
* Table and column information
* Business metric definitions

## 3. Generate SQL

The LLM converts the business question into SQLite-compatible SQL.

Example:

```sql
SELECT
    DATE(event_date, 'start of month') AS month,
    COUNT(DISTINCT CASE
        WHEN event_name = 'purchase' THEN user_id
    END) * 1.0 /
    COUNT(DISTINCT user_id) AS conversion_rate
FROM events
GROUP BY DATE(event_date, 'start of month');
```

## 4. Execute the Query

The generated SQL is executed against the SQLite analytics database.

## 5. Analyze the Results

The resulting data is passed to a second LLM prompt.

The model is instructed to:

* Use only the returned results
* Identify important findings
* Include relevant metrics
* Distinguish facts from possible explanations
* Avoid inventing unsupported numbers

## 6. Return Structured Insight

The response follows a predictable structure:

```json
{
  "summary": "Short business summary",
  "key_findings": [
    "Finding 1",
    "Finding 2",
    "Finding 3"
  ],
  "possible_explanation": [
    "Possible explanation 1",
    "Possible explanation 2"
  ],
  "confidence": "Medium"
}
```

---

# Current MVP

The MVP currently supports:

* Natural-language business questions
* Automatic database schema inspection
* Business metric definitions
* LLM-powered SQL generation
* SQLite query execution
* LLM-powered result interpretation
* Structured JSON insights
* Confidence levels
* Streamlit web interface
* Synthetic product analytics data

---

# Example Dataset

The project includes a synthetic product analytics database.

| Dataset  | Records |
| -------- | ------: |
| Users    |  10,000 |
| Products |      50 |
| Events   | 220,000 |
| Orders   |  11,523 |

The dataset contains activity across 2026, including:

* User activity
* Product interactions
* Purchases
* Orders
* Revenue
* Device information
* Countries
* Age groups
* Product categories

### Database Tables

```text
users
products
events
orders
```

### Relationships

```text
users.user_id
      │
      ├──────── events.user_id
      │
      └──────── orders.user_id

products.product_id
      │
      ├──────── events.product_id
      │
      └──────── orders.product_id
```

---

# Business Metrics

The Copilot currently understands several product analytics concepts.

### Conversion Rate

```text
Unique users with a purchase
─────────────────────────────
Unique users with any event
```

### Revenue

Total revenue recorded in the `orders` table.

### Orders

Number of records in the `orders` table.

### Average Order Value

```text
Total Revenue
─────────────
Total Orders
```

Additional concepts include:

* Users
* Products
* Purchases
* Categories
* Devices

Metric definitions are explicitly provided to the LLM so that common business terms have consistent meanings.

---

# Example Questions

Users can ask questions such as:

```text
Why did conversion rate drop in August?

What happened to revenue in August?

Which product category generated the most revenue?

What is our average order value?

Which products generated the most revenue?

How does conversion vary by device?

Which category generates the most revenue?

How many users are in each country?
```

---

# Technology Stack

| Layer           | Technology   |
| --------------- | ------------ |
| Frontend / UI   | Streamlit    |
| Backend         | Python       |
| LLM             | OpenAI API   |
| Database        | SQLite       |
| Data Processing | Pandas       |
| Query Language  | SQL          |
| Version Control | Git / GitHub |

---

# Project Structure

```text
ai-product-analytics-copilot/
│
├── app.py
│
├── data/
│   └── analytics.db
│
├── src/
│   ├── analysis.py
│   ├── business_definitions.py
│   ├── copilot.py
│   ├── database.py
│   ├── generate_data.py
│   ├── llm.py
│   ├── prompt.py
│   └── schema.py
│
├── .gitignore
└── README.md
```

### Key Components

**`app.py`**

Streamlit user interface.

**`copilot.py`**

Orchestrates the end-to-end workflow.

**`prompt.py`**

Builds the SQL-generation prompt using schema and business definitions.

**`schema.py`**

Inspects the SQLite database schema.

**`database.py`**

Executes SQL queries.

**`llm.py`**

Handles natural-language-to-SQL generation.

**`analysis.py`**

Converts query results into structured business insights.

**`business_definitions.py`**

Contains standardized definitions for product analytics metrics.

**`generate_data.py`**

Creates the synthetic analytics dataset.

---

# Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/jaspaljuneja/ai-product-analytics-copilot.git

cd ai-product-analytics-copilot
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install openai streamlit pandas
```

## 4. Configure the OpenAI API Key

Set the API key as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

The application reads the key through the OpenAI client.

**Never hard-code API keys in source code or commit them to GitHub.**

## 5. Run the Application

```bash
streamlit run app.py
```

The Streamlit application will be available locally.

---

# Product Architecture

The system uses a lightweight orchestration architecture rather than treating the LLM as the entire application.

```text
             ┌───────────────┐
             │     User      │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │   Streamlit   │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │  Orchestrator │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │      LLM      │
             │  NL → SQL     │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │    SQLite     │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │ Query Results  │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │      LLM      │
             │ Results →     │
             │ Insight       │
             └───────────────┘
```

This architecture creates a clear separation between:

**Reasoning layer**

LLM understands the user's business question and explains the results.

**Data layer**

SQLite provides the actual quantitative data.

**Application layer**

Python controls the workflow between the user, LLM, and database.

---

# AI Product Management Concepts Demonstrated

This project is designed not only as a coding exercise, but as an example of practical AI product development.

### Problem Definition

Translates a common analytics bottleneck into an AI product opportunity.

### User Experience

Allows business users to interact using natural language rather than SQL.

### AI Workflow Design

Separates:

```text
Intent → SQL → Data → Insight
```

rather than asking the LLM to directly invent an answer.

### Grounded Generation

Business explanations are generated using the returned SQL results as the evidence base.

### Structured Output

The insight-generation stage returns a predictable JSON structure rather than unrestricted prose.

### Metric Definitions

Business terminology is explicitly defined to reduce ambiguity.

### AI Evaluation

The project identifies measurable quality dimensions instead of evaluating the LLM only by whether the response "sounds good."

---

# Evaluation Framework

A production version would measure both **AI quality** and **product performance**.

### Accuracy

* SQL execution success rate
* SQL correctness
* Answer correctness
* Metric calculation accuracy
* Unsupported-claim / hallucination rate

### Performance

* Median latency (P50)
* P95 latency
* Tokens per request
* Estimated cost per analysis

### Product Metrics

* User satisfaction
* Repeat usage
* Successful question rate
* Follow-up question rate
* Time-to-insight

### North Star Metric

**Time-to-insight**

> The time required for a business user to move from a question to a useful, data-backed insight.

---

# Known Limitations

This is an MVP and intentionally uses a simple architecture.

Current limitations include:

* Synthetic data rather than production data
* SQLite rather than a production warehouse
* Limited data-source support
* No authentication
* No multi-user environment
* No production access controls
* Limited conversation memory
* No automated chart generation in the current MVP
* Generated SQL is executed directly
* Synthetic event and order relationships do not perfectly represent a production analytics system

These limitations provide the basis for future product iterations.

---

# Roadmap

## Phase 1 — MVP

* [x] Synthetic analytics database
* [x] Database schema inspection
* [x] Business metric definitions
* [x] Natural-language-to-SQL
* [x] SQL execution
* [x] Business insight generation
* [x] Streamlit interface
* [x] GitHub repository

## Phase 2 — Product Analytics

* [ ] KPI analysis
* [ ] Funnel analysis
* [ ] Cohort analysis
* [ ] Trend analysis
* [ ] Segment analysis
* [ ] Automated charts
* [ ] Follow-up questions
* [ ] Conversation context

## Phase 3 — Enterprise Data

* [ ] CSV upload
* [ ] Multiple datasets
* [ ] PostgreSQL
* [ ] MySQL
* [ ] Cloud data warehouses
* [ ] Authentication
* [ ] Role-based access

## Phase 4 — Analytics Agent

* [ ] Automated anomaly detection
* [ ] Root-cause analysis
* [ ] Proactive insights
* [ ] Scheduled reports
* [ ] Alerts
* [ ] Recommended next actions
* [ ] Multi-step analytical workflows

---

# Why This Project Matters

The core product idea is not simply **"ChatGPT that writes SQL."**

The product is an analytical workflow that connects:

```text
Business Question
       ↓
Data Retrieval
       ↓
Quantitative Analysis
       ↓
Business Interpretation
       ↓
Decision Support
```

The long-term opportunity is to move from a reactive analytics assistant toward an AI system that can proactively identify meaningful changes, investigate potential drivers, and communicate insights to business teams.

---

# Portfolio Context

This project demonstrates hands-on experience across:

* AI Product Management
* Product analytics
* KPI design
* SQL
* Python
* LLM application architecture
* Prompt engineering
* Structured outputs
* Data modeling
* AI evaluation
* Product requirements
* MVP development
* Git/GitHub

The project is intentionally being developed incrementally, starting with a simple working MVP and expanding toward a more capable analytics agent.


## Project Architecture

The AI Product Analytics Copilot uses a simple LLM-powered analytics pipeline where the application orchestrates the workflow and the LLM handles natural-language understanding, SQL generation, and business interpretation.

```text
                         ┌─────────────────────────┐
                         │        User             │
                         │                         │
                         │ "Why did conversion     │
                         │  rate drop in August?"  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     Streamlit UI        │
                         │                         │
                         │ • Question input        │
                         │ • Results display       │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │   Python Orchestrator   │
                         │       copilot.py        │
                         │                         │
                         │ Coordinates the         │
                         │ analytics workflow      │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
              ┌───────────────────┐     ┌───────────────────┐
              │  Schema + Business│     │      OpenAI       │
              │    Definitions    │────▶│       LLM         │
              │                   │     │                   │
              │ • Database schema │     │ Natural language  │
              │ • KPI definitions │     │ → SQL generation  │
              └───────────────────┘     └─────────┬─────────┘
                                                  │
                                                  ▼
                                      ┌─────────────────────┐
                                      │    SQL Execution    │
                                      │     database.py     │
                                      └──────────┬──────────┘
                                                 │
                                                 ▼
                                      ┌─────────────────────┐
                                      │     SQLite DB       │
                                      │                     │
                                      │ • users             │
                                      │ • products          │
                                      │ • events            │
                                      │ • orders            │
                                      └──────────┬──────────┘
                                                 │
                                                 ▼
                                      ┌─────────────────────┐
                                      │    Query Results    │
                                      └──────────┬──────────┘
                                                 │
                                                 ▼
                                      ┌─────────────────────┐
                                      │   Insight Engine    │
                                      │     analysis.py     │
                                      │                     │
                                      │ Results → business  │
                                      │ explanation         │
                                      └──────────┬──────────┘
                                                 │
                                                 ▼
                                      ┌─────────────────────┐
                                      │   Structured JSON   │
                                      │                     │
                                      │ • Summary           │
                                      │ • Key findings      │
                                      │ • Explanations      │
                                      │ • Confidence        │
                                      └──────────┬──────────┘
                                                 │
                                                 ▼
                                      ┌─────────────────────┐
                                      │    Streamlit UI     │
                                      │                     │
                                      │ Business insight +  │
                                      │ supporting results  │
                                      └─────────────────────┘
```

### Architecture Flow

The current MVP follows this workflow:

**1. User Question**

The user submits a natural-language business question through Streamlit.

**2. Context Assembly**

The application provides the LLM with:

* Database schema
* Table and column definitions
* Business KPI definitions
* The user's question
* SQLite-specific SQL instructions

**3. SQL Generation**

The LLM converts the business question into a SQLite-compatible SQL query.

**4. Database Execution**

The Python application executes the generated SQL against the SQLite analytics database.

**5. Result Analysis**

The query results, SQL, and business definitions are sent to a second LLM step that interprets the results.

**6. Structured Business Insight**

The analysis layer returns structured JSON containing:

* Summary
* Key findings
* Possible explanations
* Confidence level

**7. User-Facing Output**

Streamlit presents the resulting business insight to the user.

### Component Responsibilities

| Component                 | Responsibility                                |
| ------------------------- | --------------------------------------------- |
| `app.py`                  | Streamlit user interface                      |
| `copilot.py`              | Orchestrates the end-to-end workflow          |
| `prompt.py`               | Builds the SQL-generation prompt              |
| `schema.py`               | Inspects the database schema                  |
| `business_definitions.py` | Defines business metrics and terminology      |
| `llm.py`                  | Handles LLM-based SQL generation              |
| `database.py`             | Executes SQL against SQLite                   |
| `analysis.py`             | Converts query results into business insights |
| `generate_data.py`        | Generates synthetic product analytics data    |
| `analytics.db`            | Stores the analytics dataset                  |

### Design Principle

The application follows a **deterministic application layer + probabilistic AI layer** architecture.

The Python application controls the workflow, database connection, and execution. The LLM is used for tasks where natural-language understanding and interpretation provide value:

```text
Business Question
       ↓
      LLM
       ↓
   SQL Query
       ↓
 Python Application
       ↓
   SQLite Data
       ↓
      LLM
       ↓
Business Insight
```

This separation makes the system easier to extend toward additional analytics capabilities such as KPI calculations, funnel analysis, cohort analysis, automated visualization, follow-up questions, and eventually more autonomous analytics workflows.


