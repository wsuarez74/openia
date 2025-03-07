import openai

def complete(text):
    openai.api_key = "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" 
    completion = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt="text",
        temperature=0,
        max_tokens=4000
    )
    return completion
response = complete("el mejor amigo del hombre")

print(response)
