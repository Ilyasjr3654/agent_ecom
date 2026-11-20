# Fiche de suivi des projets agents IA

PFA • EMSI Casablanca • 5IA Data G3 • Présentation de l’avancement et plan de correction

Groupe : **5IA Data G3 — trinôme**   Projet n° : **43**   Date : **20 novembre 2026**

Intitulé du projet : **Système multi-agents de support client e-commerce**

Membres : **Ilyas Kharroubi, Ilyas Loulidi et Ziad Serray**

Jalon examiné : **Cadrage initial — cahier des charges v1.0**   Prochain point : **27 novembre 2026 (date proposée)**

> État déclaré sur la base des documents transmis : cahier des charges rédigé, réalisation logicielle non démontrée. Les responsabilités, échéances et objectifs ci-dessous sont des propositions à valider par le trinôme et l’encadrant. Aucun résultat expérimental ni déploiement n’est présenté comme déjà obtenu.

## Utilisation de la fiche

Avant chaque point, chaque groupe complète les réponses et rassemble les preuves. Présenter en 10 minutes : bilan, démonstration, résultats et blocages. Prévoir ensuite 5 minutes de questions. Chaque membre explique sa contribution et un choix technique.

Pour chaque rubrique, distinguer ce qui est prévu, commencé, démontré ou bloqué. Une fonction est démontrée lorsqu’un scénario reproductible et son résultat peuvent être vérifiés. Justifier toute question sans objet. Si un élément manque, indiquer la correction et son échéance.

## Bilan et périmètre

**1. Quel problème métier traitez-vous, pour quel utilisateur et avec quel résultat attendu ?**

Preuve à présenter : Un cas d’usage précis et un critère de réussite mesurable.

Réponse du groupe :

**État : cadrage rédigé.** Nous traitons les demandes répétitives reçues par le support d’une boutique en ligne : suivi de commande, retour/remboursement et questions produit. Les utilisateurs sont le client et le conseiller chargé des cas complexes. Le résultat attendu est une réponse fondée sur les données, conforme aux règles et accompagnée d’un transfert humain si nécessaire. Exemple : retrouver le statut exact d’une commande autorisée, citer son identifiant interne et ne rien inventer si elle est inconnue. Critère proposé : toutes les assertions de statut doivent correspondre aux données de référence des cas de test.

**2. Quel périmètre MVP avez-vous retenu et quelles fonctions avez-vous reportées ?**

Preuve à présenter : Liste des fonctions incluses et exclues, validée par le groupe.

Réponse du groupe :

**État : périmètre proposé, à valider.** MVP : chat avec historique, tri des demandes, consultation de commandes, RAG produit avec sources, vérification déterministe des règles de retour, simulation d’action, transfert à un humain, traces et évaluation reproductible. Trois parcours prioritaires : suivi, retour et question produit. Sont reportés : fine-tuning LoRA, français/darija, gestion avancée des comptes, modification d’adresse et administration complète des règles. Sont exclus : vrais paiements, remboursements, messages externes, clients réels, application mobile et voix. Langue initiale : anglais.

**3. Qu’aviez-vous prévu depuis le dernier point et qu’avez-vous réellement terminé ?**

Preuve à présenter : Fonctions terminées, en cours et bloquées, avec preuve pour chacune.

Réponse du groupe :

**État : premier point ; aucun point précédent documenté.** Terminé au niveau documentaire : choix du projet n°43, rédaction du cahier des charges v1.0, identification de quatre sources et description de l’architecture envisagée. Preuve disponible : cahier des charges transmis. À réaliser : acquisition et audit des fichiers, échantillons annotés, code, tests et déploiement. Aucun téléchargement de dataset, commit du projet ou résultat expérimental n’a été fourni comme preuve d’avancement. Les licences, le budget LLM et la langue restent à valider.

**4. Que peut-on exécuter aujourd’hui sans intervention manuelle cachée ?**

Preuve à présenter : Démonstration de bout en bout sur un scénario reproductible.

Réponse du groupe :

