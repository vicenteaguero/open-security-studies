# update.sh

clear
ruff check .. --fix

poetry run python scripts/create_htmls.py