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
    <name>AttributeDiffBetweenLayersAlgorithm</name>
    <message>
        <location filename="../other_csv_algorithms.py" line="246"/>
        <source>Original layer</source>
        <translation>Couche originale</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="225"/>
        <source>Attribute difference between layers</source>
        <translation>Différences attributaires entre couches</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="229"/>
        <source>Other CSV tools</source>
        <translation>Autres outils CSV</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="291"/>
        <source>Unable to compare layers with different fields or field order</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="232"/>
        <source>This algorithm takes two vector layers  with common fields (those common fields being in the same order or the result will be unreadable) and shows differences between attributes in an HTML report.

This can be useful to compare two versions of the same layer.

Under the hood, each attribute table is converted to CSV and the two CSV files are diffed.

For the output to be correct, all lines in each CSV file must be written in the same order. Thus, a sort expression must be given. For example, it can be a key field that identifies features in each layer.</source>
        <translation>Cet algorithme prend deux couches vectorielles avec des champs en commun (ces champs en commun étant dans le même ordre sinon le résultat sera illisible) et montre les différences entre les attributs dans un rapport HTML.

Cela est utile pour comparer deux versions d&apos;une même couche.

Il fonctionne en convertissant chaque table attributaire en un fichier CSV puis en comparant les lignes de chaque fichier CSV.

Pour que le résultat soit correct, les lignes de chaque fichier CSV doivent être générées dans le même ordre. C&apos;est pourquoi une expression de tri doit être indiquée. Elle peut être par exemple un champ clé qui permet d&apos;identifier les entités dans chaque couche.</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="251"/>
        <source>New layer</source>
        <translation>Nouvelle couche</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="256"/>
        <source>Fields to compare</source>
        <translation>Champs à comparer</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="263"/>
        <source>Highlight method</source>
        <translation>Méthode d&apos;affichage des différences</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="263"/>
        <source>Only highlight different lines</source>
        <translation>Ne montrer que les lignes différentes</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="263"/>
        <source>Highligt different lines and inta-line character changes (Slower on large layers)</source>
        <translation>Montrer les lignes différentes et les modifications de caractères intra-lignes (plus lent avec des grosses couches)</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="273"/>
        <source>Sort expression</source>
        <translation>Expression de tri</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="279"/>
        <source>HTML report</source>
        <translation>Rapport HTML</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="279"/>
        <source>HTML files (*.html)</source>
        <translation>Fichiers HTML (*.html)</translation>
    </message>
</context>
<context>
    <name>AttributeDiffWithPgAlgorithm</name>
    <message>
        <location filename="../other_csv_algorithms.py" line="328"/>
        <source>Attribute difference with a PostgreSQL/Postgis table</source>
        <translation>Différences attributaires avec une table PostgreSQL/Postgis</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="332"/>
        <source>Other CSV tools</source>
        <translation>Autres outils CSV</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="368"/>
        <source>PostgreSQL database (connection name)</source>
        <translation>Base de données PostgreSQL (nom de connection)</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="377"/>
        <source>PostgreSQL schema name</source>
        <translation>Nom du schéma PostgreSQL</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="390"/>
        <source>PostgreSQL original table name</source>
        <translation>Nom de la table originale PostgreSQL</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="464"/>
        <source>Table in PostgreSQL database</source>
        <translation>Table dans la base de données PostgreSQL</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="335"/>
        <source>This algorithm takes a vector layer and a PostgreSQL/Postgis table with common columns and shows differences between rows in an HTML report.

This can be useful to compare the layer with its original version in database before submitting new or updated data to database.

Under the hood, the table and attribute table are converted to CSV and the two CSV files are diffed.

For the output to be correct, all lines in each CSV file must be written in the same order. Thus, a sort expression must be given. For example, it can be a key field that identifies features in each layer.</source>
        <translation>Cet algorithme prend une couche vectorielle et une table PostgreSQL ou Postgis avec des colonnes en commun et montre les différences entre les lignes dans un rapport HTML.

Cela est utile pour comparer une couche avec son original en base avant de soumettres les données mises à jour à la base de données.

Il fonctionne en convertissant la table et la table attributaire en un fichier CSV puis en comparant les lignes de chaque fichier CSV.

