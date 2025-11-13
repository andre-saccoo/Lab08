from database.impianto_DAO import ImpiantoDAO
from database.consumo_DAO import ConsumoDAO

'''
MODELLO:
- Rappresenta la struttura dati
- Si occupa di gestire lo stato dell'applicazione
- Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        somma_consumi = 0
        conta_giorni_mese=0
        lista_consumo_medio = [] #da dare in return avrà il nome dell'impianto e la media del consumo del mese
        for impianto in self._impianti:
            lista_consumi = ConsumoDAO.get_consumi( impianto.id )
            for consumo in lista_consumi:
                if consumo.data.month == mese:
                    somma_consumi += consumo.kwh
                    conta_giorni_mese += 1
            media_consumi = somma_consumi / conta_giorni_mese
            lista_consumo_medio.append( (impianto.nome, media_consumi))
        return lista_consumo_medio

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)
        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        #sequenza parziale è una sequenza vuota | consumi_settimana è un dizionario con scritto codice impianto: lista consumi settimana

        if giorno == 8:
            self.__costo_ottimo = costo_corrente
            self.__sequenza_ottima = list(sequenza_parziale)
            #faccio la scelta per il primo giorno della settimana,
            # prendiamo i primi due consumi e impostiamo il più basso come ultimo consumo appendendolo alla lista

        else:
            id_impianto_1 = self._impianti[0].id
            id_impianto_2 = self._impianti[1].id
            if ultimo_impianto is None and giorno ==1:
                if consumi_settimana[id_impianto_1][giorno - 1] <= consumi_settimana[id_impianto_2][giorno - 1]:
                    ultimo_impianto = id_impianto_1
                    sequenza_parziale.append(ultimo_impianto)
                    costo_corrente +=consumi_settimana[id_impianto_1][giorno - 1]
                    giorno = giorno + 1
                else:
                    ultimo_impianto = id_impianto_2
                    sequenza_parziale.append(ultimo_impianto)
                    costo_corrente += consumi_settimana[id_impianto_2][giorno - 1]
                    giorno = giorno + 1
                self.__ricorsione(sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana)
                sequenza_parziale.pop()

            elif  1< giorno <= 7 and ultimo_impianto is not None:
                # if che determina altro impianto a seconda del precedente
                if ultimo_impianto == id_impianto_1:
                    altro_impianto = id_impianto_2
                else:
                    altro_impianto = id_impianto_1

                if consumi_settimana [ ultimo_impianto ][ giorno-1 ]<consumi_settimana[ altro_impianto ][ giorno-1]+5:
                    sequenza_parziale.append(ultimo_impianto)
                    costo_corrente += consumi_settimana [ ultimo_impianto ][ giorno-1 ]
                else:
                    sequenza_parziale.append(altro_impianto)
                    ultimo_impianto = altro_impianto
                    costo_corrente = costo_corrente + consumi_settimana[ altro_impianto ][ giorno-1]+5
                giorno+=1
                self.__ricorsione(sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana)
                sequenza_parziale.pop()

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        dizionario_consumi={}
        for impianto in self._impianti:
            lista_consumi = impianto.get_consumi()
            lista_consumi_settimana=[]
            for consumo in lista_consumi:
                if consumo.data.month ==mese and consumo.data.day <=7:
                    lista_consumi_settimana.append(consumo.kwh)
            dizionario_consumi[impianto.id]=lista_consumi_settimana
        return dizionario_consumi