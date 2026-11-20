# Pack de données — PFA 43

Acquisition initiale : 20 novembre 2026. Les empreintes et versions des fichiers
sources sont figées dans `sources.lock.json`. `manifest.json` inventorie les
fichiers produits, leurs tailles, leurs empreintes SHA-256 et les effectifs vérifiés.

## ABCD

`raw/abcd/abcd_v1.1.json.gz` : jeu complet officiel, inchangé, avec les splits
`train` (8 034), `dev` (1 004) et `test` (1 004). Chaque conversation possède un
`convo_id`, un `scenario`, une conversation `original` et sa version `delexed`.

`guidelines.json`, `kb.json`, `ontology.json` et `utterances.json.gz` complètent
les dialogues. La dernière table sert à résoudre les identifiants de réponses
candidates. Les coordonnées dans les scénarios sont celles de clients fictifs
du protocole de collecte, pas celles de clients de la boutique du projet.

```python
import gzip, json
with gzip.open('data/raw/abcd/abcd_v1.1.json.gz', 'rt', encoding='utf-8') as f:
    abcd = json.load(f)
print(len(abcd['train']))
```

Conserver les splits officiels. Ne pas indexer les réponses attendues du test
dans le RAG. Le corpus sert de référence ; aucun fine-tuning n'a encore été exécuté.

## Olist

Les CSV de `raw/olist/` sont compressés sans modification de leur contenu.
Toutes les lignes des huit tables ci-dessous sont conservées ; la table
optionnelle de géolocalisation n'est pas incluse.

| Table | Lignes | Clés utiles |
| --- | ---: | --- |
| olist_orders_dataset | 99 441 | order_id, customer_id |
| olist_customers_dataset | 99 441 | customer_id, customer_unique_id |
| olist_order_items_dataset | 112 650 | order_id, order_item_id, product_id, seller_id |
| olist_order_payments_dataset | 103 886 | order_id, payment_sequential |
| olist_order_reviews_dataset | 99 224 | review_id, order_id |
| olist_products_dataset | 32 951 | product_id |
| olist_sellers_dataset | 3 095 | seller_id |
| product_category_name_translation | 71 | product_category_name |

Les prix sont en BRL et les données sont historiques. Plusieurs lignes de
paiement, d'article ou d'avis peuvent concerner une commande : ne pas supposer
une relation 1:1 ni additionner après une jointure qui multiplie les lignes.
Olist ne fournit pas une politique de remboursement opérationnelle.

```python
import csv, gzip
with gzip.open('data/raw/olist/olist_orders_dataset.csv.gz', 'rt',
               encoding='utf-8', newline='') as f:
    orders = list(csv.DictReader(f))
```

## Twitter — sous-ensemble e-commerce

`processed/twitter/{train,validation,test}.jsonl.gz` contient 10 000 composantes
de conversation choisies parmi 119 622 composantes éligibles, à partir des
réponses de huit enseignes : AmazonHelp, AskeBay, AskTarget, Walmart,
ArgosHelpers, NikeSupport, NeweggService et marksandspencer.

| Split | Fils | Tweets |
| --- | ---: | ---: |
| train | 7 000 | 29 299 |
| validation | 1 500 | 6 127 |
| test | 1 500 | 6 175 |

Chaque ligne conserve les champs CSV d'origine et ajoute `conversation_id`.
Les valeurs `inbound` restent des chaînes `True` / `False`, pas des booléens JSON.
Les champs de réponse conservent leur format CSV (chaîne d'identifiants séparés
par des virgules). Grouper les lignes par `conversation_id` avant utilisation et
reconstruire les branches à partir des liens de réponse ; l'ordre du fichier
ne garantit pas l'ordre chronologique.

Préparation : union des tweets reliés par les deux champs de réponse, sélection
par SHA-256 de `42:conversation_id`, répartition 70/15/15 par composante entière.
Toutes les lignes présentes dans la source pour chaque composante retenue sont
conservées, y compris les ramifications et d'éventuels autres comptes.
Les messages absents de la source ne sont pas reconstitués. Emails résiduels et
URLs sont masqués ; le texte de la source était déjà pseudonymisé. Cela ne
constitue pas une garantie d'anonymisation exhaustive.

L'absence de chevauchement des fils est vérifiée, mais les quasi-doublons
sémantiques et les éventuelles données personnelles restantes devront être
revus avant l'entraînement. Les labels suivi/retour/produit restent à annoter.

## Amazon — fichiers locaux uniquement

La fiche éditeur ne donne pas de licence explicite de redistribution des textes.
Le dépôt fournit donc un téléchargeur vers les fichiers officiels Hugging Face,
et ne republie pas les fiches ou avis. Voir `LICENSES.md`.

```bash
python scripts/download_amazon.py --metadata-only
# Pour ajouter également les avis All_Beauty :
python scripts/download_amazon.py
```

Les JSONL sont enregistrés dans `data/local/amazon/` (ignoré par Git), avec le
commit Hugging Face résolu et leurs empreintes. Les fichiers peuvent être
volumineux. Joindre `meta_All_Beauty.jsonl` et `All_Beauty.jsonl` sur `parent_asin`,
puis limiter l'index initial à environ 1 000 produits. Les avis sont des opinions,
pas des caractéristiques produit garanties. Le téléchargement Amazon complet
n'a pas été exécuté lors de la préparation de ce pack.

## Reproductibilité et vérifications

Python 3.11+ suffit. Le téléchargement initial représente environ 265 Mo, hors
Amazon. Prévoir environ 2 Go de RAM pour la préparation du graphe Twitter.

```bash
python scripts/prepare_datasets.py
python scripts/validate_datasets.py
```

Les sources sont mises en cache dans `.cache/datasets/`, hors Git. Si Kaggle
demande une connexion, télécharger les archives depuis les liens de `LICENSES.md`,
les nommer `olist.zip` et `twitter.zip`, puis les déposer dans ce cache. Ne jamais
committer de clé Kaggle. Toute empreinte différente interrompt l'import.

Contrôles : SHA-256 des sources et résultats, comptages des tables, références
commandes/clients/produits Olist pendant la préparation, absence de conversation
commune entre splits ABCD et Twitter, absence de tweet dupliqué dans les splits.
Ces contrôles ne mesurent pas encore la qualité d'un modèle.
