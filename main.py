import argparse, json, logging, os, openai, requests
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') or exit("🚨Error: TELEGRAM_TOKEN is not set.")
openai.api_key = os.getenv('OPENAI_API_KEY') or None
SESSION_DATA = {}

def load_configuration():
    with open('configuration.json', 'r') as file:
        return json.load(file)

def get_session_id(func):
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        session_id = str(update.effective_chat.id if update.effective_chat.type in ['group', 'supergroup'] else update.effective_user.id)
        return await func(update, context, session_id, *args, **kwargs)
    return wrapper

def initialize_session_data(func):
    async def wrapper(update: Update, context: CallbackContext, session_id, *args, **kwargs):
        if session_id not in SESSION_DATA:
            logging.debug(f"Initializing session data for session_id={session_id}")
            SESSION_DATA[session_id] = load_configuration()['default_session_values']
        else:
            logging.debug(f"Session data already exists for session_id={session_id}")
        logging.debug(f"SESSION_DATA[{session_id}]: {SESSION_DATA[session_id]}")
        return await func(update, context, session_id, *args, **kwargs)
    return wrapper

def check_api_key(func):
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if not openai.api_key:
            await update.message.reply_text("⚠️Please configure your OpenAI API Key: /set openai_api_key THE_API_KEY")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def relay_errors(func):
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            await update.message.reply_text(f"An error occurred. e: {e}")
    return wrapper

@relay_errors
@get_session_id
@initialize_session_data
@check_api_key
async def handle_message(update: Update, context: CallbackContext, session_id):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    session_data = SESSION_DATA[session_id]
    if update.message.photo and session_data['model'] == "gpt-4-vision-preview":
        photo = update.message.photo[-1]
        photo_file = await context.bot.get_file(photo.file_id)
        photo_url = photo_file.file_path
        caption = update.message.caption or "Describe this image."
        session_data['chat_history'].append({
            "role": "user",
            "content": [
                {"type": "text", "text": caption},
                {"type": "image_url", "image_url": photo_url}
            ]
        })
    else:
        user_message = update.message.text
        session_data['chat_history'].append({
            "role": "user",
            "content": user_message
        })
    messages_for_api = [message for message in session_data['chat_history']]
    response = await response_from_openai(
        session_data['model'], 
        messages_for_api, 
        session_data['temperature'], 
        session_data['max_tokens']
    )
    session_data['chat_history'].append({
        'role': 'assistant',
        'content': response
    })
    await update.message.reply_markdown(response)

async def response_from_openai(model, messages, temperature, max_tokens):
    params = {'model': model, 'messages': messages, 'temperature': temperature}
    if model == "gpt-4-vision-preview": 
        max_tokens = 4096
    if max_tokens is not None: 
        params['max_tokens'] = max_tokens
    return openai.chat.completions.create(**params).choices[0].message.content

async def command_start(update: Update, context: CallbackContext):
    await update.message.reply_text("ℹ️Welcome! Go ahead and say something to start the conversation. More features can be found in this command: /help")

@get_session_id
async def command_reset(update: Update, context: CallbackContext, session_id):
    if session_id in SESSION_DATA:
        del SESSION_DATA[session_id]
        await update.message.reply_text("ℹ️All settings have been reset.")
    await update.message.reply_text("ℹ️No session data to reset.") 

@get_session_id
async def command_clear(update: Update, context: CallbackContext, session_id):
    if session_id in SESSION_DATA:
        SESSION_DATA[session_id]['chat_history'] = []
        await update.message.reply_text("ℹ️Chat history is now empty!")
    else:
        logging.warning(f"No session data found for session_id={session_id}")

def update_session_preference(session_id, preference, value):
    if session_id in SESSION_DATA:
        SESSION_DATA[session_id][preference] = value
        logging.debug(f"Updated {preference} for session_id={session_id}: {value}")
    else:
        logging.warning(f"Tried to update preference for non-existing session_id={session_id}")

