
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import openai
import config

openai.api_key = config.openai_key
# openai_api_key = config.openai_key

users={}

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hi! I'm your AI assistant. Ask me anything and I'll respond within a few seconds!")

def respond(update, context):
    message = update.message.text
    name = update.message.from_user    
    print("\nPrompt-----------------------")
    print(name)
    print(message)
    
    ## get messages log for user
    username = name['username']
    messages = users.get(username, []) 
    if(len(messages) == 0):
        users[username]=messages
        
    new_message = {"role": "user", "content": message}
    print("new_message: ", new_message)
    
    ## add newest message to messages log. length capped at 10
    add_to_chatlog(username, new_message)
    
    max_tokens=1024
    
    ##get reseponse from openAI
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    
    total_tokens_used = completions['usage']['total_tokens']
    
    if total_tokens_used <= max_tokens:
        generated_text = completions.choices[0]["message"]["content"]
        print("\nResponse---------------------")
        print(generated_text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=generated_text, parse_mode="Markdown")
        
        ##add response to messages log
        add_to_chatlog(username, {"role": "assistant", "content": generated_text})
    else:
        max_tokens_msg = "Max tokens exceeded. Try again with a shorter prompt."
        print(max_tokens_msg)
        context.bot.send_message(chat_id=update.effective_chat.id, text=max_tokens_msg)
        
        ## clear chatlog for user, otherwise full chatlog will be sent to openAI, using up max tokens
        users[username] = []
    
    print("users: ", users)


def add_to_chatlog(username, message):
    user_messages = users[username]
    user_messages.append(message)
    
    if len(user_messages) >10:
        del user_messages[0]
    
    users[username] = user_messages

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