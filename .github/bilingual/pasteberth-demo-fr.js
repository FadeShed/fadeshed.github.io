/* French presentation layer for this in-memory demo only.
 * Artifact bytes, authored comments and the copied product frontend are unchanged.
 */
(()=>{'use strict';
const exact={
'Pasteberth — local website demo':'Pasteberth — démonstration locale',
'connecting…':'connexion…','online':'en ligne','offline':'hors ligne','Log out':'Se déconnecter','All':'Tout','Projects':'Projets','Overview':'Vue d’ensemble',
'Copy link':'Copier la référence','Copy links':'Copier les références','Copy Image':'Copier l’image','Copy image':'Copier l’image','Copy Text':'Copier le texte','Copy text':'Copier le texte','Copy HTML':'Copier le HTML','Copy raw HTML':'Copier le HTML brut','Copy Bin':'Copier les données',
'Download':'Télécharger','Clear':'Vider','Delete':'Supprimer','Close':'Fermer','Replace existing file?':'Remplacer le fichier existant ?',
'A Pasteberth file already uses this name in zone':'Un fichier Pasteberth utilise déjà ce nom dans la zone','Cancel':'Annuler','Replace':'Remplacer',
'Add files':'Ajouter des fichiers','Choose destination':'Choisir la destination','Move':'Déplacer','Copy':'Copier','Comment':'Commenter','Edit comment':'Modifier le commentaire','Save':'Enregistrer','Zoom':'Zoom','Preview':'Aperçu',
'Image index':'Index des images','Content index':'Index du contenu','Selected files':'Fichiers sélectionnés','Clear selection':'Effacer la sélection','Delete selected':'Supprimer la sélection',
'Group options':'Options de groupes','Group display options':'Affichage des groupes','Hide empty groups':'Masquer les groupes vides','Show zone counts':'Afficher le nombre de zones','Layout':'Disposition','Area':'Grille','Tab':'Onglets','Show zone column':'Afficher la colonne des zones',
'Zones':'Zones','Open zones':'Zones ouvertes','NEW':'NOUVEAU','Text':'Texte','Bin':'Binaire',
'Link copied':'Référence copiée','Automatic copy failed - click Copy link':'Copie automatique refusée — cliquez sur Copier la référence','Automatic copy failed; click Copy link':'Copie automatique refusée — cliquez sur Copier la référence','Copy failed - try again':'Échec de la copie — réessayez','Copy failed; try again':'Échec de la copie — réessayez',
'Image copied':'Image copiée','Text copied':'Texte copié','Raw HTML copied':'HTML brut copié','Bin copied':'Données copiées','Clipboard cleared':'Presse-papiers vidé','Comment saved':'Commentaire enregistré','Clear the clipboard':'Vider le presse-papiers',
'The clipboard does not contain an image or text':'Le presse-papiers ne contient ni image ni texte',
'Could not copy the link — select it manually':'Impossible de copier la référence — sélectionnez-la manuellement',
'Could not copy the links — select them manually':'Impossible de copier les références — sélectionnez-les manuellement',
'Image copying is not supported by this browser':'Ce navigateur ne permet pas de copier les images',
'Binary copying is not supported by this browser':'Ce navigateur ne permet pas de copier les données binaires',
'Could not copy the image to the clipboard':'Impossible de copier l’image dans le presse-papiers',
'Could not copy the text to the clipboard':'Impossible de copier le texte dans le presse-papiers',
'Could not copy the binary to the clipboard':'Impossible de copier les données dans le presse-papiers',
'Could not clear the clipboard — use the system clipboard':'Impossible de vider le presse-papiers — utilisez celui du système',
'Choose a destination zone first':'Choisissez d’abord une zone de destination','Choose a different destination zone':'Choisissez une autre zone de destination',
'This zone is busy; try again shortly':'Cette zone est occupée ; réessayez dans un instant','One of these zones is busy; try again shortly':'Une des zones est occupée ; réessayez dans un instant','This zone is busy':'Cette zone est occupée','Zone busy; another operation is using it':'Zone occupée par une autre opération',
'ZIP downloads are disabled for this zone':'Les téléchargements ZIP sont désactivés dans cette zone',
'Maximum upload: unavailable':'Taille maximale d’envoi : indisponible','Retention: unlimited':'Rétention : sans limite',
'Active paste target: Ctrl/Command+V to paste or drag a file here':'Zone active : Ctrl/Commande+V pour coller, ou déposez un fichier ici',
'Select this zone to make it the paste target, or drag a file here':'Sélectionnez cette zone pour y coller, ou déposez un fichier ici',
'No files were uploaded':'Aucun fichier n’a été envoyé','The upload service is busy':'Le service d’envoi est occupé','Content is too large for this server':'Le contenu dépasse la taille autorisée','Not enough disk space for this upload':'Espace disque insuffisant pour cet envoi',
'The dragged selection is empty':'La sélection déplacée est vide','The drop does not contain a file':'Le dépôt ne contient pas de fichier','Could not load the text preview':'Impossible de charger l’aperçu du texte','Copy raw HTML to the clipboard':'Copier le HTML brut dans le presse-papiers',
'Not in this local demo':'Absent de cette démonstration','Invalid demo transfer':'Transfert de démonstration invalide','Unknown file':'Fichier inconnu','Unknown zone':'Zone inconnue','The file is empty':'Le fichier est vide','Unsupported name':'Nom non pris en charge','Existing demo file':'Fichier déjà présent','A filename already exists in the destination':'Ce nom de fichier existe déjà dans la destination','Local demo limit: 8 MiB per file':'Limite de la démo : 8 Mio par fichier','Local demo limit: 32 MiB of files in total':'Limite de la démo : 32 Mio de fichiers au total','This action is outside the local demo':'Cette action dépasse le cadre de la démonstration','Unsupported operation in this local demo':'Opération indisponible dans cette démonstration','Unable to create demo ZIP':'Impossible de créer le ZIP de démonstration'};
function tr(v){if(Object.hasOwn(exact,v))return exact[v];return v
 .replace(/^Download (\d+) files as ZIP$/,'Télécharger $1 fichiers en ZIP').replace(/^Download (.+)$/,'Télécharger $1').replace(/^Link copied: /,'Référence copiée : ')
 .replace(/^(\d+) links copied$/,'$1 références copiées').replace(/^Preparing ZIP with (\d+) files$/,'Préparation d’un ZIP de $1 fichiers')
 .replace(/^(\d+) files selected$/,'$1 fichiers sélectionnés').replace(/^(\d+) files deleted$/,'$1 fichiers supprimés')
 .replace(/^(\d+) files deleted, (\d+) failed$/,'$1 fichiers supprimés, $2 échecs')
 .replace(/^Destination for (\d+) selected files$/,'Destination de $1 fichiers sélectionnés')
 .replace(/^Move (\d+) selected files$/,'Déplacer $1 fichiers sélectionnés').replace(/^Copy (\d+) selected files$/,'Copier $1 fichiers sélectionnés')
 .replace(/^Copy (\d+) links$/,'Copier $1 références').replace(/^Download (\d+) files as ZIP$/,'Télécharger $1 fichiers en ZIP')
 .replace(/^Delete (\d+) selected files$/,'Supprimer $1 fichiers sélectionnés')
 .replace(/^Maximum upload: /,'Taille maximale d’envoi : ').replace(/^Retention: (\d+) files$/,'Rétention : $1 fichiers')
 .replace(/^(\d+) files in (.+); show upload details$/,'$1 fichiers dans $2 ; afficher les limites')
 .replace(/^Select zone (.+)$/,'Sélectionner la zone $1').replace(/, new files available$/,', nouveaux fichiers disponibles')
 .replace(/^Add files to /,'Ajouter des fichiers dans ').replace(/^Active zone: /,'Zone active : ')
 .replace(/^Edit comment for /,'Modifier le commentaire de ').replace(/^Comment for /,'Commentaire de ')
 .replace(/^Delete (.+) from the disk$/,'Supprimer $1 du disque').replace(/^Open preview of /,'Ouvrir l’aperçu de ')
 .replace(/^Image uploaded /,'Image déposée ').replace(/^Content uploaded /,'Contenu déposé ')
 .replace(/^Image already present /,'Image déjà présente ').replace(/^Content already present /,'Contenu déjà présent ');
}
const css=document.createElement('style');css.textContent='.tab-zone-main:empty::before{content:"Sélectionnez une zone pour l’ouvrir"}';document.head.append(css);
const nativeConfirm=window.confirm.bind(window);
window.confirm=message=>nativeConfirm(tr(String(message))
 .replace(/^Delete (\d+) selected files from the disk\?$/,'Supprimer du disque les $1 fichiers sélectionnés ?')
 .replace(/^Delete (.+) from the disk\?$/,'Supprimer $1 du disque ?')
 .replace(/^(.+) retains at most (\d+) items\. (?:this upload|\d+ uploads) will remove (\d+) oldest managed items?\. Continue\?$/,'$1 conserve au plus $2 fichiers. Cet envoi supprimera les $3 plus anciens fichiers gérés. Continuer ?'));
function refresh(){
 document.querySelectorAll('.group-tab').forEach(e=>{if(!e.dataset.fsOriginalText)e.dataset.fsOriginalText=e.textContent});
 const walk=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const nodes=[];while(walk.nextNode())nodes.push(walk.currentNode);
 for(const t of nodes){const p=t.parentElement;if(!p||p.closest('script,style,pre,code,textarea,.fname,.comment-text,.selection-summary-name,.preview-text,[data-fs-lang]'))continue;
 const raw=t.nodeValue,k=raw.trim(),value=tr(k);if(value!==k)t.nodeValue=raw.replace(k,value)}
 for(const e of document.querySelectorAll('[aria-label],[title],[placeholder]')){if(e.closest('.fname,.comment-text'))continue;for(const a of ['aria-label','title','placeholder'])if(e.hasAttribute(a)){const s=e.getAttribute(a),v=tr(s);if(v!==s)e.setAttribute(a,v)}}
}
refresh();let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;queueMicrotask(()=>{queued=false;refresh()})}).observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','placeholder']});
})();
