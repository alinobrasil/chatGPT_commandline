
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import openai
import config

openai.api_key = config.openai_key
# openai_api_key = config.openai_key

users={}
max_tokens=2048

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hi! I'm your AI assistant. Ask me anything and I'll respond within a few seconds!")

def respond(update, context):
    message = update.message.text
    name = update.message.from_user    
    
    if get_word_count(message) < max_tokens/2:
        ## if message is short enough, send to openAI
    
        print("\n\nPrompt-----------------------")
        print(name)
        print()
        print(message)
        
        ## get messages log for user. Initialize as blank if needed.
        username = name['username']
        messages = users.get(username, []) 
        if(len(messages) == 0):
            users[username]=messages

        new_message = {"role": "user", "content": message}
        # print("\nnew_message: ", new_message)
        
        ## add newest message to messages log. length capped at 10
        add_to_chatlog(username, new_message)

        try:
            ## The API Call: get reseponse from openAI.
            completions = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.7,
            )
        except Exception as e:
            print("Exception: ", e)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Oops, I'm having trouble responding. Can you try again?")
            return
        
        total_tokens_used = completions['usage']['total_tokens']
        print("\ntotal_tokens_used: ", total_tokens_used)
        
        # if total_tokens_used <= max_tokens:
        generated_text = completions.choices[0]["message"]["content"]
        
        print("\nResponse---------------------")
        print(generated_text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=generated_text, parse_mode="Markdown")
        
        
        add_to_chatlog(username, {"role": "assistant", "content": generated_text})
       
        print("\n\nActive users: ", users.keys())
        print()
    else:
        alert_text="That message was too long for me to process. Can you try to shorten it to about 1000 words?"
        print("\n", alert_text, "\n")
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=alert_text, 
                                 parse_mode="Markdown")


def add_to_chatlog(username, message):
    user_messages = users[username]
    user_messages.append(message)
    
    ## delete the first 2 messages if there are more than 10
    if len(user_messages) >10:
        print("\nRemoving older message from chat log...")
        user_messages = user_messages[1:]

    ## setting max size to half of max_tokens. Keep removing first element whie size is greater than max_tokens/2
    word_count = count_words_in_array(user_messages)
    print("\nword_count: ", word_count)
    
    while word_count > max_tokens/2:
        print("\nRemoving older message from chat log...")
        user_messages = user_messages[1:]
        word_count = count_words_in_array(user_messages)
        print("\nword_count: ", word_count)
    
    users[username] = user_messages

def count_words_in_array(messages):
    word_count = 0
    for message in messages:
        text = message.get('content', '')
        words = text.split()
        word_count += len(words)
    return word_count

def get_word_count(string):
    words = string.split()
    return len(words)

def main():
    updater = Updater(token=config.telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    respond_handler = MessageHandler(Filters.text, respond)
    dispatcher.add_handler(respond_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()