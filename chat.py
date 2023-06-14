import openai
import config

# set the API key
openai.api_key = config.openai_key

# set the model to use (e.g. "text-davinci-002")
model = "gpt-3.5-turbo"

def ask_chatGPT(prompt):
    message = {"role": "user", "content": prompt}

    # generate text
    completions = openai.ChatCompletion.create(
        model=model,
        messages=[message],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1,
    )

    # print the generated text
    return completions.choices[0]["message"]["content"]
   
   
   
if __name__ == "__main__":
        
    prompt = ""
    while prompt != "quit()":

        # set the prompt
        prompt = input("\nAsk me anything. Type quit() to terminate: ")
        
        print(ask_chatGPT(prompt))
        
