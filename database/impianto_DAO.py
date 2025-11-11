from database.DB_connect import ConnessioneDB
from model.impianto_DTO import Impianto

"""
    IMPIANTO DAO
    Gestisce le operazioni di accesso al database.
"""

class ImpiantoDAO:
    @staticmethod
    def get_impianti() -> list[Impianto] | None:
        """
        Restituisce tutti gli impianti presenti nel database
        :return: lista di tutti gli Impianti
        """
        cnx = ConnessioneDB.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM impianto """
        try:
            cursor.execute(query)
            for row in cursor:
                impianto = Impianto(
                    id=row["id"],
                    nome=row["nome"],
                    indirizzo=row["indirizzo"],
                )
                result.append(impianto)
        except Exception as e:
            print(f"Errore durante la query get_consumi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
