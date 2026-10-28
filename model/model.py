from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        strumenti = []
        try:
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("""SELECT *
                           FROM strumento""")

            for riga in cursor:
                strumenti.append(Strumento(
                    codice=riga["codice"],
                    tipo=riga["tipo"],
                    marca=riga["marca"],
                    anno_acquisto=riga["anno_acquisto"],
                    valore=riga["valore"],
                    disponibile=bool(riga["disponibile"])
                ))

            cursor.close()
            cnx.close()
            return strumenti

        except Exception as e:
            print(f"Errore durante l'accesso al database: {e}")
            if cnx:
                cnx.close()
            return None

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        cnx = get_connection()
        if cnx is None:
            return None

        strumenti = []
        try:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
                       FROM strumento
                       WHERE tipo = %s"""
            cursor.execute(query, (tipo,))

            for riga in cursor:
                strumenti.append(Strumento(
                    codice=riga["codice"],
                    tipo=riga["tipo"],
                    marca=riga["marca"],
                    anno_acquisto=riga["anno_acquisto"],
                    valore=riga["valore"],
                    disponibile=bool(riga["disponibile"])
                ))

            cursor.close()
            cnx.close()
            return strumenti

        except Exception as e:
            print(f"Errore durante l'accesso al database: {e}")
            if cnx:
                cnx.close()
            return None
