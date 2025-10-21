/**
 * Gère l'affichage/masquage d'un champ de saisie 'Autre'
 * basé sur l'état d'une checkbox.
 * @param {string} prefix - Le préfixe utilisé dans les IDs (ex: 'publie', 'recu')
 */
function toggleAutreField(prefix) {
    // La checkbox qui déclenche l'événement
    const checkbox = document.getElementById(`checkbox_${prefix}_autre`);
    // Le conteneur du champ de saisie 'Autre'
    const fieldContainer = document.getElementById(`field_${prefix}_autre`);
    // Le champ de saisie lui-même
    const inputField = fieldContainer ? fieldContainer.querySelector('input, textarea') : null;

    if (!checkbox || !fieldContainer) {
        console.error(`Éléments pour ${prefix} non trouvés.`);
        return;
    }
    
    if (checkbox.checked) {
        fieldContainer.classList.remove('hidden');
        // Rendre le champ de saisie visible
        if (inputField) {
            inputField.setAttribute('name', `${prefix}_autre`);
        }
    } else {
        fieldContainer.classList.add('hidden');
        // Masquer le champ de saisie (le retirer des données POST si possible)
        if (inputField) {
            inputField.removeAttribute('name');
            inputField.value = ''; // Optionnel: effacer la valeur
        }
    }
}

// Initialisation au chargement de la page pour tous les champs 'Autre'
document.addEventListener('DOMContentLoaded', () => {
    // Liste de tous les préfixes que vous utilisez pour les champs 'Autre'
    const prefixes = [
        'publie_comment', 
        'recu_candidature_comment', 
        'plus_grandes_difficultes', 
        'priorites_amelioration',
        'avantages_utiles'
    ];
    
    prefixes.forEach(prefix => {
        // Le prefix pour les IDs est sans le suffixe '_comment'
        const id_prefix = prefix.replace('_comment', ''); 
        if (document.getElementById(`checkbox_${id_prefix}_autre`)) {
            // Assurez-vous que l'état initial est correct lors du chargement
            toggleAutreField(id_prefix);
        }
    });

    // Gestion du champ 'Si oui' pour "Rencontrez-vous des difficultés lors du tri..."
    const triOui = document.getElementById('difficulte_tri_oui');
    const triNon = document.getElementById('difficulte_tri_non');
    const triSiOuiField = document.getElementById('field_difficulte_tri_si_oui');

    function toggleTriSiOui() {
        if (triOui && triSiOuiField) {
            if (triOui.checked) {
                triSiOuiField.classList.remove('hidden');
            } else {
                triSiOuiField.classList.add('hidden');
                triSiOuiField.querySelector('textarea').value = ''; 
            }
        }
    }
    if (triOui) triOui.addEventListener('change', toggleTriSiOui);
    if (triNon) triNon.addEventListener('change', toggleTriSiOui);
    if (triOui || triNon) toggleTriSiOui(); // Vérifie l'état initial
});