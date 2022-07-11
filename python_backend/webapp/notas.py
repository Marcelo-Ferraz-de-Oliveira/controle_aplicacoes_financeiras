from datetime import datetime
class Notas:
    def __init__(self, database) -> None:
        self.__nota = database['notas']
    @property
    def nota(self) -> list:
        return_notas = sorted(list(self.__nota.find()), key=lambda d: datetime.strptime(d["date_datetime"], "%d/%m/%Y"))
        return [{key: nota[key] for key in nota if key not in ("date_datetime", "_id") } for nota in return_notas]

    
    def addNotas(self, new_notas: list) -> None:
        for new_nota in new_notas:
            if new_nota not in self.nota:
                new_nota["date_datetime"] = datetime.strftime(datetime.strptime(new_nota["data"], "%d/%m/%Y"), "%d/%m/%Y")
                self.__nota.insert_one(new_nota)
            else:
                raise ValueError(f"A nota nº {new_nota['nota']} da Corretora {new_nota['corretora']} já foi processada!")
