from datetime import datetime
class Notas:
    def __init__(self, database) -> None:
        self.__nota = database['notas']
    @property
    def nota(self) -> list:
        return_notas = sorted(list(self.__nota.find()), key=lambda d: datetime.strptime(d["data"], "%d/%m/%Y"))
        return [{key: nota[key] for key in nota if key != "_id" } for nota in return_notas]

    
    def addNotas(self, new_notas: list) -> None:
        for new_nota in new_notas:
            if new_nota not in self.nota:
                self.__nota.insert_one(new_nota)
            else:
                raise ValueError(f"A nota nº {new_nota['nota']} da Corretora {new_nota['corretora']} já foi processada!")
