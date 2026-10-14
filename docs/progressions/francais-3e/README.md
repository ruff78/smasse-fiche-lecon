# Progression décloisonnée de français — classe de 3ème (Niger)

| Fichier | Rôle |
|---|---|
| `progression-decloisonnee-3e.pdf` | **Document livrable** (38 pages, A4 portrait/paysage) : progression annuelle complète, 2 semestres, 8 séquences, fiches de leçon développées, annexes |
| `progression-decloisonnee-3e.md` | Source éditable du document (Markdown pédagogique) : à corriger en UP puis à régénérer |

## Contenu du PDF

1. Cadre : programme officiel, profil de sortie, objectifs généraux de 3ème
2. Doctrine du décloisonnement (activités internes au français : EO, LC, LM, GR, CJ, OR, VX, PE)
3. Architecture annuelle : 8 séquences, progression semaine par semaine (S1 → S32), calendrier des évaluations
4. Les 8 fiches-séquences séance par séance (12 séances chacune) + remédiation différenciée
5. Matrice de décloisonnement et progressions spiralées (grammaire, conjugaison, orthographe, vocabulaire)
6. Sept fiches de leçon rédigées au format « visite de classe »
7. Outils de pilotage : cahier des charges documentaire, remédiation, indicateurs
8. Annexes : corpus et œuvres, trames vierges à photocopier, fiche d'erreurs, glossaire, sources, validation UP

> Points à recaler avant visa : emploi du temps officiel de l'année, calendrier scolaire
> et barèmes d'examen en vigueur (voir les encadrés « À valider sur pièces officielles » du document).

## Régénérer le PDF après modification de la source

```bash
python3 -m venv .venv-pdf
.venv-pdf/bin/pip install -r tools/pdf_export/requirements.txt
.venv-pdf/bin/python tools/pdf_export/render.py \
  docs/progressions/francais-3e/progression-decloisonnee-3e.md \
  docs/progressions/francais-3e/progression-decloisonnee-3e.pdf \
  --title "PROGRESSION DÉCLOISONNÉE DE FRANÇAIS — CLASSE DE 3ème" \
  --subtitle "Programme officiel des enseignements secondaires du Niger — 1er cycle" \
  --kicker "Année scolaire 2026-2027" \
  --header "Progression décloisonnée de français — 3ème (Niger)"
```

Le moteur (`tools/pdf_export/render.py`, ReportLab) gère : page de titre, sommaire
automatique avec numéros de page (construction en plusieurs passes), tableaux larges
en A4 paysage (`::: landscape` … `:::`), encadrés institutionnels (`> [!TITRE]`),
sauts de page conditionnels (`<!--pagebreak-->`) et signets PDF.
