# Sources, attributions et conditions des données

## ABCD — ASAPP Research

- Source : https://github.com/asappresearch/abcd
- Commit : `6b8700ce67c6b37b062dd7a60abc76d7ef832a97` ; données v1.1.
- Licence MIT du dépôt d'origine, reproduite dans `raw/abcd/LICENSE`.
- Auteurs : Derek Chen, Howard Chen, Yi Yang, Alex Lin et Zhou Yu.
- Publication : *Action-Based Conversations Dataset: A Corpus for Building More
  In-Depth Task-Oriented Dialogue Systems*, NAACL 2021, pages 3002–3017.
  https://aclanthology.org/2021.naacl-main.239/
- Changements : `utterances.json` compressé en gzip ; autres fichiers inchangés.

## Brazilian E-Commerce Public Dataset by Olist

- Auteur/fournisseur : Olist et les contributeurs indiqués sur Kaggle.
- Source : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Version renvoyée par l'API Kaggle lors de l'acquisition : 2.
- Licence affichée : **CC BY-NC-SA 4.0**.
  https://creativecommons.org/licenses/by-nc-sa/4.0/
  Texte : https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en
- Changements : compression gzip des CSV ; table de géolocalisation exclue.

## Customer Support on Twitter

- Auteur/fournisseur : Thought Vector et les contributeurs indiqués sur Kaggle.
- Source : https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter
- Version renvoyée par l'API Kaggle lors de l'acquisition : 10.
- Licence affichée : **CC BY-NC-SA 4.0**.
  https://creativecommons.org/licenses/by-nc-sa/4.0/
  Texte : https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en
- La page source demande de contacter Thought Vector pour les applications
  commerciales et l'utilisation du jeu complet. Ce dépôt distribue un
  sous-ensemble à usage académique non commercial sous la même licence.
- Changements : sélection de 10 000 composantes e-commerce, champ
  `conversation_id`, splits par composante, masquage emails/URLs, JSONL gzip.

Pour Olist et Twitter, conserver l'attribution et la licence, indiquer les
modifications et respecter les restrictions d'usage non commercial et de partage
des adaptations sous les mêmes conditions. Les données ne sont pas placées
sous une éventuelle licence du code de ce projet. Aucun fournisseur n'endosse ce projet.

## Amazon Reviews 2023 — McAuley Lab

- Source : https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
- Projet : https://amazon-reviews-2023.github.io/
- Précisions de l'éditeur sur l'absence de licence attribuée aux données :
  https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/discussions/1
- L'éditeur décrit un usage de recherche et indique ne pas pouvoir attribuer
  une licence aux données. Aucune autorisation générale de redistribution n'est
  déduite de la licence du code. Les textes ne sont donc pas inclus dans Git.
- Publication : *Bridging Language and Items for Retrieval and Recommendation*,
  2024. https://arxiv.org/abs/2403.03952