Pour que le résultat soit correct, les lignes de chaque fichier CSV doivent être générées dans le même ordre. C&apos;est pourquoi une expression de tri doit être indiquée. Elle peut être par exemple un champ clé qui permet d&apos;identifier les entités dans chaque couche.</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="406"/>
        <source>New layer</source>
        <translation>Nouvelle couche</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="411"/>
        <source>Fields to compare</source>
        <translation>Champs à comparer</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="418"/>
        <source>Highlight method</source>
        <translation>Méthode d&apos;affichage des différences</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="418"/>
        <source>Only highlight different lines</source>
        <translation>Ne montrer que les lignes différentes</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="418"/>
        <source>Highligt different lines and inta-line character changes (Slower on large layers)</source>
        <translation>Montrer les lignes différentes et les modifications de caractères intra-lignes (plus lent avec des grosses couches)</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="428"/>
        <source>Sort expression (put in ORDER BY clause)</source>
        <translation>Expression de tri (utilisée dans la clause ORDER BY)</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="434"/>
        <source>HTML report</source>
        <translation>Rapport HTML</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="434"/>
        <source>HTML files (*.html)</source>
        <translation>Fichiers HTML (*.html)</translation>
    </message>
</context>
<context>
    <name>CSVToolsProvider</name>
    <message>
        <location filename="../csv_tools_provider.py" line="88"/>
        <source>CSV Tools</source>
        <translation>Outils CSV</translation>
    </message>
</context>
<context>
    <name>ExportLayerToCsv</name>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="327"/>
        <source>Export layer to CSV</source>
        <translation>Exporter une couche en CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="335"/>
        <source>Export to CSV</source>
        <translation>Export vers CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="343"/>
        <source>This algorithm creates a CSV file from a vector layer. Geometries are converted to WKT strings.</source>
        <translation>Cet algorithme crée un fichier CSV à partir d&apos;une couche vectorielle. Les géométries sont converties en chaînes de caractères WKT.</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="350"/>
        <source>Input vector layer</source>
        <translation>Couche vectorielle en entrée</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="380"/>
        <source>CSV file</source>
        <translation>Fichier CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="360"/>
        <source>Separator</source>
        <translation>Séparateur</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="373"/>
        <source>End-line character</source>
        <translation>Caractère de fin de ligne</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="367"/>
        <source>Quoting</source>
        <translation>Délimitation des valeurs</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="355"/>
        <source>Export geometry as WKT string?</source>
        <translation>Exporter les géométries en chaînes de caractères WKT ?</translation>
    </message>
</context>
<context>
    <name>ExportPostgreSQLQueryToCsv</name>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="144"/>
        <source>Database (connection name)</source>
        <translation>Base de données (nom de la connexion)</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="192"/>
        <source>Export PostgreSQL query to CSV (COPY)</source>
        <translation>Export d&apos;une requête PostgreSQL en CSV (COPY)</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="196"/>
        <source>Export to CSV</source>
        <translation>Export vers CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="200"/>
        <source>This algorithm creates a CSV file from an SQL SELECT query. The query is ran against a PostgreSQL/Postgis database, then the result table is exported as CSV using the PostgreSQL COPY command.</source>
        <translation>Cet algorithme crée un fichier CSV à partir d&apos;une requête SQL de type SELECT. La requête est exécutée dans une base de données PostgreSQL (éventuellement avec l&apos;extension Postgis), et la table de résultats est ensuite exportée en CSV grâce à la commande COPY de PostgreSQL.</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="155"/>
        <source>SELECT SQL query</source>
        <translation>Requête SQL SELECT</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="160"/>
        <source>Separator</source>
        <translation>Séparateur</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="167"/>
        <source>Quoting</source>
        <translation>Délimitation des valeurs</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="173"/>
        <source>End-line character</source>
        <translation>Caractère de fin de ligne</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="180"/>
        <source>CSV file</source>
        <translation>Fichier CSV</translation>
    </message>
