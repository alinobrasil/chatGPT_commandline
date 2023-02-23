
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import openai
import config

openai.api_key = config.openai_key
# openai_api_key = config.openai_key

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm your GPT3 bot. Please enter your message to get a response from OpenAI's GPT3 engine.")

def respond(update, context):
    message = update.message.text
    name = update.message.from_user
    print("\nPrompt-----------------------")
    print(name)
    print(message)
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    generated_text = completions.choices[0].text
    print("\nResponse---------------------")
    print(generated_text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=generated_text)

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