from telegram.ext import Updater, CommandHandler

# Définir la fonction pour la commande /bonjour
def bonjour(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bonjour ! Bienvenue sur ce bot.")

# Mettre en place le bot
def main():
    # Insérez votre token API à la place de 'YOUR_API_TOKEN'
    updater = Updater('YOUR_API_TOKEN', use_context=True)
    dp = updater.dispatcher

    # Ajouter un gestionnaire pour la commande /bonjour
    dp.add_handler(CommandHandler("bonjour", bonjour))

    # Démarrer le bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
