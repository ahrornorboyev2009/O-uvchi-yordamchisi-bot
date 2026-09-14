import asyncio
import ast
import operator
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from config import BOT_TOKEN
from database import init_db, add_user, save_result, get_results


# =========================
# SOZLAMALAR
# =========================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# TEST SAVOLLARI
# =========================

QUIZ = [
    {
        "question": "5 + 7 nechiga teng?",
        "answers": ["10", "12", "14", "15"],
        "correct": "12",
    },
    {
        "question": "10 × 3 nechiga teng?",
        "answers": ["20", "25", "30", "35"],
        "correct": "30",
    },
    {
        "question": "100 ÷ 4 nechiga teng?",
        "answers": ["20", "25", "30", "40"],
        "correct": "25",
    },
    {
        "question": "15 - 8 nechiga teng?",
        "answers": ["5", "6", "7", "8"],
        "correct": "7",
    },
    {
        "question": "9 × 9 nechiga teng?",
        "answers": ["72", "81", "90", "99"],
        "correct": "81",
    },
]


# Foydalanuvchining test holati
user_quiz = {}


# =========================
# ASOSIY MENYU
# =========================

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Darslar"),
                KeyboardButton(text="📝 Test ishlash"),
            ],
            [
                KeyboardButton(text="🧮 Matematik yordam"),
                KeyboardButton(text="📊 Natijalarim"),
            ],
            [
                KeyboardButton(text="🔔 Eslatmalar"),
                KeyboardButton(text="ℹ️ Bot haqida"),
            ],
        ],
        resize_keyboard=True,
    )

    return keyboard


# =========================
# /START
# =========================

@dp.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user

    add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )

    await message.answer(
        f"Assalomu alaykum, {user.first_name}! 👋\n\n"
        "📚 O‘quvchi yordamchi botiga xush kelibsiz!\n\n"
        "Bu bot orqali:\n"
        "📚 Darslar bilan tanishishingiz\n"
        "📝 Test ishlashingiz\n"
        "🧮 Matematik misollarni hisoblashingiz\n"
        "📊 Natijalaringizni ko‘rishingiz\n"
        "🔔 Eslatma qo‘yishingiz mumkin.\n\n"
        "Kerakli bo‘limni menyudan tanlang 👇",
        reply_markup=main_menu(),
    )


# =========================
# 📚 DARSLAR
# =========================

