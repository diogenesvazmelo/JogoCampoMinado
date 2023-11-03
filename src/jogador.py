class Jogador():
    def __init__(self, nick: str):
        self._nick = nick
    
    @property
    def nick(self) -> str:
        return self._nick