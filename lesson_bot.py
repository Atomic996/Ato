import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, JobQueue
)
from dotenv import load_dotenv
from datetime import time

logging.basicConfig(level=logging.INFO)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN غير موجود في .env")

lesson_data = {
    "2d3d": {
        "title": "🎨 2D & 3D",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: مقدمة في التصميم {'ثنائي' if i <=5 else 'ثلاثي'} الأبعاد",
                "video": f"https://youtu.be/{['Pz75QUo7K5M','LtZg_dvJAFQ','ihQOj7J5RZY','NLZMWT2lKRM','SOFFAHgYLCU','aAQGgH5-2Rs','8Y1VR7LOgR0','r0N0nLPVwbA','8_gEF9jzWzY','8CxeqNQ3S3g'][i-1]}",
                "pdf": f"https://drive.example.com/pdf/{['2d_1','2d_2','2d_3','2d_4','2d_5','3d_6','3d_7','3d_8','3d_9','3d_10'][i-1]}.pdf"
            } for i in range(1, 11)
        }
    }
}

def generate_main_menu():
    buttons = [[InlineKeyboardButton(data["title"], callback_data=key)] for key, data in lesson_data.items()]
    return InlineKeyboardMarkup(buttons)

def generate_lessons_menu(section_key):
    lessons = lesson_data[section_key]["lessons"]
    buttons = [
        [InlineKeyboardButton(lesson["text"], callback_data=lesson_key)]
        for lesson_key, lesson in lessons.items()
    ]
    buttons.append([InlineKeyboardButton("↩️ رجوع", callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)

async def show_lesson_details(query):
    lesson = next(
        (lesson for field in lesson_data.values() for lesson_key, lesson in field["lessons"].items() if lesson_key == query.data),
        None
    )
    if lesson:
        buttons = [
            [InlineKeyboardButton("▶️ مشاهدة", url=lesson["video"])],
            [InlineKeyboardButton("📖 ملاحظات", url=lesson["pdf"])],
            [InlineKeyboardButton("↩️ رجوع", callback_data="main_menu")]
        ]
        await query.edit_message_text(lesson["text"], reply_markup=InlineKeyboardMarkup(buttons))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data.setdefault("active_users", set()).add(update.effective_chat.id)
    await update.message.reply_text("مرحبا بك في منصة التعلم التفاعلي!", reply_markup=generate_main_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(cache_time=1)
    data = query.data
    if data == "main_menu":
        await query.edit_message_text("اختر مجال التعلم:", reply_markup=generate_main_menu())
    elif data in lesson_data:
        await query.edit_message_text(
            f"{lesson_data[data]['title']} - اختر درسًا:",
            reply_markup=generate_lessons_menu(data)
        )
    else:
        await show_lesson_details(query)

async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    for user_id in context.bot_data.get("active_users", set()):
        try:
            await context.bot.send_message(chat_id=user_id, text="لا تنسَ متابعة دروسك اليوم!")
        except Exception as e:
            logging.error(f"خطأ في إرسال التذكير إلى {user_id}: {e}")

async def init(application: Application) -> None:
    application.bot_data.setdefault("active_users", set())

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).post_init(init).build()
    job_queue = app.job_queue
    job_queue.run_daily(daily_reminder, time=time(hour=18))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()