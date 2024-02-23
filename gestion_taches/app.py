from flask import Flask, render_template ,request, redirect, url_for,flash,send_file,jsonify
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    return render_template('index.html')

#afficher les taches dont le statut est en cours
@app.route("/tacheencours")
def tacheencour():
   with open('taches.json', 'r') as file:
     taches = json.load(file)
     taches_en_cours = [tache for tache in taches if tache.get('statut') == 'en cours'or tache.get('statut') == 'non assignee']
     return render_template('tacheencours.html', taches=taches_en_cours)


def get_all_employees():
    with open('employes.json', 'r') as employes_file:
        employes = json.load(employes_file)
    return employes

#@app.route("/listeemployes")
#def liste_employes():
    # Load tasks from employes.json
#    with open('employes.json', 'r') as file:
#        employes = json.load(file)
    
    # Render the template with the employes data
#    return render_template('gestionemployes.html', employes=employes)



@app.route("/edit/<titre>", methods=['GET', 'POST'])
def edit_task(titre):
    if request.method == 'POST':
        with open('taches.json', 'r') as file:
            taches = json.load(file)
        
        for tache in taches:
            if tache['titre'] == titre:
                tache['titre'] = request.form.get('titre')
                tache['description'] = request.form.get('description')
                tache['statut'] = request.form.get('statut')
                nouveau_nom_employe = request.form.get('employe_assigne')
                
                # Rechercher l'employé dans la liste des employés
                employe_details = None
                with open('employes.json', 'r') as employes_file:
                    employes = json.load(employes_file)
                    for employe in employes:
                        if employe['nom'] == nouveau_nom_employe:
                            employe_details = employe
                            break
                
                # Mettre à jour l'employé assigné dans la tâche
                tache['employe_assigne'] = employe_details
                
                break
        
        with open('taches.json', 'w') as file:
            json.dump(taches, file, indent=4)
        
        # Rediriger vers la page affichant toutes les tâches
        return redirect(url_for('touteslestaches'))
    else:
        # Si la méthode de requête est GET, renvoyer le template edit_task.html avec les détails de la tâche
        with open('taches.json', 'r') as file:
            taches = json.load(file)
        
        for tache in taches:
            if tache['titre'] == titre:
                employes = get_all_employees()  # Utilisation de la fonction pour obtenir la liste des employés
                return render_template('edit_task.html', tache=tache, employes=employes)
        
        # Si la tâche avec le titre spécifié n'est pas trouvée, rediriger vers la page affichant toutes les tâches
        flash('La tâche spécifiée n\'a pas été trouvée.', 'error')
        return redirect(url_for('touteslestaches'))








@app.route("/delete/<titre>", methods=['POST'])
def delete_task(titre):
    # Charger les tâches depuis le fichier taches.json
    with open('taches.json', 'r') as file:
        taches = json.load(file)
    
    # Filtrer les tâches pour supprimer celle avec le titre donné
    taches = [tache for tache in taches if tache['titre'] != titre]

    # Réécrire la liste filtrée dans le fichier taches.json
    with open('taches.json', 'w') as file:
        json.dump(taches, file, indent=4)
    
    # Rediriger vers la page des tâches en cours
    return redirect(url_for('tacheencour'))





@app.route("/touteslestaches")
def touteslestaches():
    # Load tasks from taches.json
    with open('taches.json', 'r') as file:
        taches = json.load(file)
    
    # Render the template with the tasks data
    return render_template('touteslestaches.html', taches=taches)


@app.route("/export-json")
def export_json():
    # Logic to export the JSON file
    # For example, you can send the file directly using Flask's send_file function
    return send_file('taches.json', as_attachment=True)





# Charger les données des employés depuis employes.json
with open('employes.json', 'r') as file:
    employes = json.load(file)

# Route pour afficher le formulaire de création
@app.route("/ajouttache", methods=['GET'])
def create_task_form():
    return render_template('ajouttache.html', employes=employes)

@app.route("/ajouttache", methods=['POST'])
def create_task():
    # Récupérer les détails de la tâche depuis le formulaire
    titre = request.form['titre']
    description = request.form['description']
    statut = request.form['statut']
    employe_nom = request.form['employe_assigne']

    # Rechercher l'employé dans la liste des employés
    employe_details = None
    for employe in employes:
        if employe['nom'] == employe_nom:
            employe_details = employe
            break

    # Créer un dictionnaire pour la nouvelle tâche
    new_task = {
        'titre': titre,
        'description': description,
        'statut': statut,
        'employe_assigne': {
            'nom': employe_details['nom'],
            'prenom': employe_details['prenom'],
            'email': employe_details['email'],
            'icone': employe_details['icone']
        }
    }

    # Ajouter la nouvelle tâche à la liste des tâches
    with open('taches.json', 'r+') as file:
        tasks = json.load(file)
        tasks.append(new_task)
        file.seek(0)
        json.dump(tasks, file, indent=4)

    # Afficher un message de confirmation
    flash('Tâche créée avec succès!', 'success')

    # Rediriger vers la page de toutes les tâches
    return render_template('ajouttache.html', employe=employe)



