import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    AIORateLimiter,
)
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# بيانات الدروس
fields = {
    "2d3d": {
        "title": "2D & 3D",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: مقدمة في التصميم {'ثنائي' if i <= 5 else 'ثلاثي'} الأبعاد",
                "video": f"https://www.youtube.com/watch?v={'Pz75QUo7K5M' if i == 1 else 'LtZg_dvJAFQ' if i == 2 else 'ihQOj7J5RZY' if i == 3 else 'NLZMWT2lKRM' if i == 4 else 'SOFFAHgYLCU' if i == 5 else 'aAQGgH5-2Rs' if i == 6 else '8Y1VR7LOgR0' if i == 7 else 'r0N0nLPVwbA' if i == 8 else '8_gEF9jzWzY' if i == 9 else '8CxeqNQ3S3g'}",
                "pdf": f"https://www.cs.cmu.edu/~15495/handouts/3d_graphics_tutorial.pdf"
            } for i in range(1, 11)
        }
    },
    "algorithms": {
        "title": "الخوارزميات",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مقدمة في الخوارزميات' if i == 1 else 'مفاهيم أساسية' if i == 2 else 'أنواع الخوارزميات' if i == 3 else 'خوارزميات الفرز' if i == 4 else 'خوارزميات البحث' if i == 5 else 'التحليل الزمني' if i == 6 else 'التحليل المكاني' if i == 7 else 'البرمجة الديناميكية' if i == 8 else 'خوارزميات الرسم البياني' if i == 9 else 'خوارزميات متقدمة'}",
                "video": f"https://www.youtube.com/watch?v={'fNZzQZgDyWc' if i == 1 else 'aK2Q5F1JpPQ' if i == 2 else 'ImtZ5yENzgE' if i == 3 else 'kgBjXUE_Nwc' if i == 4 else 'coQ5dg8wM2o' if i == 5 else 'aivIekQBT3I' if i == 6 else 'E7F8pNH84Ck' if i == 7 else 'FhQvxU_f2Aw' if i == 8 else 'ZmP3x9kA3rI' if i == 9 else '0bJrUUGTt8I'}",
                "pdf": f"https://cses.fi/book/book.pdf"
            } for i in range(1, 11)
        }
    },
    "data_modeling": {
        "title": "نمذجة البيانات",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مقدمة في نمذجة البيانات' if i == 1 else 'مفاهيم الكيانات' if i == 2 else 'العلاقات والخصائص' if i == 3 else 'المخططات ER' if i == 4 else 'التحويل إلى قواعد بيانات' if i == 5 else 'نمذجة البيانات العلائقية' if i == 6 else 'القيود والمعايير' if i == 7 else 'التكرار والاعتمادية' if i == 8 else 'نمذجة البيانات المتقدمة' if i == 9 else 'تصميم قواعد البيانات'}",
                "video": f"https://www.youtube.com/watch?v={'k2Oqtv1jRUI' if i == 1 else '8r6sK5TEXsg' if i == 2 else 'Xqz4MyGQwSc' if i == 3 else 'q_YcWyHRw3Q' if i == 4 else '5fJGr7Pb49g' if i == 5 else 'lvtFK_mzJfc' if i == 6 else 'KxvVKZpF6kw' if i == 7 else 'SlhZBbnY3j8' if i == 8 else 'GHkw1Fq8J0I' if i == 9 else 'IRkGxeTFdTE'}",
                "pdf": f"https://mohamedrabeea.net/books/book1_3521.pdf"
            } for i in range(1, 11)
        }
    },
    "env_setup": {
        "title": "تحضير بيئة التنفيذ",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مقدمة حول بيئة التطوير' if i == 1 else 'تثبيت الأدوات الأساسية' if i == 2 else 'إعداد VS Code' if i == 3 else 'تهيئة بايثون' if i == 4 else 'إعداد المشاريع' if i == 5 else 'نظام التحكم بالإصدارات' if i == 6 else 'Git و GitHub' if i == 7 else 'تنظيم الملفات' if i == 8 else 'إعداد بيئة افتراضية' if i == 9 else 'حل المشكلات التقنية'}",
                "video": f"https://www.youtube.com/watch?v={'nxDPZbR_GjQ' if i == 1 else 'TmlkO36vJYY' if i == 2 else 'r_lK_j8vT-Q' if i == 3 else 'tLKnG2zDzdI' if i == 4 else 'hJWvbxEoy2g' if i == 5 else 'AXWjivTJ4vc' if i == 6 else 'RGOj5yH7evk' if i == 7 else 'RU2uG-WCX5M' if i == 8 else 'DLX62G4lc44' if i == 9 else 'U6kBX7PHeLk'}",
                "pdf": f"https://www.cs.cmu.edu/~15131/resources/setup.pdf"
            } for i in range(1, 11)
        }
    }
}

# القوائم التفاعلية
def main_menu():
    keyboard = [[InlineKeyboardButton(v["title"], callback_data=k)] for k, v in fields.items()]
    return InlineKeyboardMarkup(keyboard)

def lessons_menu(field_key):
    field = fields[field_key]
    keyboard = [
        [InlineKeyboardButton(lesson["text"].split(":")[0], callback_data=k)]
        for k, lesson in field["lessons"].items()
    ]
    keyboard.append([InlineKeyboardButton("رجوع", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك في بوت تطوير المهارات!\nاختر أحد الأقسام:", reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data in fields:
        await query.edit_message_text(
            f"اختر درسًا من قسم {fields[data]['title']}:",
            reply_markup=lessons_menu(data)
        )
    elif data == "back_to_main":
        await query.edit_message_text("اختر أحد الأقسام:", reply_markup=main_menu())
    else:
        for field in fields.values():
            if data in field["lessons"]:
                lesson = field["lessons"][data]
                buttons = []
                if "video" in lesson:
                    buttons.append([InlineKeyboardButton("مشاهدة الفيديو", url=lesson["video"])])
                if "pdf" in lesson:
                    buttons.append([InlineKeyboardButton("تحميل PDF", url=lesson["pdf"])])
                buttons.append([InlineKeyboardButton("رجوع", callback_data="back_to_main")])
                await query.edit_message_text(
                    text=lesson.get("text", "لا يوجد شرح نصي."),
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                break

# تشغيل التطبيق باستخدام Polling
if __name__ == "__main__":
    telegram_app = Application.builder().token(BOT_TOKEN).rate_limiter(AIORateLimiter()).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CallbackQueryHandler(button_handler))
    telegram_app.run_polling()
