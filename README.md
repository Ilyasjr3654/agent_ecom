# agent_ecom
Système multi-agents de support client e-commerce

## Données du projet

Le pack de données est décrit dans [data/README.md](data/README.md).

| Source | Contenu | Utilisation |
| --- | --- | --- |
| ABCD v1.1 | 10 042 dialogues, règles, ontologie et réponses candidates | Actions, intentions et politiques de support |
| Olist | 99 441 commandes et 7 tables associées | Outils de suivi des commandes |
| Customer Support on Twitter | 10 000 fils, 41 601 tweets, 8 enseignes sélectionnées | Conversations réelles de support |
| Amazon Reviews 2023 | Téléchargement local proposé, textes non redistribués | Fiches produit et avis pour le RAG |

Les fichiers ABCD, Olist et Twitter sont compressés et importés par le workflow
[Import project datasets](https://github.com/Ilyasjr3654/agent_ecom/actions/workflows/import-datasets.yml).
Ce workflow vérifie les empreintes des sources et publie les données dans `data/`.

Python **3.11+**, sans dépendance externe pour préparer et vérifier les données :

```bash
python scripts/validate_datasets.py
# Reconstituer les mêmes fichiers depuis les sources, si nécessaire :
python scripts/prepare_datasets.py
# Télécharger les fiches produit Amazon uniquement en local :
python scripts/download_amazon.py --metadata-only
```

Les jeux restent indépendants : aucun lien client/commande/produit n'est inventé
entre Twitter, ABCD, Olist et Amazon. ABCD est un corpus de conversations humaines
scénarisées avec des clients fictifs. Les commandes Olist sont historiques et
les conversations Twitter ne constituent pas un jeu d'intentions déjà annoté.

Voir les [licences et attributions](data/LICENSES.md) avant réutilisation.
