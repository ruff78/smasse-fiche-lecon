# SMASSE Fiche Leçon - Système d'Élaboration de Fiches de Leçon

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Status](https://img.shields.io/badge/status-Development-yellow)

## 📚 À propos

SMASSE Fiche Leçon est un système complet multiplateforme pour l'élaboration automatique de fiches de leçon conformes au **programme SMASSE Niger** (Science, Mathématiques et Académies d'Enseignement).

### 🎯 Objectifs

- ✅ Générer automatiquement des fiches de leçon basées sur le curriculum SMASSE
- ✅ Supports multiplateforme (Web, Desktop, Mobile)
- ✅ Export en PDF et Word pour correction/amélioration
- ✅ Gestion centralisée des ressources pédagogiques
- ✅ Collaboration entre enseignants
- ✅ Conformité aux standards éducatifs nigériens

## 🏗️ Architecture

```
smasse-fiche-lecon/
├── backend/                 # API REST & Logique métier
│   ├── python-django/      # Service principal
│   ├── nodejs-express/     # Alternative Node.js
│   └── docker/             # Conteneurisation
├── frontend/               # Interface utilisateur
│   ├── web-react/          # Application Web (React)
│   ├── desktop-electron/   # Application Desktop (Electron)
│   └── mobile-flutter/     # Application Mobile (Flutter)
├── database/               # Schémas et migrations
├── docs/                   # Documentation
├── tests/                  # Tests automatisés
└── deploy/                 # Configuration de déploiement
```

## 🚀 Fonctionnalités Principales

### 1. Génération Automatique de Fiches
- Sélection du niveau (6e, 5e, 4e, 3e, 2nde, 1ère, Terminale)
- Sélection de la discipline (Mathématiques, Physique-Chimie, SVT, Français, etc.)
- Génération automatique basée sur les objectifs SMASSE
- Modèles prédéfinis et customisables

### 2. Structure de Fiche Standard
- En-tête (Établissement, Classe, Discipline, Chapitre)
- Objectifs pédagogiques
- Prérequis
- Contenu structuré
- Activités et exercices
- Évaluation
- Ressources recommandées

### 3. Export et Édition
- Export PDF haute qualité
- Export Word pour édition ultérieure
- Impression directe
- Partage et collaboration

### 4. Gestion des Utilisateurs
- Authentification sécurisée
- Rôles (Enseignant, Inspecteur, Administrateur)
- Espaces personnels
- Historique des fiches

## 📋 Prérequis

### Backend
- Python 3.9+ ou Node.js 16+
- PostgreSQL 12+
- Redis (cache et sessions)

### Frontend
- Node.js 16+ (React)
- Flutter SDK (Mobile)
- Electron (Desktop)

## 🔧 Installation

### Cloner le dépôt
```bash
git clone https://github.com/ruff78/smasse-fiche-lecon.git
cd smasse-fiche-lecon
```

### Backend (Django)
```bash
cd backend/python-django
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sur Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Web (React)
```bash
cd frontend/web-react
npm install
npm start
```

## 📚 Documentation

Consultez les guides détaillés :
- [Guide d'Installation](./docs/INSTALLATION.md)
- [Architecture Système](./docs/ARCHITECTURE.md)
- [API Documentation](./docs/API.md)
- [Guide Utilisateur](./docs/GUIDE_UTILISATEUR.md)
- [Guide de Contribution](./CONTRIBUTING.md)

## 🤝 Contribution

Les contributions sont bienvenues ! Veuillez consulter [CONTRIBUTING.md](./CONTRIBUTING.md) pour les directives.

## 📝 Programme SMASSE Niger

Ce projet est basé sur :
- Programmes officiels du Ministère de l'Éducation du Niger
- Référentiels SMASSE Niger
- Standards pédagogiques internationaux

## 📧 Support

Pour toute question ou problème :
- Créez une [Issue GitHub](https://github.com/ruff78/smasse-fiche-lecon/issues)
- Contactez l'équipe de développement

## 📄 Licence

Ce projet est licencié sous la [Licence Apache 2.0](./LICENSE)

## 👥 Auteurs

- **Ruff78** - Concepteur initial

## 🙏 Remerciements

- Ministère de l'Éducation du Niger
- Coordonnateurs SMASSE Niger
- Enseignants et inspecteurs contributeurs

---

**Version:** 0.1.0 | **Dernière mise à jour:** 2026-09-02
