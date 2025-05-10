import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تحميل متغيرات البيئة
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# تحميل بيانات الدروس من ملف JSON
with open("resources.json", "r", encoding="utf-8") as file:
    lesson_data = json.load(file)

# مثال على أمر بدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسل /2d3d لعرض دروس التصميم.")

# أمر يعرض دروس التصميم مثلًا
async def lessons_2d3d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    section = lesson_data.get("2d3d", {})
    message = section.get("title", "") + "\n\n"
    for key, lesson in section.get("lessons", {}).items():
        message += f"{lesson['text']}\n"
        message += f"فيديو: {lesson['video']}\n"
        message += f"PDF: {lesson['pdf']}\n\n"
    await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("2d3d", lessons_2d3d))
    
    app.run_polling()
