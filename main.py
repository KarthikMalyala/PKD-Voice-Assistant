import asyncio
import re
from EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = Chatbot(cookiePath='cookies.json')
    response = await bot.ask(prompt=input("Ask Bing!"), conversation_style=ConversationStyle.precise)

    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]

    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
    # Select only the bot response from the response dictionary
    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]
    # Remove [^#^] citations in response
    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
    print("Bot's Response:",bot_response)
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

