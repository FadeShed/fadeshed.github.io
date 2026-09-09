/* French labels for the browser-builder page, not a translation of the engine. */
window.fsBuilderText = value => {
  const s=String(value);const exact={
    'Connection data cleared.':'Données de connexion effacées.',
    'Ready.':'Prêt.','Build':'Construire','Pull':'Récupérer','Push':'Envoyer',
    'Building…':'Construction…','Choose a .zip file first.':'Choisissez d’abord un fichier .zip.',
    'Build complete — downloading public.zip':'Construction terminée — téléchargement de public.zip',
    'Fill in the GitLab instance URL, project ID and token first.':'Renseignez d’abord l’URL GitLab, l’identifiant du projet et le jeton.',
    'GitLab instance URL must be https:// (plain http:// is only allowed for localhost/127.0.0.1) — the token would otherwise travel in clear text.':'L’URL GitLab doit utiliser https:// (http:// n’est autorisé que pour localhost/127.0.0.1), sinon le jeton circulerait en clair.',
    'Pulled. Ready to build.':'Récupération terminée. Prêt à construire.',
    'Build complete. Ready to push.':'Construction terminée. Prêt à envoyer.',
    'Loading Pyodide…':'Chargement de Pyodide…','Copy':'Copier','Copied!':'Copié !'};
  if(Object.hasOwn(exact,s))return exact[s];
  return s.replace(/^Failed to load Pyodide: /,'Échec du chargement de Pyodide : ')
    .replace(/^Build failed: /,'Échec de la construction : ').replace(/^Pull failed: /,'Échec de la récupération : ')
    .replace(/^Push failed: /,'Échec de l’envoi : ').replace(/^Pulling (.+) from (.+)…$/,'Récupération de $1 depuis $2…')
    .replace(/^Pushing to (.+)…$/,'Envoi vers $1…').replace('the zip exceeds the ','le ZIP dépasse la limite de ')
    .replace(' MiB compressed-size limit.',' Mio compressés.');
};
