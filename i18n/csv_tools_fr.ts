<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0" language="af" sourcelanguage="en">
<context>
    <name>@default</name>
    <message>
        <location filename="../test/test_translations.py" line="46"/>
        <source>Good morning</source>
        <translation>Bonjour</translation>
    </message>
</context>
<context>
    <name>CSVToolsProvider</name>
    <message>
        <location filename="../csv_tools_provider.py" line="82"/>
        <source>CSV Tools</source>
        <translation>Outils CSV</translation>
    </message>
</context>
<context>
    <name>ExportPostgreSQLQueryToCsv</name>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="110"/>
        <source>Database (connection name)</source>
        <translation>Base de données (nom de la connexion)</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="129"/>
        <source>Export PostgreSQL query to CSV (COPY)</source>
        <translation>Export d&apos;une requête PostgreSQL en CSV (COPY)</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="133"/>
        <source>Export to CSV</source>
        <translation>Export vers CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="137"/>
        <source>This algorithm creates a CSV file from an SQL SELECT query. The query is ran against a PostgreSQL/Postgis database, then the result table is exported as CSV using the PostgreSQL COPY command.</source>
        <translation>Cet algorithme crée un fichier CSV à partir d&apos;une requête SQL de type SELECT. La requête est exécutée dans une base de données PostgreSQL (éventuellement avec l&apos;extension Postgis), et la table de résultats est ensuite exportée en CSV grâce à la commande COPY de PostgreSQL.</translation>
    </message>
</context>
<context>
    <name>ExportSQLiteQueryToCsv</name>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="166"/>
        <source>GeoPackage or Spatialite database</source>
        <translation>Base de données GeoPackage ou Spatialite</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="178"/>
        <source>Export SQLite query to CSV</source>
        <translation>Export d&apos;une requête SQLite en CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="182"/>
        <source>Export to CSV</source>
        <translation>Export vers CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="186"/>
        <source>This algorithm creates a CSV file from an SQL SELECT query. The query is ran against an SQLite database (Geopackage or Spatialite), then the result table is exported as CSV.</source>
        <translation>Cet algorithme crée un fichier CSV à partir d&apos; requête SQL de type SELECT. La requête est exécutée dans une base de données SQLite (Geopackage ou Spatialite), et la table de résultats est ensuite exportée en CSV.</translation>
    </message>
</context>
<context>
    <name>FeatureDiffAlgorithm</name>
    <message>
        <location filename="../other_csv_algorithms.py" line="72"/>
        <source>Original layer</source>
        <translation>Couche originale</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="77"/>
        <source>New layer</source>
        <translation>Nouvelle couche</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="89"/>
        <source>HTML report</source>
        <translation>Rapport HTML</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="89"/>
        <source>HTML files (*.html)</source>
        <translation>Fichiers HTML (*.html)</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="82"/>
        <source>Fields to compare</source>
        <translation>Champs à comparer</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="144"/>
        <source>Unable to compare layers with different fields or field order</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="133"/>
        <source>Can only compare SQLite (GeoPackage, Spatialite) or PostgreSQL layers.</source>
        <translation>Ne peut comparer que des couches SQLite (GeoPackage, Spatialite) ou PostgreSQL.</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="166"/>
        <source>No database connection have been created for PostgreSQL layer {0}.</source>
        <translation>Aucune connexion n&apos;a été créée pour la couche PostgreSQL {0}.</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="204"/>
        <source>This algorithm takes two vector layers (SQLite or PostgreSQL) with common fields (those common fields being in the same order) and shows differences between features attributes in an HTML report.

This can be useful to compare two versions of the same layer.

Under the hood, each attribute table is converted to CSV and the two CSV files are diffed.</source>
        <translation>Cet algorithme prend deux couches vectorielles (SQLite ou PostgreSQL) avec des champs en commun (ces champs en commun étant dans le même ordre) et montre les différences entre les valeurs des attributs des entités dans un rapport HTML.

Cela est utile pour comparer deux versions d&apos;une même couche.

Il fonctionne en convertissant chaque table attributaire dans un fichier CSV puis en comparant les lignes de chaque fichier CSV.</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="102"/>
        <source>Attribute difference</source>
        <translation>Différences attributaires</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="106"/>
        <source>Other CSV tools</source>
        <translation>Autres outils CSV</translation>
    </message>
</context>
<context>
    <name>LoadCSVAlgorithm</name>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="74"/>
        <source>Input CSV file</source>
        <translation>Fichier CSV en entrée</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="80"/>
        <source>Column delimiter</source>
        <translation>Séparateur de colonnes</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="86"/>
        <source>Character used to quote columns</source>
        <translation>Caractrère de délimitation des colonnes</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="91"/>
        <source>Is the first line headers ?</source>
        <translation>En-têtes en première ligne ?</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="97"/>
        <source>Decimal point</source>
        <translation>Séparateur décimal</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="104"/>
        <source>WKT column</source>
        <translation>Colonne WKT</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="105"/>
        <source>X/Y (or longitude/latitude) columns</source>
        <translation>Colonnes X, Y (ou latitude, longitude)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="106"/>
        <source>No Geometry</source>
        <translation>Pas de géométrie</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="108"/>
        <source>How geometry is given ?</source>
        <translation>Comment la géométrie est-elle renseignée ?</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="114"/>
        <source>Geometry column, as WKT (if WKT column selected)</source>
        <translation>Colonne géométrie, en WKT (si colonne WKT selectionné)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="119"/>
        <source>X/longitude column (if X/Y column selected)</source>
        <translation>Colonne X ou longitude (si colonnes X, Y selectionné)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="124"/>
        <source>Y/latitude column (if X/Y column selected)</source>
        <translation>Colonne Y ou latitude (si colonnes X, Y selectionné)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="129"/>
        <source>CRS (if geometry given)</source>
        <translation>SCR (si géométrie renseignée)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="134"/>
        <source>CSV layer</source>
        <translation>Couche CSV</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="146"/>
        <source>Create vector layer from CSV file</source>
        <translation>Créer une couche depuis un fichier CSV</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="154"/>
        <source>Import from CSV</source>
        <translation>Import depuis CSV</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="158"/>
        <source>This algorithm loads a CSV file as a vector layer, with or without geometry. If present, geometry may be given as one WKT column or as two X/Y columns.</source>
        <translation>Cet algorithme charge une couche vectorielle depuis un fichier CSV dans lequel les géométries sont données au format WKT dans une colonne.</translation>
    </message>
</context>
<context>
    <name>_AbstractExportQueryToCsv</name>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="70"/>
        <source>SELECT SQL query</source>
        <translation>Requête SQL SELECT</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="75"/>
        <source>CSV file</source>
        <translation>Fichier CSV</translation>
    </message>
</context>
</TS>