def get_all_employees():
    with open('employes.json', 'r') as employes_file:
        employes = json.load(employes_file)
    return employes





# Fonction pour éditer un employé
@app.route("/edit_employe/<nom>", methods=['GET', 'POST'])
def edit_employe(nom):
    if request.method == 'POST':
        new_nom = request.form['nom']
        new_prenom = request.form['prenom']
        new_email = request.form['email']
        new_icone = request.form['icone']

        # Chargez les employés depuis le fichier JSON
        with open('employes.json', 'r') as file:
            employes = json.load(file)

        # Trouvez l'employé à éditer
        for employe in employes:
            if employe['nom'] == nom:
                employe['nom'] = new_nom
                employe['prenom'] = new_prenom
                employe['email'] = new_email
                employe['icone'] = new_icone
                break

        # Écrivez les données mises à jour dans le fichier JSON
        with open('employes.json', 'w') as file:
            json.dump(employes, file, indent=4)

        # Redirigez vers la page de liste des employés
        return redirect(url_for('liste_employes'))
    else:
        # Si la méthode de requête est GET, renvoyez le template d'édition avec les détails de l'employé
        with open('employes.json', 'r') as file:
            employes = json.load(file)

        for employe in employes:
            if employe['nom'] == nom:
               
                return render_template('edit_employe.html', employe=employe)
        
        # Si l'employé avec l'ID spécifié n'est pas trouvé, redirigez vers la page de liste des employés
        flash('L\'employé spécifié n\'a pas été trouvé.', 'error')
        return redirect(url_for('liste_employes'))


@app.route("/listeemployes")
def liste_employes():
    # Charger les employés depuis le fichier employes.json
    with open('employes.json', 'r') as file:
        employes = json.load(file)
    
    # Charger les tâches depuis le fichier taches.json
    with open('taches.json', 'r') as file:
        taches = json.load(file)

    # Calculer le nombre de tâches en cours pour chaque employé
    for employe in employes:
        employe['taches_en_cours'] = sum(1 for tache in taches if isinstance(tache['employe_assigne'], dict) and tache['employe_assigne']['nom'] == employe['nom'] and tache['statut'] == 'en cours')

    # Calculer le nombre total de tâches assignées à chaque employé
    for employe in employes:
        employe['taches_total'] = sum(1 for tache in taches if isinstance(tache['employe_assigne'],dict) and tache['employe_assigne']['nom'] == employe['nom'])
    
    # Rendre le modèle HTML avec les données des employés
    return render_template('gestionemployes.html', employes=employes)


# Fonction pour supprimer un employé
@app.route("/delete_employe/<nom>")
def delete_employe(nom):
    # Chargez les employés depuis le fichier JSON
    with open('employes.json', 'r') as file:
        employes = json.load(file)

    # Trouvez l'employé à supprimer
    for employe in employes:
        if employe['nom'] == nom:
            employes.remove(employe)
            flash('Cet employé a été supprimé par succés!', 'success')
            break

    # Écrivez les données mises à jour dans le fichier JSON
    with open('employes.json', 'w') as file:
        json.dump(employes, file, indent=4)

    # Redirigez vers la page de liste des employés
    return render_template('gestionemployes.html', employes=employes)


def save_employees(employees):
    with open('employes.json', 'w') as file:
        json.dump(employees, file, indent=4)


@app.route("/ajoutemploye", methods=['GET', 'POST'])
def add_employe():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        icone = request.form['icone']

        new_employee = {
            'nom': nom,
            'prenom': prenom,
            'email': email,
            'icone': icone
        }

        employees = get_all_employees()

        # Vérifier si l'employé existe déjà
        for employee in employees:
            if employee['email'] == email:
                flash('Cet employé existe déjà!', 'error')
                return render_template('ajoutemploye.html', employes=employes)

        # Si l'employé n'existe pas déjà, l'ajouter à la liste des employés
        employees.append(new_employee)
        save_employees(employees)

        flash('Nouvel employé créé avec succès!', 'success')
        
        # Mettre à jour la liste des employés avant de rediriger
        return redirect(url_for('liste_employes'))
    else:
        return render_template('ajoutemploye.html', employes=employes)



@app.route("/export-employees")
def export_employees():
    with open('employes.json', 'r') as file:
        employes = json.load(file)
    return jsonify(employes)

@app.route("/export-taches-json")
def export_tasks_json():
    # Charger les tâches depuis le fichier taches.json
    with open('taches.json', 'r') as file:
        tasks = json.load(file)
    
    # Envoyer les tâches en tant que fichier JSON
    return send_file('taches.json', as_attachment=True)

app.run()
