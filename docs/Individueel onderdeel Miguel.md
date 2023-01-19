## Omschrijving

Voor het individuele onderdeel ga ik een simulated annealing algoritme maken, die optimaliseert op het probleem waarbij kabels gedeeld kunnen worden. simulated annealing is een versie van hill climber, waar in het begin het algoritme een verslechtering van de cost mag accepteren, in de hoop dat je hiermee eindigt in een lager locaal minimum. Naarmate de runtime afneemt zal het algoritme steeds minder een verslechtering accepteren.

## Nog te schrijven functies/classes

Voor dit onderdeel hoeven er geen nieuwe classes geschreven te worden. Qua functies heb ik er allereerst eentje nodig die huizen random aan batterijen verbindt, maar deze heb ik al geschreven voor de sd_hill_climber.py, dus deze kan rechtstreeks gekopiëerd worden. Vervolgens heb ik een functie nodig die daadwerkelijk het algoritme uitvoert. Hoe deze dit gaat doen is door constant een willekeurige swap te maken, en te kijken hoe deze de cost beinvloed. Vervolgens bereken je op basis van de "temperatuur" de kans dat deze verandering geaccepteerd wordt. Als je dit algoritme genoeg iteraties geeft, zullen er langzaam maar zeker geen verbeteringen meer zijn.

Ik wil ook een plot maken, die de cost van het grid plot ten opzichte van de iteratie waarop het programma zit. Als het goed is zie je dan in het begin een sterke daling van de cost, en uiteindelijk levelt deze uit.

## Experimenteel deel

Ik kan vervolgens ook testen of het algoritme een beter antwoord krijg als ik hem vraag om meerdere veranderingen te laten maken per stap, die geaccepteerd kunnen worden. Ook wil ik kijken hoe het resultaat verschilt wanneer ik de begintemperatuur, of de curve van de temperatuur aanpas.

# Aansluiting

Het programma sluit aan op het werk van de rest van het groep, doordat het één van de algoritmen is die een zo goed mogelijk antwoord probeert te zoeken voor onze casus. Het maakt natuurlijk gebruik van de reeds gecreëerde classes en de visualisatie, opdat je van het resultaat kan zien hoe goed de oplossing er intuitief uitziet. Natuurlijk kunnen de oplossingen van dit algoritme ook gebruikt worden om onze andere algoritmen mee te vergelijken, om te kijken hoe effectief ze onderling zijn