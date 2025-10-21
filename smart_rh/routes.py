from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .models import Submission # Assurez-vous que votre modèle Submission est importé
from sqlalchemy.sql import func
# Note : Les imports de flask_login sont inutiles si vous utilisez la session manuelle
# from flask_login import login_required, current_user 

main = Blueprint('main', __name__)


# --- Décorateur de Protection Manuel (basé sur la session Flask) ---
def login_required(f):
    """Vérifie si l'utilisateur est connecté pour les pages admin via la session Flask."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si la clé 'logged_in' est définie et est True
        if session.get('logged_in') != True:
            flash('Accès restreint. Veuillez vous connecter.', 'error')
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Route Formulaire Client ---
@main.route('/', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        try:
            # Fonction utilitaire pour gérer les checkbox et le champ "Autre"
            def get_checkbox_data(name, has_other=True):
                data = request.form.getlist(name)
                other = request.form.get(f'{name}_autre') if has_other else None
                
                # Ajouter le champ 'autre' s'il est rempli
                if other:
                    data.append(f"Autre: {other}")
                
                return ", ".join(data), other

            # Traitement des données des checkboxes
            publie_comment, publie_comment_autre = get_checkbox_data('publie_comment')
            recu_candidature_comment, recu_candidature_comment_autre = get_checkbox_data('recu_candidature_comment')
            plus_grandes_difficultes, difficultes_autre = get_checkbox_data('plus_grandes_difficultes')
            priorites_amelioration, priorites_amelioration_autre = get_checkbox_data('priorites_amelioration')
            avantages_utiles, avantages_utiles_autre = get_checkbox_data('avantages_utiles')

            # Création de l'objet Submission
            new_submission = Submission(
                # Partie 1
                nom_prenom=request.form.get('nom_prenom'),
                nom_entreprise=request.form.get('nom_entreprise'),
                fonction=request.form.get('fonction'),
                taille_structure=request.form.get('taille_structure'),
                type_recrutement=request.form.get('type_recrutement'),
                
                # Partie 2
                publie_comment=publie_comment,
                publie_comment_autre=publie_comment_autre,
                recu_candidature_comment=recu_candidature_comment,
                recu_candidature_comment_autre=recu_candidature_comment_autre,
                candidatures_moyenne=request.form.get('candidatures_moyenne'),
                tri_cv_comment=request.form.get('tri_cv_comment'),
                difficulte_tri=request.form.get('difficulte_tri'),
                difficulte_tri_si_oui=request.form.get('difficulte_tri_si_oui'),
                
                # Partie 3
                plus_grandes_difficultes=plus_grandes_difficultes,
                difficultes_autre=difficultes_autre,
                utilise_plateforme_rh=request.form.get('utilise_plateforme_rh'),
                plateforme_si_oui=request.form.get('plateforme_si_oui'),
                priorites_amelioration=priorites_amelioration,
                priorites_amelioration_autre=priorites_amelioration_autre,
                
                # Partie 4
                interesse_smart_rh=request.form.get('interesse_smart_rh'),
                avantages_utiles=avantages_utiles,
                avantages_utiles_autre=avantages_utiles_autre,
                teste_beta=request.form.get('teste_beta'),
                raison_adoption=request.form.get('raison_adoption'),

                # Partie 5
                plateforme_rh_ideale=request.form.get('plateforme_rh_ideale'),
                attentes_principales=request.form.get('attentes_principales'),
                suggestions=request.form.get('suggestions'),
            )

            db.session.add(new_submission)
            db.session.commit()
            flash('Merci pour votre participation !', 'success')
            return redirect(url_for('main.remerciement'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Une erreur est survenue lors de la soumission : {e}", 'error')
            print(f"Erreur de soumission : {e}")
            
    return render_template('formulaire.html')

@main.route('/remerciement')
def remerciement():
    return render_template('remerciement.html')


# --- Espace Admin (Authentification et Routes Protégées) ---

# NOTE : Pour un projet réel, cette variable devrait être dans un fichier .env !
ADMIN_PASSWORD = "SMART_RH_ADMIN_2024"

@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            # --- CORRECTION MAJEURE : Enregistrement de la connexion dans la session ---
            session['logged_in'] = True 
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.admin_dashboard'))
        flash('Mot de passe incorrect', 'danger')
    return render_template('admin_login.html')

@main.route('/admin/dashboard')
@login_required # <--- Ajout du décorateur de protection
def admin_dashboard():
    submissions = Submission.query.order_by(Submission.date_soumission.desc()).all()
    return render_template('admin_dashboard.html', submissions=submissions)

@main.route('/admin/summary')
@login_required # <--- Ajout du décorateur de protection
def admin_summary():
    # Analyse de données : agrégation des réponses
    
    # Ex: Compter la répartition de la taille de structure
    taille_stats = db.session.query(
        Submission.taille_structure, 
        func.count(Submission.taille_structure)
    ).group_by(Submission.taille_structure).all()
    
    # Ex: Compter la répartition des difficultés de tri (Oui/Non)
    difficulte_tri_stats = db.session.query(
        Submission.difficulte_tri, 
        func.count(Submission.difficulte_tri)
    ).group_by(Submission.difficulte_tri).all()
    
    # Total des soumissions pour les pourcentages
    total_submissions = Submission.query.count()

    # NOTE : L'analyse des champs de type Text (checkboxes multiples) est plus complexe 
    # et nécessiterait des requêtes spécifiques ou un traitement Python après la récupération.
    
    return render_template('admin_resume.html', 
                           taille_stats=taille_stats,
                           difficulte_tri_stats=difficulte_tri_stats,
                           total_submissions=total_submissions)

@main.route('/admin/submission/<int:submission_id>')
@login_required # <--- Ajout du décorateur de protection
def admin_submission_detail(submission_id):
    """Affiche les détails d'une soumission spécifique."""
    # Utilise get_or_404 pour gérer le cas où l'ID n'existe pas
    submission = Submission.query.get_or_404(submission_id)
    return render_template('admin_detail.html', submission=submission)