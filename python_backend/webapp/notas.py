class Notas:
    def __init__(self) -> None:
        self.__nota = []
    @property
    def nota(self) -> list:
        return self.__nota
    
    def addNotas(self, new_notas: list) -> None:
        for new_nota in new_notas:
            if new_nota not in self.__nota:
                self.__nota.append(new_nota)
            else:
                raise ValueError(f"A nota nº {new_nota['nota']} da Corretora {new_nota['corretora']} já foi processada!")