**État : non démontré.** Aucun parcours exécutable de bout en bout n’est attesté à ce jour. Le premier scénario visé est une demande de suivi : session client de test, identifiant d’une commande du jeu de développement, appel de l’outil autorisé, réponse contenant le statut exact et trace de l’exécution. Deux variantes vérifieront le refus d’une commande appartenant à un autre client et l’absence d’invention pour un identifiant inexistant. La preuve attendue est une commande de lancement et un test automatisé reproductible.

État général : **Conforme au jalon documentaire de cadrage ; validation pédagogique et audit des données à réaliser avant le développement complet.**

Décision ou aide attendue de l’enseignant : **Valider le trinôme, le MVP en anglais, l’usage d’ABCD comme dialogues humains scénarisés, le caractère facultatif du fine-tuning et le budget modèle. Encadrant : nom non communiqué.**

## Données et architecture

**5. Quel dataset ou corpus utilisez-vous exactement et comment y accède-t-on ?**

Preuve à présenter : Nom, URL, version ou date, licence et fichiers retenus.

Réponse du groupe :

**État : sources sélectionnées ; fichiers locaux et versions exactes à figer lors de l’acquisition.** Les références sont les quatre sources du cahier des charges, et non Bitext, qui n’est pas retenu dans ce cadrage.

