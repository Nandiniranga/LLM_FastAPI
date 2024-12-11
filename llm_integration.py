import openai

# Set up your OpenAI API key
openai.api_key = ""

def query_llm(content: dict, user_query: str):
    prompt = f"""
    Content: {content}
    Query: {user_query}

    Please answer the query and format the response in the following JSON structure:
    {{
        "query": "<user's query>",
        "response": {{
            "summary": "<summary text>",
            "key_points": {{
                "revenue": "<value>",
                "net_income": "<value>"
            }}
        }}
    }}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",  # or your chosen model
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()