@get_session_id
@initialize_session_data
async def command_set(update: Update, context: CallbackContext, session_id):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️Please specify what to set (model, temperature, system_prompt, max_tokens, openai_api_key).")
        return
    preference, *rest = args
    preference = preference.lower()
    value = ' '.join(rest)
    valid_models = load_configuration()['valid_models']
    if preference == 'model':
        if not value:
            model_list = "\n".join(f"{model}: {', '.join(shorthand)}" for model, shorthand in valid_models.items())
            await update.message.reply_text(f"Available models:\n{model_list}")
            return
        if value in sum(valid_models.values(), []):
            actual_model = next(m for m in valid_models if value in valid_models[m])
            update_session_preference(session_id, 'model', actual_model)
            await command_clear(update, context)
            logging.debug(f"After model update, SESSION_DATA[{session_id}]: {SESSION_DATA[session_id]}")
            await update.message.reply_text(f"✅Model set to {actual_model}.")
        else:
            await update.message.reply_text("⚠️Invalid model. Please choose from the available models.")
        return
    if preference == 'openai_api_key':
        openai.api_key = value
        await update.message.reply_text("✅OpenAI API key has been set.")
    elif preference == 'temperature':
        try:
            temperature = float(value)
            if 0 <= temperature <= 2.0:
                update_session_preference(session_id, 'temperature', temperature)
                await update.message.reply_text(f"✅Temperature set to {value}.")
            else:
                raise ValueError
        except ValueError:
            await update.message.reply_text("⚠️Invalid temperature. Please provide a value between 0.0 and 2.0.")
    elif preference == 'system_prompt':
        update_session_preference(session_id, 'system_prompt', value)
        await update.message.reply_text("✅System prompt updated.")
    elif preference == 'max_tokens':
        if value.isdigit():
            update_session_preference(session_id, 'max_tokens', int(value))
            await update.message.reply_text(f"✅Max tokens set to {value}.")
        else:
            await update.message.reply_text("⚠️Invalid max tokens. Please provide a numeric value.")
    else:
        await update.message.reply_text("⚠️Invalid setting or value.")

@get_session_id
async def command_show(update: Update, context: CallbackContext, session_id):
    session_data = SESSION_DATA.get(session_id, {})
    message = "**Session Data:**\n"
    if not session_data:
        message += "Session data not initialized, yet.\n"
    else:
        preferences = {k: v for k, v in session_data.items() if k != 'chat_history'}
        for key, value in preferences.items():
            message += f"{key.capitalize()}: {value}\n"
    message += "\n**Chat History:**\n"
    if 'chat_history' in session_data and session_data['chat_history']:
        for chat in session_data['chat_history']:
            role = chat['role'].capitalize()
            content = chat['content']
            if isinstance(content, list):  # Handling gpt-4-vision-preview model message
                for item in content:
                    if item.get('type') == 'image_url':
                        message += f"  {role}: <Image sent>\n"
                    elif 'text' in item:
                        message += f"  {role}: {item['text']}\n"
            else:
                message += f"  {role}: {content}\n"
    else:
        message += "No chat history available."
    max_length = 4096
    message_chunks = [message[i:i + max_length] for i in range(0, len(message), max_length)]
    for chunk in message_chunks:
        await update.message.reply_text(chunk)

async def command_help(update: Update, context: CallbackContext):
    commands = [
        ("/reset", "Reset settings"),
        ("/clear", "Clean up chat history"),
        ("/set", "Change settings"),
        ("/show", "Show session data and chat history"),
        ("/help", "Command list"),
    ]
    help_text = "<b>📚 Usage Commands:</b>\n"
    for command, description in commands:
        help_text += f"<code>{command}</code> - {description}\n"
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

def register_handlers(application):
    application.add_handlers(handlers={ 
        -1: [
            CommandHandler('start', command_start),
            CommandHandler('reset', command_reset),
            CommandHandler('clear', command_clear),
            CommandHandler('set', command_set),
            CommandHandler('show', command_show),
            CommandHandler('help', command_help)
        ],
        1: [MessageHandler(filters.ALL & (~filters.COMMAND), handle_message)]
    })

def railway_dns_workaround():
    from time import sleep
    sleep(1.3)
    for _ in range(3):
        if requests.get("https://api.telegram.org", timeout=3).status_code == 200:
            print("The api.telegram.org is reachable.")
            return
        print(f'The api.telegram.org is not reachable. Retrying...({_})')
    print("Failed to reach api.telegram.org after 3 attempts.")

def main():
    parser = argparse.ArgumentParser(description="Run the Telegram bot.")
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.disable(logging.WARNING)
    railway_dns_workaround()
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    register_handlers(application)
    try:
        print("The Telegram Bot will now be running in long polling mode.")
        application.run_polling()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
