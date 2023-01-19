# Technische Beschrijving Sander Britton

In dit document ga ik een plan uitwerken voor mijn individuele onderdeel van de Smart Grid case. Eerst ga ik een omschrijving geven mijn onderdeel. Vervolgens ga ik uitschrijven wat ik hiervoor nog moet doen. Als laatste bespreek ik hoe dit onderdeel in het geheel van het project past.

## Omschrijving

Als individueel onderdeel wil ik een Plant Propagation Algorithm maken. Dit algoritme zou gebruik moeten kunnen maken van verschillende hill-climber algoritmes om zo dus voor own-cables en shared-cables te werken. Hierin zou ik dus ook eventueel kunnen testen met verschillende types hill-climbers.

Als extra onderdeel wil ik het ook mogelijk maken om de JSON files te visualiseren in een grid, wat nu alleen mogelijk is na het runnen van een algoritme.

## Wat te doen

Hier bespreek ik wat ik per onderdeel moet doen.

### Plant Propagation Algorithm
In principe hoef ik alleen het Plant Propagation Algorithm te schrijven, omdat we al een steepest descent hill climber hebben die ik kan gebruiken. Deze hill climber zal ik waarschijnlijk wel nog een class van moeten maken.

Voor de Plant Propagation Algorithm ga ik een apart bestand aanmaken met hierin een soort 'main' functie die gebruikt kan worden om de algorithm te laten runnen. Deze grote functie zal ik onderdelen in meerdere kleine functies om het overzicht te behouden. 

### JSON Visualisatie
Voor de visualisatie van JSON bestanden zal ik een bestand aanmaken om de JSON files in te lezen en deze om te zetten naar een correct Grid object. Hiermee kan ik namelijk de bestaande visualisatie weer hergebruiken.

## Aansluiting project

De plant Propagation Algorithm zal gebruikt kunnen worden om een oplossing te vinden voor het probleem. Hier mee kunnen de anderen hun eigen algoritme vergelijken met die van mij en dus bepalen of hun algoritme waarschijnlijk beter kan of niet. 

De JSON visualisatie kan gebruikt worden om de resultaten van lange runs op te slaan in JSON formaat en deze vervolgens later te visualiseren. Dit maakt het makkelijker om tweaks te maken aan de visualisatie, zonder het programma opnieuw lang te laten runnen. 