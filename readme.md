Run your own personal gpt3.5 assistant in Telegram

Before you start:

Create a telegram bot by messaging @Botfather on telegram.
See the paragraph on "Creating  a new bot" here: https://core.telegram.org/bots/features#creating-a-new-bot
You'll need to obtain the tokenID to do step #2 below. 


1. install dependencies
```pip install -r requirements.txt```

2. set up config (fill in api key and telegram tokenID) in config.py

3. run the bot
```python telegrambot.py```

After that, just send a message to your bot and you should start getting responses from ChatGPT.
