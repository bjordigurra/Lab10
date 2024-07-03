import copy
import operator

import flet as ft

from model.country import Country


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno = 0
        self._stato = None

    def handleCalcola(self, e):
        self._view._txt_result.controls.clear()
        if self._view._txtAnno.value == "" or self._view._txtAnno.value.isdigit() is False:
            self._view.create_alert("Inserire un numero valido!")
            return

        if int(self._view._txtAnno.value) < 1816 or int(self._view._txtAnno.value) > 2016:
            self._view.create_alert("Inserire un anno compreso tra 1816 e 2016!")
            return

        self._model.creaGrafo(self._view._txtAnno.value)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.numNodes()} nodi"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.numEdges()} archi"))

        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.componenteConnessa()} componenti connesse."))

        self._view._txt_result.controls.append(ft.Text("Di seguito il dettaglio sui nodi:"))
        lista = list(self._model.grafo.nodes)

        #nuova_lista = [stato for stato in self._model.countries if stato not in lista]
        # lista con stati non confinanti con nessuno (isole) che non sono nodi del grafo

        #lista.extend(nuova_lista) # aggiungo gli stati non nodi alla lista finale
        lista.sort(key=operator.attrgetter("StateNme"))

        for nodo in lista:
            self._view._txt_result.controls.append(ft.Text(f"{nodo.StateNme} -- {self._model.getGrado(nodo)} vicini"))

        self.populate_ddStati()

        self._view.update_page()


    def handleStatiRaggiungibili(self, e):
        self._view._txt_result.controls.clear()
        if self._view._ddStati.value is None:
            self._view.create_alert("Selezionare uno Stato!")
            return

        #print(self._view._ddStati.value)
        #print(self._model._idMap)
        #print(self._model._idMap[f"{self._view._ddStati.value}"])
        #print(type(self._view._ddStati.value))
        successori = set(self._model.getConnessioni(self._model._idMap[int(self._view._ddStati.value)]))
        if len(successori) == 0:
            self._view._txt_result.controls.append(ft.Text("Nessuno Stato raggiungibile via terra."))
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text("Stati raggiungibili:"))
        lista = list(successori)
        lista.sort(key=operator.attrgetter("StateNme"))
        for elemento in lista:
            self._view._txt_result.controls.append(ft.Text(elemento))

        self._view.update_page()



    def leggi_anno(self):
        if self._view._txtAnno.value is None:
            self._anno = None
        else:
            self._anno = self._view._txtAnno.value

    def leggi_stato(self, e):
        if self._view._ddStati.value is None:
            self._stato = None
        else:
            self._stato = e.control.data

    def populate_ddStati(self):
        stati = list(self._model.grafo.nodes)
        stati.sort(key=operator.attrgetter("StateNme"))
        for stato in stati:
            self._view._ddStati.options.append(ft.dropdown.Option(text=stato.StateNme,
                                                                  data=stato,
                                                                  key=stato.CCode,
                                                                  on_click=self.leggi_stato))
