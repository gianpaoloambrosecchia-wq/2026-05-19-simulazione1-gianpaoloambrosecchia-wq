import flet as ft

from model.model import Model
from UI.view import View
from UI.controller import Controller


def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()


ft.app(target=main)


# Area musica — il catalogo
# artist è il punto di partenza. Ha solo ArtistId e Name. Ogni artista può avere più album.
# album contiene AlbumId, Title e la chiave esterna ArtistId che lo collega all'artista. Ogni album appartiene a un solo artista.
# track è la tabella più ricca — ogni brano ha Name, Milliseconds, Bytes, UnitPrice e tre FK: AlbumId (da quale album viene), GenreId e MediaTypeId.
# genre e mediatype sono semplici tabelle di lookup con solo id e nome. Esempi di generi: Rock, Jazz, Classical. Esempi di media type: MPEG audio, AAC audio.

# Area vendite — il ciclo dell'acquisto
# customer contiene i dati anagrafici del cliente (nome, indirizzo, email) più SupportRepId che è una FK verso employee — indica quale dipendente lo assiste.
# invoice è lo "scontrino". Ha CustomerId (chi ha comprato), InvoiceDate, l'indirizzo di fatturazione e il Total.
# invoiceline è il dettaglio della fattura — ogni riga corrisponde a un brano acquistato. Contiene InvoiceId, TrackId, UnitPrice e Quantity. Questa è la tabella chiave per quasi tutti gli esercizi del grafo, perché collega i brani agli acquisti.

# Area dipendenti e playlist
# employee ha i dati di chi lavora nel negozio. La cosa interessante è il campo ReportsTo che è una auto-referenza — è una FK sulla stessa tabella employee, che permette di rappresentare la gerarchia (chi riporta a chi).
# playlist e playlisttrack gestiscono le playlist. playlisttrack è una tabella di associazione many-to-many — una playlist può avere molti brani, e un brano può stare in molte playlist. Non ha chiave primaria propria: la PK è la coppia (PlaylistId, TrackId).

# ReportsTo è una FK che punta alla stessa tabella employee. Significa "questo dipendente riporta a chi ha questo EmployeeId". Quindi Mitchell riporta ad Adams, Park riporta a Mitchell.
# In SQL, quando vuoi fare la gerarchia, fai un self-join:
#    SELECT e_sub.Name AS dipendente, e_sup.Name AS supervisore
#    FROM employee e_sub, employee e_sup
#    WHERE e_sub.ReportsTo = e_sup.EmployeeId
# Dai lo stesso alias diverso alla stessa tabella due volte — una volta come "subordinato", una volta come "supervisore".

#    SELECT e_sup.EmployeeId, e_sub.EmployeeId, COUNT(c.CustomerId) AS peso
#    FROM employee e_sup, employee e_sub, customer c
#    WHERE e_sub.ReportsTo = e_sup.EmployeeId
#          AND c.SupportRepId = e_sub.EmployeeId
#    GROUP BY e_sup.EmployeeId, e_sub.EmployeeId
# Qui usi entrambi i meccanismi insieme: il self-join per trovare la coppia supervisore→subordinato, e il join con customer per contare i clienti del subordinato.
