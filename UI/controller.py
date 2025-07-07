import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.coloreSelezionato = None
        self.annoSelezionato = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        for a in range(2015,2019):
            self._view._ddyear.options.append(ft.dropdown.Option(str(a)))
        colors = self._model.get_colors()
        for c in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))
        self._view.update_page()


    def handle_graph(self, e):
        self.annoSelezionato = self._view._ddyear.value
        self.coloreSelezionato = self._view._ddcolor.value
        if self.annoSelezionato is None:
            self._view.txtOut.controls.append(ft.Text("Selezionare un anno"))
            self._view.update_page()
            return
        if self.coloreSelezionato is None:
            self._view.txtOut.controls.append(ft.Text("Selezionare un colore"))
            self._view.update_page()
            return
        self._model.buildGraph(self.annoSelezionato, self.coloreSelezionato)
        self.fillDDProduct()
        nodi, archi = self._model.getGraphDetails()
        self._view.txtOut.controls.append(ft.Text(f"Grafo creato con {nodi} nodi e {archi} archi"))
        archi = self._model.getArchiMaggiori()
        for i in range(0,3):
            try:
                self._view.txtOut.controls.append(ft.Text(f"{archi[i][0]}, {archi[i][1]}, {archi[i][2]} "))
            except:
                pass
        self._view.update_page()


    def fillDDProduct(self):
        prodotti = self._model.getAllNodes()
        for p in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(key=p, data=p, on_click=self.handleProductSelection))
        self._view.update_page()

    def handleProductSelection(self, e):
        self.prodottoSelezionato = e.control.data

    def handle_search(self, e):
        if self.prodottoSelezionato is None:
            self._view.txtOut2.controls.append(ft.Text("Selezionare un nodo di partenza"))
            self._view.update_page()
            return
        numArchiMaxCamm = self._model.getMaxCamminoArchi(self.prodottoSelezionato)
        self._view.txtOut2.controls.append(ft.Text(f"numero archi percorso più lungo: {numArchiMaxCamm}"))
        self._view.update_page()
