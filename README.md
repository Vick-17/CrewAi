# CrewAI

Cette application permet de générer un projet Python à partir d'une demande utilisateur en utilisant un ensemble d'agents d'IA. Elle crée un dépôt GitHub et y pousse automatiquement le résultat.

## Utilisation

1. Renseigner les variables `GITHUB_TOKEN` et `GITHUB_USERNAME` dans un fichier `.env`.
2. Lancer le script `python main.py` puis saisir la demande à traiter.
3. Le projet généré est placé dans le dossier `projects/` et poussé vers GitHub.

## Dépendances

- Python 3.10+
- [crewai](https://pypi.org/project/crewai/)
- `python-dotenv`
- `requests`

