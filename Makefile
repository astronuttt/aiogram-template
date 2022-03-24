default: help


help:
	@echo "help text"

migration:
	aerich migrate

migrate:
	aerich upgrade

downgrade:
	aerich downgrade

run-reload:
	./bot.py --reload --debug

run:
	./bot.py