@dp.message(F.text == "📚 Darslar")
async def lessons_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧮 Matematika",
                    callback_data="lesson_math",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💻 Informatika",
                    callback_data="lesson_it",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇬🇧 Ingliz tili",
                    callback_data="lesson_english",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📖 Ona tili",
                    callback_data="lesson_language",
                )
            ],
        ]
    )

    await message.answer(
        "📚 <b>Darslar bo‘limi</b>\n\n"
        "Kerakli fanni tanlang:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "lesson_math")
async def lesson_math(callback: CallbackQuery):
    await callback.message.answer(
        "🧮 <b>Matematika</b>\n\n"
        "Matematika bo‘yicha asosiy mavzular:\n\n"
        "➕ Qo‘shish\n"
        "➖ Ayirish\n"
        "✖️ Ko‘paytirish\n"
        "➗ Bo‘lish\n"
        "📐 Geometriya\n"
        "📊 Foizlar\n\n"
        "Misol yechish uchun 🧮 Matematik yordam tugmasidan foydalaning.",
        parse_mode="HTML",
    )

    await callback.answer()


@dp.callback_query(F.data == "lesson_it")
async def lesson_it(callback: CallbackQuery):
    await callback.message.answer(
        "💻 <b>Informatika</b>\n\n"
        "Informatika bo‘yicha:\n\n"
        "🐍 Python\n"
        "🌐 HTML\n"
        "🎨 CSS\n"
        "🗄 Ma’lumotlar bazasi\n"
        "🤖 Telegram botlar\n\n"
        "Keyingi versiyalarda batafsil darslar qo‘shamiz.",
        parse_mode="HTML",
    )

    await callback.answer()


@dp.callback_query(F.data == "lesson_english")
async def lesson_english(callback: CallbackQuery):
    await callback.message.answer(
        "🇬🇧 <b>Ingliz tili</b>\n\n"
        "Ingliz tilini o‘rganish uchun:\n\n"
        "🔤 Lug‘at\n"
        "📖 Grammatika\n"
        "💬 Kundalik iboralar\n"
        "📝 Testlar\n\n"
        "Keyingi versiyalarda darslar kengaytiriladi.",
        parse_mode="HTML",
    )

    await callback.answer()


@dp.callback_query(F.data == "lesson_language")
async def lesson_language(callback: CallbackQuery):
    await callback.message.answer(
        "📖 <b>Ona tili</b>\n\n"
        "Ona tili bo‘yicha:\n\n"
        "🔤 Imlo\n"
        "📚 So‘z turkumlari\n"
        "📝 Gap tuzilishi\n"
        "📖 Adabiyot\n\n"
        "Keyingi versiyalarda yangi mavzular qo‘shamiz.",
        parse_mode="HTML",
    )

    await callback.answer()


# =========================
# 📝 TEST BOSHLASH
# =========================

@dp.message(F.text == "📝 Test ishlash")
async def test_handler(message: Message):
    user_id = message.from_user.id

    user_quiz[user_id] = {
        "question": 0,
        "score": 0,
    }

    await send_question(message, user_id)


async def send_question(message: Message, user_id: int):
    data = user_quiz[user_id]
    question_number = data["question"]

    if question_number >= len(QUIZ):
        score = data["score"]
        total = len(QUIZ)

        save_result(
            user_id=user_id,
            subject="Matematika",
            score=score,
            total=total,
        )

        del user_quiz[user_id]

        percent = int((score / total) * 100)

        await message.answer(
            "🎉 <b>Test tugadi!</b>\n\n"
            f"📊 Natija: <b>{score}/{total}</b>\n"
            f"📈 Foiz: <b>{percent}%</b>\n\n"
            "Natijangiz 📊 Natijalarim bo‘limiga saqlandi.",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

        return

    question = QUIZ[question_number]

    buttons = []

    for answer in question["answers"]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"answer:{question_number}:{answer}",
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await message.answer(
        f"📝 <b>{question_number + 1}-savol / {len(QUIZ)}</b>\n\n"
        f"❓ {question['question']}",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# =========================
# TEST JAVOBINI TEKSHIRISH
# =========================

@dp.callback_query(F.data.startswith("answer:"))
async def answer_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_quiz:
        await callback.answer(
            "Avval testni boshlang.",
            show_alert=True,
        )
        return

    parts = callback.data.split(":", 2)

    question_number = int(parts[1])
    answer = parts[2]

    current_question = QUIZ[question_number]

    if answer == current_question["correct"]:
        user_quiz[user_id]["score"] += 1

        await callback.answer("✅ To‘g‘ri javob!")
        await callback.message.answer("✅ To‘g‘ri!")

    else:
        await callback.answer("❌ Noto‘g‘ri javob!")

        await callback.message.answer(
            f"❌ Noto‘g‘ri.\n"
            f"To‘g‘ri javob: {current_question['correct']}"
        )

    user_quiz[user_id]["question"] += 1

    await send_question(
        callback.message,
        user_id,
    )


# =========================
# 🧮 MATEMATIK YORDAM
# =========================

@dp.message(F.text == "🧮 Matematik yordam")
async def math_handler(message: Message):
    await message.answer(
        "🧮 <b>Matematik yordam</b>\n\n"
        "Menga matematik misol yuboring.\n\n"
        "Masalan:\n"
        "25 + 34\n"
        "100 - 25\n"
        "15 * 8\n"
        "100 / 4\n"
        "(10 + 5) * 2",
        parse_mode="HTML",
    )


# =========================
# XAVFSIZ MATEMATIK HISOBLASH
# =========================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate_expression(expression: str):
    tree = ast.parse(
        expression,
        mode="eval",
    )

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Noto‘g‘ri son")

        if isinstance(node, ast.UnaryOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Noto‘g‘ri amal")

            return operation(calculate(node.operand))

        if isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Noto‘g‘ri amal")

            left = calculate(node.left)
            right = calculate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Daraja juda katta")

            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                if right == 0:
                    raise ZeroDivisionError

            return operation(left, right)

        raise ValueError("Noto‘g‘ri ifoda")

    return calculate(tree)


@dp.message(F.text.regexp(r"^[0-9+\-*/().%\s]+$"))
async def calculate_handler(message: Message):
    expression = message.text.strip()

    try:
        if len(expression) > 100:
            raise ValueError("Juda uzun misol")

        result = calculate_expression(expression)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        await message.answer(
            f"🧮 Misol: <code>{expression}</code>\n\n"
            f"✅ Javob: <b>{result}</b>",
            parse_mode="HTML",
        )

    except ZeroDivisionError:
        await message.answer(
            "❌ Nolga bo‘lish mumkin emas."
        )

    except Exception:
        await message.answer(
            "❌ Misolni hisoblab bo‘lmadi.\n\n"
            "Masalan:\n"
            "25 + 34\n"
            "100 - 25\n"
            "15 * 8\n"
            "100 / 4"
        )


# =========================
# 📊 NATIJALAR
# =========================

@dp.message(F.text == "📊 Natijalarim")
async def results_handler(message: Message):
    user_id = message.from_user.id

    results = get_results(user_id)

    if not results:
        await message.answer(
            "📊 Sizda hali test natijalari mavjud emas.\n\n"
            "📝 Test ishlash tugmasini bosib test ishlang."
        )
        return

    text = "📊 <b>Sizning natijalaringiz</b>\n\n"

    for number, result in enumerate(results, start=1):
        subject, score, total = result

        text += (
            f"{number}. 📚 {subject}\n"
            f"   Natija: {score}/{total}\n\n"
        )

    await message.answer(
        text,
        parse_mode="HTML",
    )


# =========================
# 🔔 ESLATMALAR
# =========================

@dp.message(F.text == "🔔 Eslatmalar")
async def reminder_handler(message: Message):
    await message.answer(
        "🔔 <b>Eslatma</b>\n\n"
        "Hozircha oddiy vaqtli eslatma funksiyasi mavjud.\n\n"
        "Masalan, menga:\n"
        "<code>10 daqiqa</code>\n\n"
        "deb yuboring.",
        parse_mode="HTML",
    )


@dp.message(F.text.regexp(r"^\d+\s*(daqiqa|minut|soniya|sekund)$"))
async def set_reminder(message: Message):
    text = message.text.lower().strip()

    parts = text.split()

    try:
        number = int(parts[0])
    except ValueError:
        await message.answer("❌ Vaqtni to‘g‘ri yozing.")
        return

    if number <= 0:
        await message.answer("❌ Vaqt 0 dan katta bo‘lishi kerak.")
        return

    unit = parts[1]

    if unit in ["daqiqa", "minut"]:
        seconds = number * 60
    else:
        seconds = number

    if seconds > 86400:
        await message.answer(
            "❌ Eslatma 24 soatdan oshmasligi kerak."
        )
        return

    await message.answer(
        f"🔔 Eslatma o‘rnatildi.\n\n"
        f"⏰ {number} {unit}dan keyin sizga xabar beraman."
    )

    await asyncio.sleep(seconds)

    try:
        await message.answer(
            "🔔 <b>Eslatma vaqti bo‘ldi!</b>\n\n"
            "📚 O‘qishni unutmang! 💪",
            parse_mode="HTML",
        )
    except Exception:
        logging.exception("Eslatma yuborishda xatolik")


# =========================
# ℹ️ BOT HAQIDA
# =========================

@dp.message(F.text == "ℹ️ Bot haqida")
async def about_handler(message: Message):
    await message.answer(
        "ℹ️ <b>O‘quvchi yordamchisi</b>\n\n"
        "Bu bot o‘quvchilarga yordam berish uchun yaratilgan.\n\n"
        "📚 Darslar\n"
        "📝 Testlar\n"
        "🧮 Matematik yordam\n"
        "📊 Natijalarni saqlash\n"
        "🔔 Eslatmalar\n\n"
        "🚀 Bot doimiy ravishda rivojlantiriladi.",
        parse_mode="HTML",
    )


# =========================
# NOMA’LUM XABAR
# =========================

@dp.message()
async def other_message_handler(message: Message):
    await message.answer(
        "🤔 Bu buyruqni tushunmadim.\n\n"
        "Quyidagi menyudan foydalaning:",
        reply_markup=main_menu(),
    )


# =========================
# BOTNI ISHGA TUSHIRISH
# =========================

async def main():
    init_db()

    print("✅ O‘quvchi yordamchisi boti ishga tushdi!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())