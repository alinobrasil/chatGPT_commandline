import openai
import config

# set the API key
openai.api_key = config.openai_key

# set the model to use (e.g. "text-davinci-002")
model = "gpt-4"
# "text-davinci-003"

prompt = ""

while prompt != "quit()":
        

    # set the prompt
    prompt = input("\nAsk me anything. Type quit() to terminate: ")

    # generate text
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1,
    )

    # print the generated text
    generated_text = completions.choices[0].text
    print(generated_text)
