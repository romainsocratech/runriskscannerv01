import subprocess
import datetime
from collections import Counter

repo_path = "."

def git(cmd):
    return subprocess.check_output(cmd, cwd=repo_path).decode("utf-8").strip()

# -----------------------
# Collecte des données
# -----------------------

authors = git(["git", "log", "--format=%an"]).split("\n")
author_counts = Counter(authors)

commit_count = int(git(["git", "rev-list", "--count", "HEAD"]))
authors_count = len(author_counts)

top_author, top_commits = author_counts.most_common(1)[0]

ownership = round((top_commits / commit_count) * 100)

bus_factor = len([a for a in author_counts.values() if a > commit_count * 0.1])

files_modified = git(["git", "log", "--name-only", "--pretty=format:"]).split("\n")
file_counts = Counter(files_modified)

hotspot_file, hotspot_changes = file_counts.most_common(1)[0]

churn = len(files_modified)

# âge du projet
first_commit = git(["git", "log", "--reverse", "--format=%cd", "--date=short"]).split("\n")[0]
first_commit_date = datetime.datetime.strptime(first_commit, "%Y-%m-%d")

today = datetime.datetime.today()
project_age_years = round((today - first_commit_date).days / 365)

# dernier commit
last_commit = git(["git", "log", "-1", "--format=%cd", "--date=short"])
last_commit_date = datetime.datetime.strptime(last_commit, "%Y-%m-%d")

last_commit_days = (today - last_commit_date).days

# fréquence commits
commit_frequency = round(commit_count / project_age_years) if project_age_years > 0 else commit_count

# complexité RUN approximative
run_complexity = len(file_counts)

# fichiers critiques
critical_files = len([f for f, c in file_counts.items() if c > 20])

# développeurs actifs
developer_count = authors_count

# knowledge concentration
knowledge_concentration = ownership

# -----------------------
# SCORE RUN
# -----------------------

score = 100

if bus_factor <= 2:
    score -= 20

if knowledge_concentration > 60:
    score -= 15

if churn > 500:
    score -= 10

if project_age_years > 10:
    score -= 10

if developer_count <= 3:
    score -= 10

if last_commit_days > 30:
    score -= 5

# -----------------------
# DIAGNOSTIC
# -----------------------

diagnostic = []
recommendations = []

if bus_factor <= 2:
    diagnostic.append("Dépendance humaine élevée (bus factor faible)")
    recommendations.append("Mettre en place un transfert de connaissance")

if knowledge_concentration > 60:
    diagnostic.append("Concentration du savoir sur un développeur")
    recommendations.append("Répartir les contributions sur plusieurs développeurs")

if churn > 500:
    diagnostic.append("Code churn important")
    recommendations.append("Stabiliser les modules les plus modifiés")

if developer_count <= 3:
    diagnostic.append("Équipe de maintenance réduite")
    recommendations.append("Renforcer l'équipe ou organiser du binômage")

if project_age_years > 10:
    diagnostic.append("Présence de modules legacy anciens")
    recommendations.append("Cartographier les dépendances critiques")

if hotspot_changes > 50:
    diagnostic.append("Hotspot critique détecté dans le code")
    recommendations.append("Surveiller et refactoriser les fichiers hotspots")

if commit_frequency < 10:
    diagnostic.append("Activité de développement faible")
    recommendations.append("Relancer la maintenance active du projet")

if critical_files > 10:
    diagnostic.append("Plusieurs fichiers critiques très modifiés")
    recommendations.append("Documenter les modules critiques")

if run_complexity > 200:
    diagnostic.append("Complexité RUN élevée")
    recommendations.append("Simplifier l'architecture ou modulariser")

if last_commit_days > 30:
    diagnostic.append("Projet peu actif récemment")
    recommendations.append("Revoir la gouvernance du projet")

# -----------------------
# RESULTAT
# -----------------------

print("\nRUN Risk Score :", score)
print("\nAnalyse structurelle :\n")

print("Developers actifs :", developer_count)
print("Bus factor :", bus_factor)
print("Knowledge concentration :", knowledge_concentration, "%")
print("Commits :", commit_count)
print("Code churn :", churn)
print("Age du projet :", project_age_years, "ans")
print("Dernier commit :", last_commit_days, "jours")
print("Hotspot :", hotspot_file, "→", hotspot_changes, "modifications")
print("Complexité RUN :", run_complexity)
print("Fichiers critiques :", critical_files)

print("\nDiagnostic :\n")

for d in diagnostic:
    print("-", d)

print("\nRecommandations :\n")

for r in recommendations:
    print("-", r)