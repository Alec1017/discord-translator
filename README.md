## Getting Started

### 1. Install Dependencies
```bash
# globally install virtualenv (if not already installed)
python3 -m pip install virtualenv

# clone the repo
git clone git@github.com:Alec1017/discord-translator.git

# move into the project directory
cd discord-translator

# create a virtual environment
python3 -m virtualenv venv

# activate virtual environment
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

### 2. Create Environment Variables
Create a `.env` file at the root of the discord-translator directory
```bash
# create .env file
touch .env
```

Add envrionment variables to the `.env` file:
```bash
# add your discord session token
echo "TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXX" >> .env

# add the channel ID of the channel you want translations from
echo "CHANNEL_ID=0123456789" >> .env

# add the language to translate from
# in this example, we translate from chinese (zh-CN)
echo "LANGUAGE_FROM=zh-CN" >> .env

# add the language to translate to
# in this example, we translate to english (en)
echo "LANGUAGE_TO=en" >> .env

# language codes can be found here: https://www.andiamo.co.uk/resources/iso-language-codes/
```

The resulting `.env` file should look something like this:
```
TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXX
CHANNEL_ID=0123456789
LANGUAGE_FROM=zh-CN
LANGUAGE_TO=en
```

## Usage

Double-check that the virtual environment is activated before usage:
```bash
source venv/bin/activate
```

You can run the translator with the following command:
```bash
python run.py
```