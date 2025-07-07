from crewai import Crew, Task
from agents.analyst import create_analyst
from agents.dev import create_developer
from agents.tester import create_tester
from agents.optimizer import create_optimizer


def create_crew(prompt_user: str):
    analyst = create_analyst()
    dev = create_developer()
    tester = create_tester()
    optimizer = create_optimizer()

    task1 = Task(
        agent=analyst,
        description=f"Analyser la demande suivante : {prompt_user} et décrire les étapes nécessaires.",
        expected_output="Une spécification technique détaillée du script à développer.",
    )

    task2 = Task(
        agent=dev,
        description="Développer un script Python basé sur la spécification fournie.",
        expected_output="Code Python complet pour réaliser la tâche demandée.",
    )

    task3 = Task(
        agent=tester,
        description="Tester le script produit et rapporter les erreurs.",
        expected_output="Rapport de tests automatisés + feedback",
    )

    task4 = Task(
        agent=optimizer,
        description="Améliorer le script, ajouter sécurité et optimisation.",
        expected_output="Script finalisé, performant et sécurisé.",
    )

    task5 = Task(
        agent=tester,
        description="Re tester le script produit et rapporter les erreurs.",
        expected_output="Rapport de tests automatisés + feedback",
    )

    return Crew(
        agents=[analyst, dev, tester, optimizer],
        tasks=[task1, task2, task3, task4, task5],
        verbose=True,
    )
