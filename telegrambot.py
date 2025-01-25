from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from transformers import pipeline
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load the TinyLlama model
logger.info("Loading TinyLlama model...")
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
logger.info("TinyLlama model loaded successfully.")

# Handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    logger.info("User issued /start command")
    await update.message.reply_text("Hello! I'm your AI Assistant bot. How can I help you?")

# Process user messages
async def process(update: Update, context: CallbackContext) -> None:
    try:
        user_message = update.message.text.strip()
        logger.info(f"User message received: {user_message}")

        # Create a structured prompt for TinyLlama
        prompt = f"""Q: {user_message}
A:"""
        
        # Generate a response using TinyLlama
        response = pipe(
            prompt,
            max_length=300,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,  # Enable sampling
            truncation=True,  # Enable truncation
        )
        bot_response = response[0]['generated_text'].split("A:")[-1].strip()  # Extract the answer part

        logger.info(f"Bot response: {bot_response}")
        await update.message.reply_text(bot_response)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

# Main function to start the bot
def main() -> None:
    API_token = "8036261038:AAE-b1tRGI9xt4ZRiwTxFT78LsMWOwVgN30"  # Replace with your bot's API token
    application = Application.builder().token(API_token).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process))

    logger.info("Aditi's AI Assistant Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()