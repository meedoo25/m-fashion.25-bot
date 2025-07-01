from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
import os

NAME, PHONE, CIN, WILAYA, ID_CARD = range(5)

ADMIN_IDS = [6244970377]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا بك! من فضلك أرسل اسمك الكامل للبدء بالتسجيل.", reply_markup=ReplyKeyboardRemove())
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("أدخل رقم هاتفك:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("أدخل رقم بطاقة تعريفك:")
    return CIN

async def get_cin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cin"] = update.message.text
    await update.message.reply_text("أدخل ولايتك:")
    return WILAYA

async def get_wilaya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wilaya"] = update.message.text
    await update.message.reply_text("أرسل الآن صورة بطاقة تعريفك كصورة (وليس ملف).")
    return ID_CARD

async def get_id_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("من فضلك أرسل بطاقة التعريف على شكل صورة.")
        return ID_CARD

    photo_file = await update.message.photo[-1].get_file()
    context.user_data["photo"] = photo_file.file_id
    user_id = update.effective_user.id

    message = (
        f"طلب تسجيل جديد:
"
        f"الاسم: {context.user_data['name']}
"
        f"الهاتف: {context.user_data['phone']}
"
        f"رقم التعريف: {context.user_data['cin']}
"
        f"الولاية: {context.user_data['wilaya']}
"
        f"user_id: {user_id}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("قبول", callback_data=f"accept_{user_id}"),
         InlineKeyboardButton("رفض", callback_data=f"reject_{user_id}")]
    ])

    for admin_id in ADMIN_IDS:
        await context.bot.send_photo(chat_id=admin_id, photo=context.user_data["photo"], caption=message, reply_markup=keyboard)

    await update.message.reply_text("تم إرسال معلوماتك. سيتم الرد بعد مراجعتها.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.run_polling()
