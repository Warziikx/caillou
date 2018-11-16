# Commandes

Démarrer l'application : ```set FLASK_DEBUG=1 && flask run```

# Notation
- 12 points sur la récupération des données des produits.
- 8 points pour le serveur flask et l’interface
Bonus:
- + de 1000 produits (1 point)
- Interface pas trop moche (1 point) 

# Calcul du score

```
SCORE = ((0.6 * nutriscore) + (0.4 * novascore) + (0.1 * bio/pasbio)) * 100
```

Cas particulier :
* L'eau a un score de 100
* Les alcools ne peuvent pas être notés
* Certains produits n'ont pas toutes les infos, on les ignores.

## API

https://en.wiki.openfoodfacts.org/API/Read/Search

Pour la recherche de produit (search_terms à modifier):
 - https://world.openfoodfacts.org/cgi/search.pl?search_terms=banania&search_simple=1&action=process&json=1

Pour vérifier que nos données sont bonnes:
 - https://world.openfoodfacts.org/cgi/search.pl