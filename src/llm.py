from openai import OpenAI
from prompt import build_prompt

client = OpenAI()


def generate_sql(user_question):

    prompt = build_prompt(user_question)

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":

    question = "Why did conversion rate drop in August?"

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)