</context>
<context>
    <name>ExportSQLiteQueryToCsv</name>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="240"/>
        <source>GeoPackage or Spatialite database</source>
        <translation>Base de données GeoPackage ou Spatialite</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="281"/>
        <source>Export SQLite query to CSV</source>
        <translation>Export d&apos;une requête SQLite en CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="285"/>
        <source>Export to CSV</source>
        <translation>Export vers CSV</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="289"/>
        <source>This algorithm creates a CSV file from an SQL SELECT query. The query is ran against an SQLite database (Geopackage or Spatialite), then the result table is exported as CSV.</source>
        <translation>Cet algorithme crée un fichier CSV à partir d&apos; requête SQL de type SELECT. La requête est exécutée dans une base de données SQLite (Geopackage ou Spatialite), et la table de résultats est ensuite exportée en CSV.</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="244"/>
        <source>SELECT SQL query</source>
        <translation>Requête SQL SELECT</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="249"/>
        <source>Separator</source>
        <translation>Séparateur</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="256"/>
        <source>Quoting</source>
        <translation>Délimitation des valeurs</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="262"/>
        <source>End-line character</source>
        <translation>Caractère de fin de ligne</translation>
    </message>
    <message>
        <location filename="../export_to_csv_algorithms.py" line="269"/>
        <source>CSV file</source>
        <translation>Fichier CSV</translation>
    </message>
</context>
<context>
    <name>LoadCSVAlgorithm</name>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="139"/>
        <source>Input CSV file</source>
        <translation>Fichier CSV en entrée</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="145"/>
        <source>Column delimiter</source>
        <translation>Séparateur de colonnes</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="151"/>
        <source>Character used to quote columns</source>
        <translation>Caractrère de délimitation des colonnes</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="156"/>
        <source>Is the first line headers ?</source>
        <translation>En-têtes en première ligne ?</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="162"/>
        <source>Decimal point</source>
        <translation>Séparateur décimal</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="169"/>
        <source>WKT column</source>
        <translation>Colonne WKT</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="170"/>
        <source>X/Y (or longitude/latitude) columns</source>
        <translation>Colonnes X, Y (ou latitude, longitude)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="171"/>
        <source>No Geometry</source>
        <translation>Pas de géométrie</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="173"/>
        <source>How geometry is given ?</source>
        <translation>Comment la géométrie est-elle renseignée ?</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="179"/>
        <source>Geometry column, as WKT (if WKT column selected)</source>
        <translation>Colonne géométrie, en WKT (si colonne WKT selectionné)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="184"/>
        <source>X/longitude column (if X/Y column selected)</source>
        <translation>Colonne X ou longitude (si colonnes X, Y selectionné)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="189"/>
        <source>Y/latitude column (if X/Y column selected)</source>
        <translation>Colonne Y ou latitude (si colonnes X, Y selectionné)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="194"/>
        <source>CRS (if geometry given)</source>
        <translation>SCR (si géométrie renseignée)</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="199"/>
        <source>CSV layer</source>
        <translation>Couche CSV</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="211"/>
        <source>Create vector layer from CSV file</source>
        <translation>Créer une couche depuis un fichier CSV</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="219"/>
        <source>Import from CSV</source>
        <translation>Import depuis CSV</translation>
    </message>
    <message>
        <location filename="../import_from_csv_algorithms.py" line="223"/>
        <source>This algorithm loads a CSV file as a vector layer, with or without geometry. If present, geometry may be given as one WKT column or as two X/Y columns.</source>
        <translation>Cet algorithme charge une couche vectorielle depuis un fichier CSV dans lequel les géométries sont données au format WKT dans une colonne.</translation>
    </message>
</context>
<context>
    <name>_AbstractAttributeDiffAlgorithm</name>
    <message>
        <location filename="../other_csv_algorithms.py" line="141"/>
        <source>&lt;p&gt;No differences found&lt;/p&gt;</source>
        <translation>&lt;p&gt;Aucune différence trouvée&lt;/p&gt;</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="146"/>
        <source>Attribute difference report</source>
        <translation>Rapport sur les différences attributaires</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="146"/>
        <source>CSV Tools QGIS Extension</source>
        <translation>Extension QGIS CSV Tools</translation>
    </message>
    <message>
        <location filename="../other_csv_algorithms.py" line="146"/>
        <source>Differences found</source>
        <translation>Différences trouvées</translation>
    </message>
</context>
</TS>
