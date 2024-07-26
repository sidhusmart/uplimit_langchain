import asyncio
import aiohttp
import langchain_rag_app

async def telegram_bot_response():
    import os
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
    os.environ['LANGCHAIN_API_KEY'] = "ENTER LANGCHAIN API KEY"
    os.environ['LANGCHAIN_PROJECT'] = "ENTER LANGCHAIN PROJECT"
    bot_token = 'ENTER YOUR BOT TOKEN HERE'
    api_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    send_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    offset = None  # Variable to manage the offset of updates

    async with aiohttp.ClientSession() as session:
        while True:
            # Adjust the API URL to include the offset
            request_url = f"{api_url}?offset={offset}" if offset else api_url

            async with session.get(request_url) as response:
                updates = await response.json()
                if updates['result']:
                    for update in updates['result']:
                        last_update_id = update['update_id']
                        chat_id = update['message']['chat']['id']
                        incoming_message = update['message']['text']
                        outgoing_message = ""
                        if (incoming_message == "/start"):
                            outgoing_message = "Hi there! I'm Pillpal and I'm ready to help you with any queries on your pills"
                        else:
                            outgoing_message = langchain_rag_app.provide_bot_response(incoming_message)
                        message = outgoing_message

                        payload = {
                            'chat_id': chat_id,
                            'text': message
                        }
                        async with session.post(send_url, data=payload) as send_response:
                            print("Message sent:", await send_response.text())

                        # Update the offset to only receive new messages next time
                        offset = last_update_id + 1

            # Sleep for a short period to avoid hitting the API rate limit
            await asyncio.sleep(1)

# Run the bot response function
asyncio.run(telegram_bot_response())
