from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, filters
from chesscombot import *

STATSEEKER = range(1)


TOKEN: Final = '6718024001:AAEDqgn8VljKmzonf29ScSXeUHT_SSbKh_w'
BOT_USERNAME: Final = '@chess_statsseekerbot'

async def start_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Please provide me the username')
    return STATSEEKER


async def stat_seeker(update: Update, context = ContextTypes.DEFAULT_TYPE):
    username = update.message.text
    take_data(username)
    if take_data(username) != False:
        await update.message.reply_photo(f'./{username}.png')
        await update.message.reply_text('Here you are :)')
        os.remove(f'./{username}.png')
    else:
        await update.message.reply_text('There is no user with provided name')
    return ConversationHandler.END

async def help_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Currently you can do: \n- /start - check the stats of user on chess.com \n- /help - get list of all the commands')

async def handle_response(text: str):

    return 'Please type /start to get me to work'

async def cancel(update: Update, context = ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END


async def handle_message(update: Update, context = ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) | {message_type} | {update.message.text}')

    response: str = handle_response(text)
    print(f"BOT | {response}")
    await update.message.reply_text(response)

async def error(update: Update, context = ContextTypes.DEFAULT_TYPE):
    print(f"Update {Update} | Error: {context.error}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('help', help_command))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            STATSEEKER: [MessageHandler(filters.TEXT, stat_seeker)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling(poll_interval=1)
    app.error_handlers(error)