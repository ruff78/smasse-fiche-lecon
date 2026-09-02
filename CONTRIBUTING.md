# Guide de Contribution

Merci de votre intérêt pour le projet SMASSE Fiche Leçon ! Ce document fournit les directives pour contribuer au projet.

## Code de Conduite

Tous les contributeurs doivent respecter un code de conduite professionnel et courtois.

## Processus de Contribution

### 1. Avant de commencer
- Vérifiez que votre idée n'existe pas déjà dans les [issues](https://github.com/ruff78/smasse-fiche-lecon/issues)
- Créez une issue pour discuter des changements majeurs

### 2. Forking et Branching
```bash
# Fork le dépôt
# Clone votre fork
git clone https://github.com/YOUR_USERNAME/smasse-fiche-lecon.git

# Créez une branche pour votre feature
git checkout -b feature/votre-feature
```

### 3. Développement
- Suivez les standards de code du projet
- Écrivez des tests pour vos changements
- Mettez à jour la documentation si nécessaire

### 4. Commit et Push
```bash
# Commitez avec des messages clairs
git commit -m "feat: description de la feature"

# Poussez vers votre fork
git push origin feature/votre-feature
```

### 5. Pull Request
- Créez une PR vers la branche `develop`
- Décrivez clairement les changements
- Liez les issues pertinentes
- Attendez la révision

## Standards de Développement

### Python (Backend Django)
- PEP 8 pour le style de code
- Utilisez black pour le formatage
- Tapez vos annotations
- Écrivez des tests unitaires

### JavaScript/React (Frontend)
- ESLint + Prettier pour le style
- Composants fonctionnels avec hooks
- PropTypes ou TypeScript pour la typage
- Tests avec Jest

## Flux de Travail avec Git

```bash
# Avant de développer, mettez à jour depuis upstream
git fetch upstream
git rebase upstream/develop

# Développez votre feature
# ...

# Tests locaux
pytest  # Backend
npm test  # Frontend

# Push et créez une PR
git push origin feature/votre-feature
```

## Documentation

Toute contribution doit inclure :
- Code documenté (docstrings/comments)
- Tests automatisés
- Mise à jour des fichiers README pertinents

## Problèmes et Questions

Utilisez les [Discussions GitHub](https://github.com/ruff78/smasse-fiche-lecon/discussions) pour les questions.

Merci de contribuer ! 🙏
