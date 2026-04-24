db = db.getSiblingDB('blog_db');


db.posts.insertMany([
    {
        titre: "Introduction à Docker",
        contenu: "Docker permet d'isoler des applications dans des conteneurs.",
        auteur: "Along",
        tags: ["devops", "conteneurisation"]
    },
    {
        titre: "Pourquoi utiliser FastAPI ?",
        contenu: "FastAPI est moderne, rapide et gère l'asynchrone nativement.",
        auteur: "Tom",
        tags: ["python", "api"]
    },
    {
        titre: "SQL ou NoSQL ?",
        contenu: "Les deux ont leurs avantages. Les architectures hybrides en tirent parti.",
        auteur: "Noah",
        tags: ["bdd", "architecture"]
    },
    {
        titre: "Gérer les volumes Docker",
        contenu: "Les volumes sont essentiels pour ne pas perdre la data au redémarrage.",
        auteur: "Adrien",
        tags: ["docker", "persistance"]
    },
    {
        titre: "La sécurité des bases de données",
        contenu: "Ne jamais mettre de mots de passe en dur, utiliser des .env !",
        auteur: "Tom",
        tags: ["sécurité", "bonnes-pratiques"]
    }
]);


print("Initialisation MongoDB terminée : 5 posts insérés dans blog_db.");