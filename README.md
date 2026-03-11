# Polyglossia 🚀

**Polyglossia** is an app designed to accelerate language learning.  

The app leverages AI to make learning more efficient by:

- Integrating with **OpenAI** for
  - generating sentences
  - checking grammar and stylistic correctness
- Quickly creating advanced **ANKI flashcards** for vocabulary and grammar practice.

## Local setup
```bash
cp .env.example .env # + replace with your own values

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

# Optional: create superuser
./scripts/seed_dev_data.sh
```

## Important notes
**Current Focus**: The app is currently optimized for Polish-German translations and learning.
