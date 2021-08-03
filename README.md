# manufacturing-optimizer
Using python PuLP, Flask and variable inputs to optimise the product mix for maximum profit

Linear and integer programming are key techniques for discrete optimization problems and they pop up pretty much everywhere in modern business and technology sectors. 


To test with Powershell

$biketypes = "T1","T2","T3","T4"
$bike_profit = 45, 60, 55, 50
$part_names = "wheels","alloy_chassis","steel_chassis","hub_gears","derailleur_gears"
$parts_stock = 180, 40, 60, 50, 40
$bike_parts = (2,1,0,1,0),(2,0,1,0,1),(2,1,0,0,1),(2,0,1,1,0)

#,$bike_Parts | ConvertTo-Json -Depth 5 -Compress


$JSON = [PSCustomObject]@{
    'language' = 'Python'
    'bike_types' = $biketypes
    'bike_profit' = $bike_profit
    'part_names' = $part_names
    'parts_stock'= $parts_stock
    'bike_parts' = $bike_parts

} | ConvertTo-Json

Invoke-WebRequest -Uri 'http://localhost:5000/json-post' -ContentType 'application/json' -Method POST -Body $JSON
