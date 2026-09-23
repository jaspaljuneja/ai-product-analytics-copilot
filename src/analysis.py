from openai import OpenAI
from business_definitions import BUSINESS_DEFINITIONS
import json

client = OpenAI()


def generate_insight(user_question, sql, columns, results):

    results_text = "\n".join(
        str(dict(zip(columns, row)))
        for row in results
    )

    prompt = f"""
You are an AI Product Analytics Copilot.

Your job is to explain data analysis results to a business user.

BUSINESS DEFINITIONS:
{BUSINESS_DEFINITIONS}

USER QUESTION:
{user_question}

SQL USED:
{sql}

QUERY RESULTS:
{results_text}

INSTRUCTIONS:
1. Answer the user's question using only the SQL results provided.
2. Do not invent facts or numbers.
3. Identify the most important business finding.
4. Include relevant metrics and percentage-point changes.
5. Identify important segments when the data supports it.
6. Clearly distinguish facts from possible explanations.
7. If the data does not support a conclusion, say so.
8. Keep the language concise and business-friendly.

Return ONLY valid JSON in this exact structure:

{{
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
    "confidence": "High/Medium/Low"
}}
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return json.loads(response.output_text)


if __name__ == "__main__":

    question = "Why did conversion rate drop in August?"

    sql = """
    SELECT
        'July' AS month,
        18.94 AS conversion_rate
    UNION ALL
    SELECT
        'August',
        9.77;
    """

    columns = ["month", "conversion_rate"]

    results = [
        ("July", 18.94),
        ("August", 9.77)
    ]

    insight = generate_insight(
        question,
        sql,
        columns,
        results
    )

    print("\nBusiness Insight:\n")
    print(json.dumps(insight, indent=2))
