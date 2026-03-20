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
  
  -l suivie du mot de passe de la trousse permet des lister les enregistrements. L’affichage commence par une ligne indiquant le contenu de chaque colonne. Chaque enregistrement est précédé par un numéro de ligne.

  Les mots de passe qui restent chiffrés et afficherons "*****" à leurs places


