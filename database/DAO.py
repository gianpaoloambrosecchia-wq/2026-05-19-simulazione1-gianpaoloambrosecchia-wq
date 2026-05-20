from database.DB_connect import DBConnect
from model.arco import Arco
from model.artista import Artista


class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from genre
                    """

        cursor.execute(query)

        for row in cursor:
            result.append((row["GenreId"],row["Name"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getArtists(genreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select ar.ArtistId, ar.Name, sum(il.Quantity) as pop
                    from artist ar
                    join album al on al.ArtistId = ar.ArtistId 
                    join track t on t.AlbumId = al.AlbumId
                    join invoiceline il on t.TrackId = il.TrackId 
                    join invoice i on il.InvoiceId = i.InvoiceId 
                    where t.GenreId = %s
                    group by ar.ArtistId, ar.Name """

        cursor.execute(query, (genreId,))

        for row in cursor:
            result.append(Artista(
                row["ArtistId"],
                row["Name"],
                row["pop"]
            ))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getEdges(genreId, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct a1.ArtistId as a1Id, a2.ArtistId as a2Id
                    from artist a1, album al1, track t1, invoiceline il1, invoice i1, artist a2, album al2, track t2, invoiceline il2, invoice i2
                    where a1.ArtistId < a2.ArtistId and a1.ArtistId = al1.ArtistId and a2.ArtistId = al2.ArtistId and t1.AlbumId = al1.AlbumId and
                          t2.AlbumId = al2.AlbumId and il1.TrackId = t1.TrackId and il2.TrackId = t2.TrackId and t1.GenreId = %s and t2.GenreId = %s and
                          il1.InvoiceId = i1.InvoiceId and il2.InvoiceId = i2.InvoiceId and i1.CustomerId = i2.CustomerId """

        cursor.execute(query, (genreId,genreId))

        for row in cursor:
            result.append((idMap[row["a1Id"]], idMap[row["a2Id"]]))

        cursor.close()
        conn.close()
        return result







