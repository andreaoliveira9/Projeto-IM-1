import random


# Decorator para randomizar as respostas TTS para cada intenção
def randomize(func):
    def wrapper(*args, **kwargs):
        return random.choice(func(*args, **kwargs))

    return wrapper


@randomize
def random_goodbye():
    return [
        "Até logo! Espero que tenha gostado da música!",
        "Tchau! Volte sempre para ouvir mais!",
        "Adeus! Até a próxima!",
    ]


class IntentNotUnderstoodWell:
    def __init__(self, intent, entities):
        self.intent = intent
        self.entities = entities

    def __str__(self):
        return f"Intent: {self.intent}, Entities: {self.entities}"
