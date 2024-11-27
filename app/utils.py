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
        "Tchau! Espero que você tenha uma boa música!",
        "Até mais! Estou aqui quando você precisar!",
    ]


@randomize
def random_play_song():
    return [
        "Reproduzindo sua música agora!",
        "Tocando a música solicitada.",
        "Sua música está começando, aproveite!",
        "Iniciando a reprodução da música no YouTube Music.",
        "Reproduzindo a música que você pediu.",
    ]


@randomize
def random_pause():
    return [
        "A música foi pausada.",
        "Música em pausa agora.",
        "A reprodução foi interrompida, aguarde.",
        "A música está pausada. Para retomar, me avise!",
        "Interrompendo a música conforme solicitado.",
    ]


@randomize
def random_resume():
    return [
        "Retomando a música.",
        "A música voltou a tocar.",
        "Reprodução retomada!",
        "Recomeçando a música onde parou.",
        "A música está tocando novamente.",
    ]


@randomize
def random_next_song():
    return [
        "Pulando para a próxima faixa.",
        "Indo para a próxima música!",
        "A próxima música está tocando agora.",
        "Avançando para a próxima faixa na playlist.",
        "Trocando para a próxima música.",
    ]


@randomize
def random_previous_song():
    return [
        "Voltando para a música anterior.",
        "A música anterior está tocando agora.",
        "Reproduzindo a faixa anterior.",
        "Indo para a música que tocou antes.",
        "Tocando a música anterior na playlist.",
    ]


@randomize
def random_increase_volume():
    return [
        "Aumentando o volume.",
        "Volume mais alto agora.",
        "Deixando o som um pouco mais alto!",
        "O volume foi aumentado.",
        "Tornando a música mais audível.",
    ]


@randomize
def random_decrease_volume():
    return [
        "Diminuindo o volume.",
        "Volume mais baixo agora.",
        "Reduzindo o som um pouco.",
        "O volume foi diminuído.",
        "Deixando o som mais suave.",
    ]


@randomize
def random_mute():
    return [
        "Silenciando a música.",
        "O som foi colocado no mudo.",
        "Música em modo silencioso.",
        "A música foi silenciada, para ouvir novamente desative o mudo.",
        "Silenciando o volume da música.",
    ]


@randomize
def random_unmute():
    return [
        "Som ativado novamente.",
        "Retirando do mudo, a música está tocando.",
        "Desativando o modo mudo.",
        "Você pode ouvir a música agora.",
        "Volume ativado novamente.",
    ]


@randomize
def random_play_playlist():
    return [
        "Reproduzindo a playlist solicitada.",
        "Iniciando a playlist que você pediu.",
        "A playlist está tocando agora.",
        "Começando a playlist escolhida.",
        "Iniciando a reprodução da playlist.",
    ]


@randomize
def random_add_to_favorites():
    return [
        "Adicionando esta música aos seus favoritos.",
        "A música foi marcada como favorita.",
        "Esta faixa agora está nos seus favoritos.",
        "Música adicionada aos favoritos!",
        "Salvando essa música nos seus favoritos.",
    ]


@randomize
def random_repeat_song():
    return [
        "Colocando a música no modo de repetição.",
        "A música será repetida.",
        "Repetindo a música atual.",
        "A faixa está em modo de repetição agora.",
        "A música vai tocar de novo.",
    ]


@randomize
def random_shuffle_on():
    return [
        "Modo aleatório ativado.",
        "Playlist em modo embaralhado.",
        "Ativando o modo de reprodução aleatória.",
        "A reprodução será feita em ordem aleatória.",
        "Embaralhando as músicas agora.",
    ]


@randomize
def random_shuffle_off():
    return [
        "Modo aleatório desativado.",
        "Voltando à ordem normal de reprodução.",
        "Desativando a reprodução aleatória.",
        "As músicas vão tocar na sequência original.",
        "Reproduzindo na ordem da playlist.",
    ]


@randomize
def random_not_understand():
    return [
        "Desculpe, não entendi o que você pediu.",
        "Não compreendi o comando, pode repetir?",
        "Pode dizer novamente? Não entendi.",
        "Desculpe, não reconheci o pedido.",
        "Comando não entendido, pode tentar de novo?",
    ]


class IntentNotUnderstoodWell:
    def __init__(self, intent, entities):
        self.intent = intent
        self.entities = entities

    def __str__(self):
        return f"Intent: {self.intent}, Entities: {self.entities}"
