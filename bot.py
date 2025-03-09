import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,  # Заменили Updater на ApplicationBuilder
    CommandHandler,
    ContextTypes
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

user_tasks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_tasks[user_id] = []
    await update.message.reply_text(
        "📝 Привет! Я бот для задач.\n"
        "Команды:\n"
        "/add <задача> - добавить\n"
        "/list - показать список\n"
        "/delete <номер> - удалить"
    )

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    task = ' '.join(context.args)
    
    if not task:
        await update.message.reply_text("❌ Укажите задачу: /add Купить молоко")
        return
    
    user_tasks[user_id].append(task)
    await update.message.reply_text(f"✅ Добавлено: {task}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    tasks = user_tasks.get(user_id, [])
    
    if not tasks:
        await update.message.reply_text("📭 Список пуст!")
        return
    
    tasks_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
    await update.message.reply_text(f"📋 Ваши задачи:\n{tasks_list}")

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    tasks = user_tasks.get(user_id, [])
    
    try:
        task_num = int(context.args[0]) - 1
        deleted_task = tasks.pop(task_num)
        await update.message.reply_text(f"🗑 Удалено: {deleted_task}")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Укажите номер: /delete 1")
    except KeyError:
        await update.message.reply_text("❌ Список задач пуст!")

def main() -> None:
    # Используем ApplicationBuilder вместо Updater
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CommandHandler("delete", delete_task))
    
    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
