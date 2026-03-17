
import subprocess
import os
import shutil
import datetime
from collections import Counter

print("\nRUN Risk Scanner\n")

repo_url = input("Entrer l'URL du repository Git : ")

repo_folder = "temp_repo"

if os.path.exists(repo_folder):
    shutil.rmtree(repo_folder)

print("\nClonage du repository...\n")

subprocess.run(["git", "clone", repo_url, repo_folder], check=True)

os.chdir(repo_folder)

def git(cmd):
    return subprocess.check_output(cmd).decode("utf-8").strip()

authors = git(["git","log","--format=%an"]).split("\n")
author_counts = Counter(authors)

commit_count = int(git(["git","rev-list","--count","HEAD"]))

authors_count = len(author_counts)

top_author, top_commits = author_counts.most_common(1)[0]

ownership = round((top_commits/commit_count)*100)

bus_factor = len([a for a in author_counts.values() if a > commit_count*0.05])

files_modified = git(["git","log","--name-only","--pretty=format:"]).split("\n")

file_counts = Counter(files_modified)

hotspot_file, hotspot_changes = file_counts.most_common(1)[0]

churn = len(files_modified)

first_commit = git(["git","log","--reverse","--format=%cd","--date=short"]).split("\n")[0]

first_commit_date = datetime.datetime.strptime(first_commit,"%Y-%m-%d")

today = datetime.datetime.today()

project_age = round((today-first_commit_date).days/365)

run_complexity = len(file_counts)

critical_files = len([f for f,c in file_counts.items() if c > 30])

developer_count = authors_count

knowledge_concentration = ownership

# SCORE

score = 100

if bus_factor <= 2:
    score -= 20

if knowledge_concentration > 60:
    score -= 15

if churn > 1000:
    score -= 10

if project_age > 10:
    score -= 10

if developer_count <= 3:
    score -= 10

print("\n==============================")
print("RUN Risk Score :",score)
print("==============================\n")

print("Analyse structurelle :\n")

print("Developers actifs :",developer_count)
print("Bus factor :",bus_factor)
print("Knowledge concentration :",knowledge_concentration,"%")
print("Total commits :",commit_count)
print("Code churn :",churn)
print("Age du projet :",project_age,"ans")
print("Hotspot fichier :",hotspot_file,"→",hotspot_changes,"modifications")
print("Complexité RUN :",run_complexity)
print("Fichiers critiques :",critical_files)

print("\nDiagnostic :\n")

if bus_factor <= 2:
    print("- Forte dépendance à quelques développeurs")

if knowledge_concentration > 60:
    print("- Concentration du savoir sur un nombre limité de personnes")

if project_age > 10:
    print("- Modules anciens pouvant augmenter le risque RUN")

if churn > 1000:
    print("- Activité de modification élevée")

print("\nRecommandations :\n")

print("- Renforcer la documentation des modules critiques")
print("- Mettre en place du binômage sur les zones sensibles")
print("- Réduire les single points of failure humains")
print("- Cartographier les flux et dépendances")
print("- Mettre en place un transfert de connaissance")
print("- Surveiller les hotspots du code")
print("- Stabiliser les modules les plus modifiés")
print("- Documenter les scripts et pipelines critiques")
print("- Réduire la dépendance à un seul expert")
print("- Maintenir un historique clair des changements")
print("- Identifier les modules legacy")
print("- Améliorer la visibilité globale du système")
