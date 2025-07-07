import os
import subprocess
import requests
from dotenv import load_dotenv
from crew import create_crew
import time
time.sleep(30)


load_dotenv()


def init_git_and_push(project_path, repo_name):
    import os
    import subprocess
    import requests

    github_token = os.getenv("GITHUB_TOKEN")
    github_username = os.getenv("GITHUB_USERNAME")

    if not github_token or not github_username:
        print("❌ GITHUB_TOKEN ou GITHUB_USERNAME manquant dans .env")
        return

    # Crée le repo distant s’il n’existe pas
    response = requests.post(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github+json"
        },
        json={"name": repo_name, "private": False}
    )

    if response.status_code not in [201, 422]:  # 422 = repo déjà existant
        print("❌ Erreur lors de la création du repo GitHub :", response.json())
        return

    print("✅ Repo GitHub prêt")

    git_url = f"https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git"

    # Init git
    subprocess.run(["git", "init"], cwd=project_path)

    # Vérifie s’il y a au moins un fichier, sinon crée README.md
    if not any(os.scandir(project_path)):
        readme_path = os.path.join(project_path, "README.md")
        with open(readme_path, "w") as f:
            f.write(f"# {repo_name}\n\nProjet généré automatiquement.")
        print("📄 README.md ajouté car le projet était vide.")

    # Ajoute et commit
    subprocess.run(["git", "add", "."], cwd=project_path)

    commit = subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=project_path,
        capture_output=True,
        text=True
    )

    if "nothing to commit" in commit.stderr.lower():
        print("⚠️ Aucun commit effectué (rien à valider). Abandon du push.")
        return

    # Branche main
    subprocess.run(["git", "branch", "-M", "main"], cwd=project_path)

    # Remove + add remote origin
    subprocess.run(["git", "remote", "remove", "origin"],
                   cwd=project_path, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin",
                   git_url], cwd=project_path)

    # Push
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_path)
    print("🚀 Projet poussé sur GitHub avec succès.")






if __name__ == "__main__":
    user_prompt = input("Quelle est ta demande ?\n> ")

    crew = create_crew(user_prompt)
    result = crew.kickoff()

    print("\n🧾 Résultat final :\n", result)

    import re


    def slugify_project_name(prompt):
        # Convertir la phrase en slug court et valide
        project_name = re.sub(r'\W+', '-', prompt.lower()).strip('-')
        # Limite GitHub : max 100 caractères (on coupe à 80 pour plus de sécurité)
        return project_name[:20]
    
    # 🔧 Récupère le nom du projet (ou génère un nom propre)
    import re
    project_name = slugify_project_name(user_prompt)
    project_path = f"./projects/{project_name}"

    # Crée le dossier si besoin
    os.makedirs(project_path, exist_ok=True)

    # ⚠️ Ici, tu dois écrire le `result` ou les fichiers générés dans ce dossier
    # Tu peux adapter cela à ton système si CrewAI écrit déjà les fichiers dans ce chemin

    # 🟢 Init git + push GitHub
    init_git_and_push(project_path, project_name)
