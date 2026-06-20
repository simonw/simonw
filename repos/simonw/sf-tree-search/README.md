# San Francisco Tree Search

A simple [Datasette](https://github.com/simonw/datasette) demo application.

Try it out here: https://sf-trees.com/

The data comes from [the San Francisco Department of Public Works](https://data.sfgov.org/City-Infrastructure/Street-Tree-List/tkzw-k3nq).

<img src="screenshot.png?raw=true" alt="Screenshot" width="602">

## How I built this

I used [csvs-to-sqlite](https://github.com/simonw/csvs-to-sqlite) to convert their CSV file into a SQLite database like this:

    csvs-to-sqlite Street_Tree_List.csv sf-trees.db \
        -c qLegalStatus -c qSpecies -c qSiteInfo \
        -c PlantType -c qCaretaker -c qCareAssistant \
        -f qLegalStatus -f qSpecies -f qAddress \
        -f qSiteInfo -f PlantType -f qCaretaker \
        -f qCareAssistant -f PermitNotes

I then deployed the resulting SQLite database using `datasette publish now`:

https://san-francisco.datasettes.com/sf-trees/Street_Tree_List

I composed a SQL query for searching the list of trees, using SQLite's full-text search feature:

    select
        Latitude,
        Longitude,
        qSpecies.value as qSpecies,
        qAddress
    from
        Street_Tree_List
        join qSpecies
            on Street_Tree_List.qSpecies = qSpecies.id
    where
        Street_Tree_List.rowid in (
            select
                rowid
            from
                [Street_Tree_List_fts]
            where [Street_Tree_List_fts] match :search
        )

You can [try this query out using Datasette](https://san-francisco.datasettes.com/sf-trees-ebc2ad9?sql=select+Latitude%2C%0D%0A++++Longitude%2C%0D%0A++++qSpecies.value+as+qSpecies%2C%0D%0A++++qAddress%0D%0Afrom%0D%0A++++Street_Tree_List%0D%0A++++join+qSpecies%0D%0A++++++++on+Street_Tree_List.qSpecies+%3D+qSpecies.id%0D%0Awhere%0D%0A++++Street_Tree_List.rowid+in+%28%0D%0A++++++++select%0D%0A++++++++++++rowid%0D%0A++++++++from%0D%0A++++++++++++%5BStreet_Tree_List_fts%5D%0D%0A++++++++where+%5BStreet_Tree_List_fts%5D+match+%3Asearch%0D%0A++++%29%0D%0A&search=olive).

Finally, I used [Leaflet](http://leafletjs.com/) and [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) to construct a simple search interface.
