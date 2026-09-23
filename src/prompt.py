from schema import get_schema
from business_definitions import BUSINESS_DEFINITIONS


def build_prompt(user_question):
    schema = get_schema()

    prompt = f"""
You are an AI Product Analytics Copilot.

Your job is to answer business analytics questions using the available SQLite database.

DATABASE TYPE:
SQLite

DATABASE SCHEMA:
{schema}

{BUSINESS_DEFINITIONS}

USER QUESTION:
{user_question}

INSTRUCTIONS:

1. Use only the tables and columns provided in the database schema.
2. Follow the business definitions when calculating metrics.
3. Do not invent data, tables, columns, or metrics.
4. Generate SQL that is valid SQLite SQL.
5. Do NOT use PostgreSQL-specific syntax.
6. Do NOT use DATE_TRUNC().
7. Do NOT use EXTRACT().
8. For month calculations in SQLite, use:
   DATE(event_date, 'start of month')
9. For extracting month numbers in SQLite, use:
   STRFTIME('%m', event_date)
10. If the question cannot be answered using the available data, clearly say so.
11. Return only the SQL query.
"""

    return prompt


if __name__ == "__main__":
    question = "Why did conversion rate drop in August?"
    prompt = build_prompt(question)
    print(prompt)
