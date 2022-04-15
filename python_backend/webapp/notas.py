from datetime import datetime
class Notas:
    def __init__(self) -> None:
        self.__nota = []
    @property
    def nota(self) -> list:
        
        return_notas = sorted(self.__nota, key=lambda d: d["date_datetime"])
        return [{key: nota[key] for key in nota if key != "date_datetime"} for nota in return_notas]
    
    def addNotas(self, new_notas: list) -> None:
        for new_nota in new_notas:
            if new_nota not in self.__nota:
                new_nota["date_datetime"] = datetime.strptime(new_nota["data"], "%d/%m/%Y")
                self.__nota.append(new_nota)
            else:
                raise ValueError(f"A nota nº {new_nota['nota']} da Corretora {new_nota['corretora']} já foi processada!")
