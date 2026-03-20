# Gestionnaire_mot_de_passe
Script de gestion sécurisé d'une trousse de mots de passes liés à plusieurs comptes

# Description du programme :
Le programme permet de gérer vos mots de passe liés à plusieurs comptes (Gmail, Facebook, etc.) d’une manière sécuritaire. Votre trousse de mots de passe est protégée par un secret unique (un autre mot de passe). Chaque fois que vous voulez accéder à un de vos comptes, vous déverrouillez les informations requises dans le gestionnaire en fournissant le secret. Voici plus de détails techniques sur les fonctionnalités de ce gestionnaire :

— Il y a un fichier JSON (trousse.json) sur notre disque dur contenant des enregistrements ayant les informations suivantes :
  — URL : l’adresse URL du service.
  — user : le nom d’utilisateur lié au compte.
  — pwd : le mot de passe lié au compte associé à l’URL.
  — Une fois sur le disque dur, les informations liées à ces champs sont chiffrées séparément avec AES-CBC-128 bits.
  
La clé de protection est générée à partir d’un secret (un mot de passe) donné par l’utilisateur. Il s’agit du seul secret dont l’utilisateur a besoin de se souvenir. Chaque champ aura son propre iv (nécessaire pour le mode CBC) généré aléatoirement et enregistré à côté du champ en question pour faciliter son déchiffrement plus tard.

# Manipulation en ligne de commande: 

— l’option -a permet d’ajouter un nouvel enregistrement à la trousse de clé. Elle doit être suivie par le mot de passe de la trousse. Dans ce cas, l’utilisateur doit spécifier les champs de l’enregistrement avec les options suivantes :
  -url : donne l’URL.
  -user : donne le nom d’utilisateur (username).
  -pwd : donne le mot de passe permettant d’accéder au service.

Exemple :
gestionnaire_mot_de_passe.py -a 123pwd -url www.facebook.com -user alice@gmail.com -pwd 12t3r
— l’option -l suivie du mot de passe de la trousse permet des lister les enregistrements. L’affichage commence par une ligne indiquant le contenu de chaque colonne. Chaque enregistrement est précédé par un numéro de ligne. Tout doit apparaitre en clair sauf les noms d’utilisateurs et leurs mots de passe qui restent chiffrés et nous affichons "*****" à leurs places.

Exemple de commande :
gestionnaire_mot_de_passe.py -l 123pwd

Exemple de résultats.

ligne       url              user         pwd
1       www.facebook.com    *****        *****
2       www.gmail.com       *****        *****

— l’option -d suivie du mot de passe de la trousse permet d’afficher une ligne particulière tout en déchiffrant certains champs de plus. Le numéro de la ligne est spécifié avec l’option -i. Si nous voulons déchiffrer le nom, nous le spécifions avec le champ -user et si nous voulons déchiffrer le mot de passe, nous le spécifions avec l’option -pwd. Autrement, ces informations restent chiffrées. L’exemple suivant permet d’afficher le contenu de toute la ligne numéro 1 en clair :

gestionnaire_mot_de_passe.py -d 123pwd -i 1 -user -pwd

Exemple de résultats.

ligne         url                 user            pwd
1       www.facebook.com      alice@gmail.com    12t3r

Un autre exemple 

gestionnaire_mot_de_passe.py -d 123pwd -i 2 -pwd

ligne         url          user        pwd
2       www.gmail.com     *****       5ewr1
