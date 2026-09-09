# FileShed

> Un atelier agentique dans Open WebUI : traiter des données, transformer des documents et des médias, éditer précisément, collaborer et remettre des fichiers utilisables. Le stockage persistant en était la fondation, pas toute la raison d'être.

**Retraité.** Le code et les choix de conception de FileShed restent disponibles. OpenTerminal couvre désormais une grande partie des besoins d'origine de son auteur ; c'est sa raison de mettre le projet à la retraite, pas une promesse d'équivalence complète ni de compatibilité avec l'Open WebUI actuel.

## Travailler depuis une conversation

Avec `shed_exec`, un modèle utilisant des appels d'outils pouvait inspecter, rechercher, transformer et regrouper des fichiers au moyen de programmes explicitement autorisés. Ces commandes dépendent des logiciels installés sur l'hôte : une commande autorisée n'est pas nécessairement disponible. Ce n'est ni un shell sans restrictions ni un service d'exécution de Python arbitraire.

Les outils SQLite importent du CSV, exécutent des requêtes et exportent les résultats. Les données intermédiaires restent dans des fichiers plutôt que d'être recopiées à chaque message. Pandoc, FFmpeg et les autres commandes disponibles permettent de transformer documents et médias. La production PDF et le traitement d'images nécessitent les outils correspondants.

Les modifications par ligne ou motif, les changements d'octets et un parcours explicite verrouiller/éditer/enregistrer-ou-annuler permettent des changements précis. Documents et Groupes disposent d'un historique Git automatique ; Stockage est un espace de travail personnel, pas le versionnement automatique de tous les fichiers.

## Un atelier privé et des documents partagés

Pièces jointes importe les fichiers de la conversation en cours. Stockage conserve les fichiers de travail personnels entre les conversations. Documents conserve les documents personnels avec Git. Groupes repose sur l'appartenance aux groupes Open WebUI et sur les modes `owner`, `group` et `owner_ro` pour le travail partagé.

La création d'archives ZIP et les liens de téléchargement Open WebUI transforment le travail en livrable. Ces liens nécessitent une session Open WebUI authentifiée ; ce ne sont pas des liens publics de partage. L'aide par tâche `shed_help`, la découverte des commandes, les sorties limitées et les erreurs correctives rendent cette interface utilisable par les appels d'outils d'un modèle.

## Suivre un parcours complet

L'exemple documenté part de données sur les pays, convertit du JSON en CSV, l'importe dans SQLite, calcule des densités de population, classe les résultats, exporte du CSV et remet un ZIP à télécharger. Le parcours sur ce site illustre cette séquence ; ce n'est pas un agent actif ni une garantie de nombre de tours. Les téléchargements réseau nécessitent l'autorisation explicite de l'administrateur.

## Les limites à connaître

Les listes de commandes autorisées, la validation des chemins et arguments, les quotas, les délais et les modes réseau (`disabled`, `safe`, `all`) sont des protections applicatives, pas un bac à sable du système d'exploitation. L'extension dépend d'API Open WebUI. Les verrous sont conçus pour une instance unique, pas une coordination distribuée.

Le code comprend également un chiffrement facultatif des fichiers personnels avec AES-256-GCM et Argon2id. Les groupes restent non chiffrés, les clés utilisées à l'exécution sont exposées au processus hôte, les commandes shell voient les octets chiffrés et la perte de la clé fait perdre l'accès. Ce n'est pas un chiffrement universel de bout en bout. Consultez ensemble le code et le guide concerné avant d'activer une fonction : les documents et l'implémentation de ce projet retraité ne promettent pas une compatibilité avec un hôte plus récent.

## Explorer le projet

- [Présentation](index.html) : opérations, espaces de travail et parcours de traitement des données.
- [Guide d'origine, en anglais](https://github.com/Fade78/Fileshed/blob/main/README.md) : installation, exemples et référence des fonctions.
- [Spécification de conception, en anglais](https://github.com/Fade78/Fileshed/blob/main/docs/SPEC.md) : propriété, protections, architecture, verrous et chiffrement.
- [Implémentation](https://github.com/Fade78/Fileshed/blob/main/Fileshed.py) : outils publics et logique interne.
- [Licence](https://github.com/Fade78/Fileshed/blob/main/LICENSE) : licence MIT originale et attribution.
