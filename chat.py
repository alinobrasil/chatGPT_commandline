import openai
import config

mykey = input("\n\n****enter your API key: ")

# set the API key
openai.api_key = mykey

# set the model to use (e.g. "text-davinci-002")
model = "text-davinci-003"

prompt = ""

while prompt != "quit()":
        

    # set the prompt
    prompt = input("\n\n****Ask me anything. Type quit() to terminate:       ")
    try:
        if prompt != "":
            # generate text
            completions = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )

            # print the generated text
            generated_text = completions.choices[0].text
            print(generated_text)
    except openai.error.AuthenticationError:
        print("\n****Api error")
        mykey = input("Enter your API key again: ")
        openai.api_key = mykey
    # endif
