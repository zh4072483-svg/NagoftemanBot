import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        target_id = context.args[0]
        context.user_data["target_id"] = target_id
        await update.message.reply_text(
            "پیامت رو بفرست 🕊\n"
            "پیامت بدون نمایش نام فرستنده برای صاحب لینک ارسال میشه."
        )
    else:
        link = f"https://t.me/{context.bot.username}?start={update.effective_user.id}"
        await update.message.reply_text(
            "سلام 🕊\n"
            "لینک ناشناس خودت:\n\n"
            f"{link}\n\n"
            "این لینک رو برای دوستات بفرست."
        )


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_id = context.user_data.get("target_id")

    if not target_id:
        await update.message.reply_text(
            "اول از لینک اختصاصی یک نفر وارد بات شو 🕊"
        )
        return

    try:
        await context.bot.copy_message(
            chat_id=int(target_id),
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )

        await update.message.reply_text("پیامت با موفقیت ناشناس ارسال شد 🕊")

    except Exception:
        await update.message.reply_text(
            "ارسال پیام انجام نشد. ممکنه صاحب لینک هنوز بات رو شروع نکرده باشه."
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, receive_message))

    print("NagoftemanBot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
