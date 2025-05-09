import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    AIORateLimiter,
    JobQueue
)
from dotenv import load_dotenv

# تحميل بيانات التوكن من ملف البيئة
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
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
    },
    "algorithms": {
        "title": "🧠 الخوارزميات",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مقدمة في الخوارزميات' if i==1 else 'مفاهيم أساسية' if i==2 else 'أنواع الخوارزميات' if i==3 else 'خوارزميات الفرز' if i==4 else 'خوارزميات البحث' if i==5 else 'التحليل الزمني' if i==6 else 'التحليل المكاني' if i==7 else 'البرمجة الديناميكية' if i==8 else 'خوارزميات الرسم البياني' if i==9 else 'خوارزميات متقدمة'}",
                "video": f"https://youtu.be/{['fNZzQZgDyWc','aK2Q5F1JpPQ','ImtZ5yENzgE','kgBjXUE_Nwc','coQ5dg8wM2o','aivIekQBT3I','E7F8pNH84Ck','FhQvxU_f2Aw','ZmP3x9kA3rI','0bJrUUGTt8I'][i-1]}",
                "pdf": f"https://drive.example.com/pdf/{['algo_basics','algo_concepts','algo_types','algo_sorting','algo_searching','algo_time','algo_space','algo_dynamic','algo_graph','algo_advanced'][i-1]}.pdf"
            } for i in range(1, 11)
        }
    },
    "env_setup": {
        "title": "⚙️ تحضير بيئة التنفيذ",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مقدمة عامة' if i==1 else 'تنصيب الأدوات' if i==2 else 'إعداد المحرر' if i==3 else 'متطلبات النظام' if i==4 else 'بيئة افتراضية' if i==5 else 'تثبيت الحزم' if i==6 else 'إعداد متغيرات البيئة' if i==7 else 'تنظيم الملفات' if i==8 else 'تشغيل أول مشروع' if i==9 else 'حل المشاكل الشائعة'}",
                "video": f"https://youtu.be/{['env1','env2','env3','env4','env5','env6','env7','env8','env9','env10'][i-1]}",
                "pdf": f"https://drive.example.com/pdf/{['env_intro','env_tools','env_editor','env_requirements','env_virtualenv','env_packages','env_vars','env_structure','env_run','env_troubleshooting'][i-1]}.pdf"
            } for i in range(1, 11)
        }
    },
    "data_modeling": {
        "title": "🗂️ نمذجة البيانات",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مفاهيم النمذجة' if i==1 else 'الكيانات والصفات' if i==2 else 'العلاقات' if i==3 else 'ERD' if i==4 else 'أنواع العلاقات' if i==5 else 'المفتاح الأساسي' if i==6 else 'المفتاح الأجنبي' if i==7 else 'تحسين النموذج' if i==8 else 'النموذج المنطقي' if i==9 else 'النموذج الفيزيائي'}",
                "video": f"https://youtu.be/{['dm1','dm2','dm3','dm4','dm5','dm6','dm7','dm8','dm9','dm10'][i-1]}",
                "pdf": f"https://drive.example.com/pdf/{['dm_concepts','dm_entities','dm_relations','dm_erd','dm_types','dm_pk','dm_fk','dm_optimize','dm_logical','dm_physical'][i-1]}.pdf"
            } for i in range(1, 11)
        }
    },
    "project_mgmt": {
        "title": "📋 تسيير مشروع",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مقدمة في إدارة المشاريع' if i==1 else 'تحديد نطاق المشروع' if i==2 else 'تخطيط المهام' if i==3 else 'الجدولة الزمنية' if i==4 else 'تقدير الموارد' if i==5 else 'إدارة المخاطر' if i==6 else 'تتبع التقدم' if i==7 else 'إدارة الفريق' if i==8 else 'الاتصال والتقارير' if i==9 else 'إغلاق المشروع'}",
                "video": f"https://youtu.be/{['pm1','pm2','pm3','pm4','pm5','pm6','pm7','pm8','pm9','pm10'][i-1]}",
                "pdf": f"https://drive.example.com/pdf/{['pm_intro','pm_scope','pm_tasks','pm_schedule','pm_resources','pm_risks','pm_tracking','pm_team','pm_comms','pm_closure'][i-1]}.pdf"
            } for i in range(1, 11)
        }
    },
    "video_editing": {
        "title": "🎬 معالجة الفيديوهات",
        "lessons": {
            f"lesson{i}": {
                "text": f"الدرس {i}: {'مقدمة في تحرير الفيديو' if i==1 else 'قص ودمج المقاطع' if i==2 else 'إضافة تأثيرات' if i==3 else 'العمل مع الصوت' if i==4 else 'الكتابة على الفيديو' if i==5 else 'الفلاتر والانتقالات' if i==6 else 'التصدير بجودة عالية' if i==7 else 'تطبيقات الهاتف' if i==8 else 'استخدام الذكاء الاصطناعي' if i==9 else 'مشروع نهائي'}",
                "video": f"https://youtu.be/{['vid1','vid2','vid3','vid4','vid5','vid6','vid7','vid8','vid9','vid10'][i-1]}",
                "pdf": f"https://drive.example.com/pdf/{['vid_intro','vid_cut_merge','vid_effects','vid_audio','vid_text','vid_filters','vid_export','vid_mobile','vid_ai','vid_final'][i-1]}.pdf"
            } for i in range(1, 11)
        }
    }
}

def generate_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f["title"], callback_data=k)] 
        for k, f in lesson_data.items()
    ])

def generate_lessons_menu(field_key: str):
    field = lesson_data[field_key]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f"{i}. {lesson['text']}", 
            callback_data=lesson_id
        )] for i, (lesson_id, lesson) in enumerate(field["lessons"].items(), 1)
    ] + [[InlineKeyboardButton("🏠 الرئيسية", callback_data="main")]])

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبا بك في منصة التعلم التفاعلي!",
        reply_markup=generate_main_menu()
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "main":
        await query.edit_message_text(
            "اختر مجال التعلم:",
            reply_markup=generate_main_menu()
        )
    elif query.data in lesson_data:
        await show_lessons(query, query.data)
    else:
        await show_lesson_details(query)

async def show_lessons(query, field_key):
    await query.edit_message_text(
        f"دروس {lesson_data[field_key]['title']}:",
        reply_markup=generate_lessons_menu(field_key)
    )

async def show_lesson_details(query):
    lesson = next(
        (l for f in lesson_data.values() for l in f["lessons"].values() 
         if l.get("id") == query.data), None
    )
    if lesson:
        buttons = [
            [InlineKeyboardButton("▶️ مشاهدة", url=lesson["video"])],
            [InlineKeyboardButton("📖 ملاحظات", url=lesson["pdf"])]
        ]
        if lesson.get("quiz"):
            buttons.append([InlineKeyboardButton("📝 اختبار", callback_data=lesson["quiz"])])
        await query.edit_message_text(
            lesson["text"],
            reply_markup=InlineKeyboardMarkup(buttons)
        )

async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in context.bot_data.get("active_users", []):
        await context.bot.send_message(
            chat_id,
            "⏰ تذكير: لم تكمل دروسك اليومية بعد!"
        )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    # جدولة التذكيرات
    job_queue = app.job_queue
    job_queue.run_daily(daily_reminder, time=datetime.time(hour=18))
    
    # بدء التشغيل
    app.run_polling()
