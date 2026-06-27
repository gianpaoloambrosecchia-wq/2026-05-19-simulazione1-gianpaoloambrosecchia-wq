
#1)
# Grafo non orientato e pesato tra dipendenti. I nodi sono i dipendenti che gestiscono almeno 1 cliente.
# Esiste un arco tra il dipendente A e il dipendente B se almeno un cliente ha acquistato brani dello stesso
# artista per entrambi (cioè: un cliente di A e un cliente di B hanno comprato brani dello stesso artista).
# Il peso dell'arco è il numero di artisti in comune tra i clienti dei due dipendenti.

# select t1.employeeid, t2.employeeid, count(distinct t1.artistid) as peso
# from (select e.EmployeeId, a.ArtistId
# from employee e, customer c, invoice i, invoiceline i2, track t, album a
# where e.EmployeeId = c.SupportRepId and c.CustomerId = i.CustomerId and i.InvoiceId = i2.InvoiceId
# 	  and t.TrackId = i2.TrackId and a.AlbumId = t.AlbumId) t1
# join (select e.EmployeeId, a.ArtistId
# from employee e, customer c, invoice i, invoiceline i2, track t, album a
# where e.EmployeeId = c.SupportRepId and c.CustomerId = i.CustomerId and i.InvoiceId = i2.InvoiceId
# 	and t.TrackId = i2.TrackId and a.AlbumId = t.AlbumId) t2 on t1.artistid  = t2.artistid
# where t1.employeeid<t2.employeeid
# group by t1.employeeid, t2.employeeid


