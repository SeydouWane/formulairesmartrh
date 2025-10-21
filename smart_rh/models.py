from . import db
from datetime import datetime

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    date_soumission = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Partie 1 : Informations générales ---
    nom_prenom = db.Column(db.String(100), nullable=True)
    nom_entreprise = db.Column(db.String(100), nullable=True)
    fonction = db.Column(db.String(100), nullable=True)
    taille_structure = db.Column(db.String(50), nullable=True)
    type_recrutement = db.Column(db.String(50), nullable=True)

    # --- Partie 2 : Processus actuel ---
    # Ces champs contiennent des listes de choix multiples qui peuvent être longs
    publie_comment = db.Column(db.Text, nullable=True) # CHANGÉ : De String à Text (ou String(500))
    publie_comment_autre = db.Column(db.Text, nullable=True)
    
    recu_candidature_comment = db.Column(db.Text, nullable=True) # CHANGÉ
    recu_candidature_comment_autre = db.Column(db.Text, nullable=True)

    candidatures_moyenne = db.Column(db.String(50), nullable=True)

    tri_cv_comment = db.Column(db.Text, nullable=True)
    difficulte_tri = db.Column(db.String(3), nullable=True) # Oui/Non
    difficulte_tri_si_oui = db.Column(db.Text, nullable=True)

    # --- Partie 3 : Problèmes et frustrations ---
    plus_grandes_difficultes = db.Column(db.Text, nullable=True) # CHANGÉ
    difficultes_autre = db.Column(db.Text, nullable=True)
    
    utilise_plateforme_rh = db.Column(db.String(3), nullable=True) # Oui/Non
    plateforme_si_oui = db.Column(db.Text, nullable=True)

    priorites_amelioration = db.Column(db.Text, nullable=True) # CHANGÉ
    priorites_amelioration_autre = db.Column(db.Text, nullable=True)

    # --- Partie 4 : Perception de la solution Smart RH ---
    interesse_smart_rh = db.Column(db.String(10), nullable=True) # "Peut-être" passe (10 chars suffisent)
    avantages_utiles = db.Column(db.Text, nullable=True) # CHANGÉ : Liste de choix potentiellement longue
    avantages_utiles_autre = db.Column(db.Text, nullable=True)
    # LE CHAMP QUI CAUSE LE PROBLÈME :
    teste_beta = db.Column(db.String(50), nullable=True) # CORRIGÉ: 20 -> 50 pour "Peut-être, selon les conditions" (27 chars)
    raison_adoption = db.Column(db.Text, nullable=True)

    # --- Partie 5 : Vos attentes et suggestions ---
    plateforme_rh_ideale = db.Column(db.Text, nullable=True)
    attentes_principales = db.Column(db.Text, nullable=True)
    suggestions = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Submission {self.nom_entreprise} - {self.date_soumission.strftime('%Y-%m-%d')}>"