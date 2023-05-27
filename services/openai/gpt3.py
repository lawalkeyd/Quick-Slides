import openai

from QuickSlides.settings import OPENAI_KEY

openai.api_key = OPENAI_KEY
def summarize_text(text):
    # Call to OpenAI's API to summarize text
    # TODO: handle the exceptions correctly
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"{text}\n\nSummarize:",
      temperature=0.3,
      max_tokens=60
    )

    return response.choices[0].text.strip()