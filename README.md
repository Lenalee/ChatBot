# Authentification:

## Generating token via personal access token:
Start in Developer Console. Then, go to Settings > Authorization > Personal Access Tokens and create a new token together with necessary scopes. You won't be able to change those scopes once you create the token.

to do it follow the tutorial: https://platform.text.com/docs/authorization/
then, to create a token use this: 

ACCOUNT_ID is present in the livechat app.

auth_string = f"{ACCOUNT_ID}:{PERSONAL_ACCESS_TOKEN}"
access_token = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

you can also debug and see the account id here: https://platform.text.com/console/settings/authorization/token-debugger

for this type of autentification we need to use this header:

headers = {
    "Authorization": f"Basic {auth_encoded}",
    "Content-Type": "application/json"
}

## Generating token via implicit grant(oauth):
here is the tutorial i used: https://platform.text.com/docs/authorization/
video tutorial: https://www.youtube.com/watch?v=-EUZ_Ynvz5Q&ab_channel=LiveChat

the script that autentificates is auth.html. In that script i specify cliend id and redirect uri. The same redirect uri should be specified in the livechat app.
In order for it work i only need to open the web page and copy the token from the console.
the symbol '%3A' needs to be replaced with ':' in the token.

for this type of autentification we need to use this header:

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Start a testing chat server:
cd /path/to/your/html

python -m http.server 3000
open http://localhost:3000/chat.html


# Creating a bot:


for ngrok:
http://127.0.0.1:4040 page with all requests

# Starting the chatbot server:
python webhook_tester.py
ngrok http 5000
copy forward url

connect webhooks to the bot

# glosary
X-Author-Id is bot id
In order to see chat as "on" i need to expose it to the internet.


#TODO
bot token refresh strategy!

# requirements
poetry export \
  -f requirements.txt \
  --output requirements.txt \
  --without-hashes \
  --dev