| Source et accès | Fichiers / sous-ensemble retenus | Licence et version |
| --- | --- | --- |
| [Customer Support on Twitter — Kaggle](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter) | `twcs.csv` ; fils complets de marques de commerce sélectionnées après inspection | CC BY-NC-SA 4.0 affichée ; version Kaggle, date d’acquisition et SHA-256 à enregistrer |
| [Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | `olist_orders_dataset.csv`, `olist_customers_dataset.csv`, `olist_order_items_dataset.csv`, `olist_order_payments_dataset.csv`, `olist_products_dataset.csv`, `olist_order_reviews_dataset.csv` ; sous-ensemble cohérent de commandes | CC BY-NC-SA 4.0 ; données historiques 2016–2018 ; version téléchargée et SHA-256 à enregistrer |
| [Amazon Reviews 2023 — McAuley Lab](https://amazon-reviews-2023.github.io/main.html) | Sous-ensemble proposé : `All_Beauty.jsonl.gz` et `meta_All_Beauty.jsonl.gz`, joints par `parent_asin` ; limiter l’index initial à environ 1 000 produits | Édition 2023 ; conditions applicables aux données à confirmer avant ingestion, sans assimiler la licence du code à celle des données |
| [ABCD — ASAPP](https://github.com/asappresearch/abcd) | `data/abcd_v1.1.json.gz`, `data/guidelines.json`, `data/kb.json`, `data/ontology.json` | Version de données v1.1 ; licence MIT affichée par le dépôt contenant code et données ; commit exact et SHA-256 à figer |

Un manifeste conservera pour chaque fichier : URL, version/commit, date d’acquisition, licence, taille, empreinte et transformations. L’accès Kaggle pourra nécessiter une authentification locale ; les secrets ne seront pas déposés dans Git.

**6. Les données couvrent-elles réellement le problème posé ? Que simulez-vous ?**

Preuve à présenter : Variables utiles, labels, limites et distinction entre réel et synthétique.

Réponse du groupe :

**État : couverture partielle identifiée.** Twitter apporte des échanges publics réels mais pas les labels métier nécessaires. Olist apporte des commandes historiques anonymisées : statut, dates, lignes et paiements. Amazon apporte les fiches produit et avis ; les avis restent des opinions, pas des caractéristiques garanties. ABCD contient des dialogues humains scénarisés avec clients fictifs et actions annotées. Sont simulés : l’identité de connexion, les rapprochements entre sources, les scénarios transversaux et tout remboursement. Aucun identifiant Olist ne sera présenté comme naturellement lié à un produit Amazon ou à un client Twitter. Le prototype ne représente pas les données opérationnelles d’un commerçant marocain.

**7. Comment avez-vous nettoyé, annoté et séparé les données sans fuite ?**

Preuve à présenter : Pipeline, exemples avant/après, splits et règles anti-doublons.

Réponse du groupe :

**État : pipeline prévu, non exécuté.** Normaliser l’encodage, retirer les entrées vides, dédupliquer et masquer les identifiants personnels en conservant les liens nécessaires à la reconstruction des fils. Conserver les splits officiels d’ABCD. Pour Twitter, répartir les conversations complètes et regrouper les quasi-doublons ; viser 70/15/15 avec graine 42. Deux membres annoteront indépendamment une partie de l’échantillon, puis arbitreront leurs désaccords. Les reformulations et traductions d’un même exemple resteront dans le même split. Les réponses attendues du test resteront hors de l’index RAG ; l’index contiendra seulement les documents auxquels le système a droit.

**8. Quelle insuffisance des données risque de fausser votre conclusion ?**

Preuve à présenter : Biais identifié et mesure concrète pour en réduire l’effet.

Réponse du groupe :

**État : risques identifiés.** Les principales limites sont le décalage entre sources, l’absence de liens réels entre conversations et commandes, les messages Twitter courts dont une partie de la résolution peut se dérouler en privé, les langues différentes et les dates anciennes d’Olist. Nous séparerons les évaluations par source et distinguerons les cas réels des scénarios construits. L’anglais sera la langue du MVP ; les avis portugais d’Olist ne seront pas mélangés à l’évaluation anglaise. Les conclusions porteront sur ce prototype et ne démontreront pas une performance en production au Maroc.

**9. Quels composants fonctionnent et comment échangent-ils les données ?**

Preuve à présenter : Schéma d’architecture à jour et exemple de requête API.

Réponse du groupe :

**État : architecture conçue sur document ; fonctionnement non démontré.** Flux prévu : interface Next.js → API FastAPI → orchestrateur LangGraph → outil commandes PostgreSQL, recherche produit pgvector ou moteur de règles → contrôle de réponse → chat ou console humaine. PostgreSQL conservera conversations et états ; Langfuse recevra des traces filtrées. Redis sera introduit pour les tâches asynchrones si nécessaire. Exemple de contrat proposé : `POST /api/conversations/{id}/messages` avec `{"text":"Where is my order?","order_id":"<id_autorisé>"}`. Le client est déterminé par la session authentifiée, pas par un identifiant libre fourni au LLM.

**10. Pourquoi avez-vous choisi ces frameworks plutôt qu’une solution plus simple ?**

Preuve à présenter : Justification liée au besoin, aux compétences et aux ressources.

Réponse du groupe :

**État : choix proposés selon le catalogue.** FastAPI centralise les outils Python et la validation des entrées ; LangGraph rend explicites les embranchements, états et interruptions humaines ; PostgreSQL avec pgvector réunit données relationnelles et recherche documentaire. Next.js fournit le chat et la console de reprise. Langfuse vise l’analyse des appels, Ragas une partie de l’évaluation, Docker Compose la reproductibilité. Nous utiliserons un seul framework d’orchestration. Redis et les traitements parallèles seront ajoutés lorsqu’un besoin mesuré le justifie. Une chaîne simple et un agent unique serviront de comparaisons.

**11. Comment gérez-vous l’état, la mémoire, les erreurs et les reprises ?**

Preuve à présenter : Modèle d’état, journal d’une exécution et exemple d’échec traité.

Réponse du groupe :

**État : conception prévue.** L’état contient l’identifiant de conversation, la session autorisée, l’intention, les résultats d’outils, les références documentaires, l’action proposée et le statut d’escalade. La mémoire est limitée à la conversation avec résumé des anciens tours. Les reprises s’appuieront sur des états persistés et des identifiants de requête. Prévoir un délai maximal, une nouvelle tentative sur erreur transitoire et une réponse d’échec contrôlée. Les actions simulées auront une clé d’idempotence pour éviter un double traitement. Un outil indisponible ne déclenchera jamais l’invention d’un statut ou d’un remboursement.

Correction prioritaire sur les données ou la conception : **Figer les fichiers et licences, séparer les identités de chaque source et documenter les associations simulées. Responsable proposé : Ilyas Kharroubi. Échéance : 24/11/2026.**

## Fonctionnement des agents et protocole

**12. Quelle décision l’agent prend-il et quels outils appelle-t-il ?**

Preuve à présenter : Trace d’un scénario avec entrées, décisions, appels et sorties.

Réponse du groupe :

**État : comportement spécifié.** Le système choisit la route de traitement et les informations à demander. Les outils envisagés sont `get_order_status`, `search_product_docs`, `evaluate_return_policy` et `create_handoff`. Les paramètres sont validés avant appel. Pour une demande de retour : identifier la commande autorisée, lire ses données, appliquer une règle versionnée, puis proposer la décision et son motif. Toute action à effet reste simulée et soumise aux permissions applicatives. L’absence d’information indispensable provoque une demande de précision ou un transfert.

**13. Quel résultat obtenez-vous avec des règles ou une chaîne sans agent ?**

Preuve à présenter : Comparaison sur les mêmes cas, avec le même budget de calcul.

Réponse du groupe :

**État : aucune mesure disponible.** B1 utilisera des mots-clés et réponses prédéfinies ; B2 un agent sans RAG servira à mesurer l’effet de l’accès documentaire ; B3 un agent unique disposera des mêmes outils, documents et politiques que le multi-agents. La comparaison B3/multi-agents sera la principale pour isoler l’apport de l’orchestration. Tous seront testés sur les mêmes cas, avec un modèle commun lorsque pertinent, des plafonds de calcul comparables et un coût mesuré. Aucun gain de qualité ou de coût n’est acquis avant expérimentation.

**14. Si plusieurs agents collaborent, quel rôle distinct remplit chacun ?**

Preuve à présenter : Rôles, échanges et comparaison avec un agent unique. Sinon expliquer l’absence de multi-agents.

Réponse du groupe :

**État : rôles prévus.** L’orchestrateur distribue les tâches ; le tri propose l’intention et le besoin d’escalade ; le suivi consulte la commande ; l’agent produit recherche les sources ; le composant politiques vérifie les règles ; la rédaction compose la réponse ; l’escalade prépare le dossier humain. Un composant n’implique pas nécessairement un appel LLM : politiques, validation et une partie de l’escalade seront déterministes. Les résultats structurés sont échangés dans l’état partagé. Seules les branches utiles à la demande seront exécutées pour maîtriser la latence.

**15. Comment vérifiez-vous une sortie du LLM avant de l’utiliser ?**

Preuve à présenter : Validation du format, contrôle des sources, test métier et cas d’abstention.

Réponse du groupe :

**État : contrôles prévus.** Valider le schéma des sorties structurées, les noms d’outils et types de paramètres ; vérifier l’appartenance de la commande à la session et appliquer les règles métier en code. Les citations devront désigner des documents réellement retrouvés et soutenir les affirmations. Une source absente ou contradictoire provoquera une abstention ou une clarification. Une note de confiance auto-déclarée par le LLM ne sera pas assimilée à une probabilité fiable : les seuils seront calibrés sur la validation et combinés à la disponibilité des preuves.

**16. Quelles actions exigent une validation humaine et quelles limites imposez-vous ?**

Preuve à présenter : Permissions, plafond d’appels, coût maximal et scénario d’action refusée.

Réponse du groupe :

**État : politique MVP proposée.** Toute simulation de remboursement, d’annulation ou de changement de données exige une confirmation humaine explicite ; aucune transaction réelle n’est intégrée. La lecture de commande est limitée au client autorisé. Plafonds initiaux proposés : 6 appels LLM, 8 appels d’outils et 60 secondes par demande, puis arrêt contrôlé. Un plafond monétaire sera fixé avant activation d’une API payante, après choix du modèle. Cas de refus attendu : demande de remboursement sans commande autorisée, même si le client demande d’ignorer les règles.

**17. Quels tests prouvent que les fonctions annoncées marchent réellement ?**

Preuve à présenter : Tests automatisés, résultat daté et anomalies encore ouvertes.

Réponse du groupe :

**État : aucun test exécuté fourni.** Prévoir des tests unitaires des règles, validateurs et autorisations ; des tests d’intégration de consultation et recherche ; trois tests de bout en bout pour suivi, retour et question produit ; des tests de reprise et d’idempotence. Les limites temporelles des retours seront testées avant, à et après l’échéance définie. Chaque rapport indiquera date, commit, modèle, données et résultats. Les simulations de réponses LLM serviront aux tests logiciels ; l’évaluation avec le modèle réel sera identifiée séparément.

**18. Quels indicateurs avez-vous choisis et pourquoi conviennent-ils au projet ?**

Preuve à présenter : Définition des métriques, baseline et protocole de mesure.

Réponse du groupe :

**État : protocole défini, seuils à calibrer sur validation.** F1 macro et exactitude pour le tri ; précision et rappel de recherche sur questions annotées ; fidélité RAG, validité et pertinence des citations ; exactitude de décision et taux de réussite des scénarios de retour ; précision/rappel de l’escalade. Mesurer aussi latences médiane/P95, appels, jetons et coût par conversation. Les scores automatisés seront complétés par une revue humaine. Les métriques propres à ABCD ne porteront ce nom que si le protocole officiel est reproduit ; sinon elles seront qualifiées de métriques adaptées.

Correction prioritaire sur l’agent ou les tests : **Écrire les contrats d’outils, les règles d’autorisation et une comparaison équitable agent unique/multi-agents ; préparer les tests avant les appels réels. Responsable proposé : Ilyas Loulidi, revue du trinôme. Échéance : 25/11/2026.**

## Résultats et déploiement

**19. Quels résultats chiffrés obtenez-vous sur un jeu de test distinct ?**

Preuve à présenter : Tableau baseline/solution, taille du test, latence et coût par scénario.

Réponse du groupe :

**État : non mesuré.** Aucun chiffre de performance n’est disponible. Proposition : constituer un corpus annoté d’environ 300 conversations Twitter (210/45/45 sous réserve de représentation des classes), un jeu de 50 questions produit et un sous-ensemble de test ABCD choisi sans consulter ses réponses pour régler le système. Les effectifs réels seront enregistrés après audit. Les variantes et le multi-agents seront comparés sur les mêmes jeux gelés, avec analyse d’erreurs et indication de l’incertitude liée aux petits effectifs.

**20. Quels sont vos trois échecs les plus importants et comment les expliquez-vous ?**

Preuve à présenter : Entrées, sorties observées, causes probables et correction envisagée.

Réponse du groupe :

**État : aucun échec observé documenté ; trois risques à tester.** (1) Confusion entre suivi et retour : vérifier les demandes mixtes et permettre une clarification. (2) Réponse produit non soutenue : vérifier la recherche, les citations et l’abstention quand les documents ne suffisent pas. (3) Retour autorisé à tort : vérifier les dates, l’identité de test et les conditions par tests de frontières. Ces situations sont des scénarios prévus, pas des incidents déjà constatés. Les sorties observées seront ajoutées après les premières exécutions.

**21. Quelles entrées difficiles ou hostiles avez-vous testées ?**

Preuve à présenter : Données manquantes, outil indisponible, prompt malveillant, réponse non sourcée.

Réponse du groupe :

**État : tests prévus, non exécutés.** Jeux difficiles : commande absente, commande d’un autre client, produit inconnu, message vide ou très long, demande multilingue, plusieurs intentions, outil indisponible et documents contradictoires. Jeux hostiles : « ignore les règles », demande de secrets, faux identifiant client et instruction malveillante insérée dans un avis produit. Résultat attendu : appel autorisé seulement, informations provenant des outils, refus ou transfert motivé et aucune exposition de données d’un autre client. Les limites constatées seront consignées.

**22. Un autre groupe peut-il installer et lancer votre application ?**

Preuve à présenter : README vérifié, dépendances fixées et commande de lancement.

Réponse du groupe :

**État : installation reproductible à construire et à vérifier.** Livraison prévue : README, dépendances fixées, `.env.example` sans secret, scripts d’acquisition et manifeste des données. Le démarrage cible sera `docker compose up --build` après configuration et préparation documentée des données ; les tests auront une commande dédiée. Ces commandes constituent une cible de livraison, pas une exécution validée aujourd’hui. La preuve sera une installation sur une machine distincte avec étapes, temps et difficultés consignés.

**23. Quelle version est déployée et quel parcours avez-vous validé ?**

Preuve à présenter : Commit ou version, environnement, démonstration et résultat du test de bout en bout.

Réponse du groupe :

**État : aucune version logicielle déployée attestée.** La v1.0 disponible correspond au cahier des charges uniquement. L’environnement cible est local sous Docker Compose. La première version exécutable sera identifiée par un commit Git et un tag après succès des parcours de suivi, de retour et de question produit. La démonstration conservera l’identifiant du scénario, la version des sources, le modèle utilisé et le résultat du test. Aucun lien de déploiement ni SHA de commit n’est inventé dans cette fiche.

**24. Comment protégez-vous les secrets, les accès et les données ?**

Preuve à présenter : Configuration sans secrets, contrôle d’accès et politique de journalisation.

Réponse du groupe :

**État : exigences prévues, à tester.** Secrets dans des variables d’environnement et hors du dépôt ; accès séparés client, conseiller et administrateur ; contrôle serveur de l’appartenance des commandes ; outils de consultation avec requêtes paramétrées et droits limités. Masquer les identifiants personnels avant traces et exports. Les données externes sont traitées comme du contenu, jamais comme des consignes d’exécution. Vérifier ce qui est transmis au fournisseur LLM. Prévoir des tests d’accès interdit, une suppression des sessions de test et une recherche de secrets avant publication.

### Résultats à comparer

| Indicateur | Baseline | Solution | Jeu ou scénario |
| --- | --- | --- | --- |
| F1 macro du tri | Non mesurée — B1/B3 à construire | Non mesurée | Conversations annotées, test gelé |
| Exactitude de consultation | Non mesurée | Non mesurée | Statuts Olist et cas d’accès autorisé/interdit |
| Fidélité et citations soutenant la réponse | Non mesurées | Non mesurées | Questions produit et sources Amazon autorisées |
| Décision de retour et respect des étapes | Non mesurés | Non mesurés | Sous-ensemble ABCD et règles figées |
| Précision et rappel d’escalade | Non mesurés | Non mesurés | Cas annotés à escalader / à traiter |
| Latence médiane et P95 | Non mesurées | Non mesurées | Même environnement et mêmes scénarios |
| Coût et nombre d’appels par conversation | Non mesurés | Non mesurés | Modèle et tarifs datés, jetons tracés |

Pour un projet industriel, démontrer en simulation et expliquer les limites du passage au réel. Pour un projet informatique, montrer les droits accordés aux outils et les actions qui exigent une validation humaine.

## Contributions et corrections

**25. Quelle contribution chaque membre peut-il présenter et expliquer ?**

Preuve à présenter : Tâches, commits, résultats et revue croisée. Chaque membre explique au moins un choix technique.

Réponse du groupe :

**État : répartition proposée, contributions de code non démontrées.**

| Membre | Responsabilité proposée | Preuve future et choix à expliquer |
| --- | --- | --- |
| Ilyas Kharroubi | Préparation Olist/Amazon, PostgreSQL, recherche documentaire et API métier | Manifeste, contrôles de jointures, exemple de recherche sourcée ; choix du schéma et des filtres |
| Ilyas Loulidi | Orchestration LangGraph, routage, intégration ABCD et moteur de règles | Trace d’un parcours, tests des règles ; choix entre graphe, règles et appels LLM |
| Ziad Serray | Interface, console humaine, instrumentation et déploiement Compose | Parcours client/conseiller, tableau de traces et procédure de lancement ; choix des indicateurs |

L’annotation, les tests d’acceptation, le rapport et les revues seront partagés. Les contributions effectives seront justifiées par commits et résultats au prochain jalon.

**26. Quel blocage menace le prochain jalon et de quelle aide avez-vous besoin ?**

Preuve à présenter : Cause précise, tentatives déjà faites et décision attendue.

Réponse du groupe :

**État : décisions ouvertes ; aucune panne technique observée.** Le prochain jalon dépend de l’acceptation des dialogues scénarisés ABCD dans l’exigence de données réelles, de l’autorisation du trinôme, de la langue et du budget LLM. Le cahier des charges identifie ces points ; aucune demande à l’encadrant ni réponse n’est attestée. Aide attendue : validation pédagogique de ces choix. Actions autonomes possibles immédiatement : inventaire des fichiers, vérification des licences, préparation des contrats d’outils et constitution des échantillons.

**27. Quelle affirmation ou fonctionnalité devez-vous corriger après cette revue ?**

Preuve à présenter : Écart entre prévu et observé, cause et preuve de correction attendue.

Réponse du groupe :

**État : corrections proposées à reporter au cahier des charges.** Remplacer « prouver que le multi-agents est plus fiable » par « mesurer dans quelles conditions il apporte un gain ». Distinguer données opérationnelles réelles, dialogues humains scénarisés et actions simulées. Maintenir séparés les produits Amazon et Olist, sauf correspondance explicitement artificielle. Corriger EF-13 : les retours humains enrichissent le développement ou une future version d’évaluation, jamais le test final utilisé pour annoncer les performances après ajustement. Preuve attendue : cahier des charges v1.1 et protocole révisé.

**28. Quelles sont vos trois prochaines actions prioritaires ?**

Preuve à présenter : Action observable, responsable nommé, échéance et test d’acceptation.

Réponse du groupe :

**État : actions proposées pour le prochain jalon.**

1. **Auditer les données — Ilyas Kharroubi — 24/11/2026 :** inventaire des quatre sources, empreintes des échantillons acquis, langues, champs et anomalies. Acceptation : données chargeables, contrôles de clés documentés, absence de jointure fictive présentée comme réelle.
2. **Définir les outils et les règles — Ilyas Loulidi — 25/11/2026 :** graphe des trois parcours, contrats d’outils et règles de retour versionnées. Acceptation : 10 exemples de décisions revus à la main, avec critères d’autorisation et d’abstention.
3. **Préparer le socle et les preuves — Ziad Serray — 27/11/2026 :** dépôt structuré, configuration locale et squelette chat/API avec données de test. Acceptation : lancement documenté, un aller-retour visible et une trace technique ; coordination avec les deux autres membres.

**29. Faut-il réduire le périmètre ou revoir le choix des données ou des outils ?**

Preuve à présenter : Décision argumentée et effet sur le planning et les livrables.

Réponse du groupe :

**État : réduction proposée du MVP, sans changement de sujet.** Conserver les trois parcours prioritaires, une langue et un seul orchestrateur. Utiliser une seule catégorie Amazon et des échantillons maîtrisables ; traiter les quatre sources dans des évaluations distinctes. Reporter le fine-tuning, le multilingue, l’administration avancée et la montée en charge. Une fonction déterministe ne deviendra pas un agent LLM par principe. Le planning conserve 10 semaines ; cette réduction réserve du temps aux tests, à la comparaison avec l’agent unique et à la démonstration.

**30. Quelle preuve présenterez-vous lors du prochain point d’avancement ?**

Preuve à présenter : Jalon vérifiable et scénario exact qui permettra de le valider.

Réponse du groupe :

**État : preuve attendue au point proposé du 27/11/2026.** Présenter le cahier des charges v1.1, la répartition validée, un inventaire des sources et un mini-échantillon inspecté. Démonstration visée : démarrer le socle, envoyer une demande de suivi associée à une session de test, consulter une commande autorisée et afficher le statut exact avec une trace. Tester ensuite un identifiant inconnu et un accès interdit. Le service peut encore être déterministe à ce jalon ; aucune capacité multi-agents ne sera annoncée avant sa démonstration.

### Plan de correction à valider

| Action prioritaire | Responsable | Échéance | Preuve de correction |
| --- | --- | --- | --- |
| 1. Auditer les sources et expliciter les données simulées | Ilyas Kharroubi | 24/11/2026 — proposée | Inventaire, échantillons lisibles, licences et contrôles de clés |
| 2. Définir outils, règles et protocole comparatif | Ilyas Loulidi | 25/11/2026 — proposée | Contrats, graphe des parcours, 10 décisions revues et protocole sans fuite |
| 3. Préparer le socle et le premier parcours de suivi | Ziad Serray, intégration avec le trinôme | 27/11/2026 — proposée | Démarrage documenté, aller-retour chat/API, trace et cas d’erreur |

Décision de la revue : **Proposition du groupe : poursuivre le cadrage et corriger avant le prochain jalon, avec un MVP limité aux trois parcours prioritaires. Décision effective réservée à l’enseignant.**

Commentaire de l’enseignant : **Réservé à l’enseignant lors de la revue ; aucun commentaire reçu à ce jour.**
