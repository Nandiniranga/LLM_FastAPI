import openai

# Set up your OpenAI API key
openai.api_key = "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"

def query_llm(content: dict, user_query: str):
    prompt = f"""
    Content: {content}
    Query: {user_query}
    Provide a structured JSON response including:
    - summary
    - key_points (if applicable)
    """
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()
