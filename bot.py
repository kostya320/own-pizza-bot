import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_CHAT_ID, CHANNEL_ID

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Отправь мне сообщение, которое хочешь предложить для публикации.\n\n"
        "Можно отправлять текст, фото, видео, документы и другие медиа!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📝 Как использовать бота:\n"
        "1. Отправь сообщение (текст, фото, видео и т.д.)\n"
        "2. Администратор рассмотрит твою заявку\n"
        "3. Если одобрят - сообщение опубликуют в канале"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех входящих сообщений"""
    user = update.effective_user
    message = update.message
    
    logger.info(f"Получено сообщение от @{user.username} (ID: {user.id})")
    
    # Пересылаем сообщение в админский чат
    try:
        # Отправляем информацию о пользователе
        user_info = f"👤 Пользователь: @{user.username or user.first_name}\n🆔 ID: {user.id}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=user_info)
        
        # Пересылаем оригинальное сообщение
        forwarded_message = await message.forward(chat_id=ADMIN_CHAT_ID)
        
        # Создаем кнопки для модерации
        keyboard = [
            [
                InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{forwarded_message.message_id}"),
                InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{forwarded_message.message_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем кнопки модерации
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="Выберите действие:",
            reply_markup=reply_markup
        )
        
        # Уведомляем пользователя
        await message.reply_text("📨 Ваше сообщение отправлено на модерацию. Ожидайте ответа!")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await message.reply_text("❌ Произошла ошибка при отправке сообщения. Попробуйте позже.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки модерации"""
    query = update.callback_query
    await query.answer()
    
    action, message_id = query.data.split('_', 1)
    message_id = int(message_id)
    
    try:
        if action == "approve":
            # Копируем сообщение в канал
            await context.bot.copy_message(
                chat_id=CHANNEL_ID,
                from_chat_id=ADMIN_CHAT_ID,
                message_id=message_id
            )
            await query.edit_message_text("✅ Сообщение одобрено и опубликовано в канале!")
            
        elif action == "reject":
            await query.edit_message_text("❌ Сообщение отклонено.")
            
    except Exception as e:
        logger.error(f"Ошибка при модерации: {e}")
        await query.edit_message_text("❌ Произошла ошибка при обработке.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    """Основная функция запуска бота"""
    # Создаем приложение бота
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.ALL, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()