import os
import requests
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
print(BOT_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)
API_URL = "https://rest.cosmos.directory/cosmoshub/cosmos/gov/v1beta1/proposals?proposal_status=0&pagination.key=AAAAAAAAAx0="
API_URL2="https://rest.cosmos.directory/cosmoshub/cosmos/gov/v1beta1/proposals/"
last_prop=0

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    
@bot.message_handler(commands=['gov'])
def send_proposals(message):
    
    # Effectuer une requête GET vers l'API Cosmos pour obtenir les propositions
    response = requests.get(API_URL)

    # Vérifier si la requête a réussi (statut HTTP 200)
    if response.status_code == 200:
        # Charger les données JSON à partir de la réponse
        data = response.json()

        # Récupérer la liste de propositions depuis le champ "proposals"
        proposals_data = data.get("proposals", [])
        last_three_proposals = proposals_data[-3:]
        # Envoyer les propositions au chat Telegram
        proposals_text = ""
        for proposal in last_three_proposals:
            title = proposal["proposal_id"]
            description = proposal["content"]["title"]
            proposals_text += f"{title} -- {description}\n\n"
        bot.reply_to(message, proposals_text)
        last_prop=int(title)
    else:
        bot.reply_to(message, f"La requête a échoué avec le statut {response.status_code}")

@bot.message_handler(commands=['sondage'])
def create_poll(message):
    # Extraire l'identifiant de la proposition à partir du texte du message
    proposal_id=last_prop
    try:
        proposal_id = int(message.text.split()[1])  # Supposons que le format soit "/sondage <id>"
    except (IndexError, ValueError):
        proposal_id=last_prop
    #    return
        # Utiliser l'identifiant de la proposition pour récupérer les détails depuis l'API
    proposal_url = f"{API_URL2}{proposal_id}"
    response = requests.get(proposal_url)
   
    # Créer un sondage avec la question basée sur la proposition
    if response.status_code == 200:
        proposal_data = response.json()
        # Extraire des détails de la proposition
        title = proposal_data["proposal"]["proposal_id"]
        description = proposal_data["proposal"]["content"]["title"]

        # Créer un sondage avec la question basée sur la proposition
        question = f"Ton vote sur : {title} -- {description}?"
        options = ["Oui", "Non", "Sans opinion", "Abstention"]

        # Envoyer le sondage au chat Telegram
        poll_message = bot.send_poll(
            message.chat.id,
            question,
            options,
            is_anonymous=False,
            allows_multiple_answers=False,
        )

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
bot.infinity_polling()
