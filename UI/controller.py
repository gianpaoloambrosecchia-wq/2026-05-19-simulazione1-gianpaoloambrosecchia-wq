import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceArtist = None

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        for g in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    key = g[0],
                    text = g[1]
                )
            )
        self._view.update_page()

    def _fillDDArtist(self):
        artists = self._model._graph.nodes
        for a in artists:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(
                    data = a,
                    key = a.ArtistId,
                    text = a.Name,
                    on_click=self._readDDArtist
                )
            )
        self._view.update_page()

    def handleCreaGrafo(self, e):
        genreId = self._view._ddGenre.value
        if genreId is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un genere musicale dal menu a tendina", color="red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(genreId)
        self._fillDDArtist()
        numNodes, numEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {numNodes} nodi e {numEdges} archi")
        )
        self._view.update_page()

        topArtista, influenza = self._model.getInfluenza()

        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente {topArtista} con influenza {influenza}")
        )
        topArchi = self._model.getTopArchi()
        for a in topArchi:
            self._view.txt_result.controls.append(
                ft.Text(f"Arco: {a[0]} -> {a[1]} - Peso: {a[2]['weight']}")
            )
        self._view.update_page()



    def handleCammino(self,e):
        if self._choiceArtist is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un artista dal menu", color="red")
            )
            self._view.update_page()
            return

        self._model.getPath(self._choiceArtist)
        path = self._model._bestSol
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il percorso più lungo dal nodo {self._choiceArtist} ha lunghezza {len(path)} e costo {self._model._bestCosto}")
        )
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()





    def _readDDArtist(self, e):
        if e.control.data is None:
            self._choiceArtist = None

        self._choiceArtist = e.control.data

        print(f"Selezionato l'artista {self._choiceArtist}")