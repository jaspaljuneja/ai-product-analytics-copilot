from llm import generate_sql
from database import run_sql
from analysis import generate_insight
import json


def ask_copilot(question):

    print("\nUser question:")
    print(question)

    print("\nGenerating SQL...")
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    print("\nExecuting SQL...")
    columns, results = run_sql(sql)

    print("\nGenerating business insight...")

    insight = generate_insight(
        user_question=question,
        sql=sql,
        columns=columns,
        results=results
    )

    print("\nBusiness Insight:")
    print(json.dumps(insight, indent=2))
    return insight

if __name__ == "__main__":
    question = "Why did conversion rate drop in August?"
    ask_copilot(question)
