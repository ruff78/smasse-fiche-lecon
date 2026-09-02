# Architecture du Système

## Vue d'ensemble

SMASSE Fiche Leçon utilise une architecture modulaire avec séparation claire entre les couches.

## Architecture Générale

```
┌─────────────────────────────────────────────────────────────┐
│                    Clients (Multiplateforme)                │
├──────────────────┬──────────────────┬───────────────────────┤
│   Web (React)    │  Desktop (Electron) │  Mobile (Flutter)  │
└────────┬─────────┴──────────┬────────┴───────────┬──────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   API Gateway     │
                    │   (REST/GraphQL)  │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │ Auth    │          │ Fiche   │          │ Resource│
   │ Service │          │ Service │          │ Service │
   └────┬────┘          └────┬────┘          └────┬────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
        ┌────▼─────┐    ┌────▼─────┐    ┌──▼──────┐
        │PostgreSQL│    │   Redis  │    │ Storage │
        │Database  │    │  Cache   │    │  (S3)   │
        └──────────┘    └──────────┘    └─────────┘
```

## Couches Application

### 1. Couche Présentation (Frontend)

#### Web (React)
- SPA moderne
- État global (Redux/Context)
- Composants réutilisables
- Responsive design

#### Desktop (Electron)
- Application native-like
- Utilise le même code React
- Accès système fichiers
- Fonctionnalités offline

#### Mobile (Flutter)
- App native iOS/Android
- Interface optimisée tactile
- Synchronisation de données

### 2. Couche API (Backend)

#### Services Microservices

**Authentication Service**
- JWT tokens
- OAuth2 support
- Gestion des rôles

**Fiche Service**
- CRUD fiches de leçon
- Génération automatique
- Versioning
- Export PDF/Word

**Resource Service**
- Gestion des ressources
- Curriculum SMASSE
- Templates
- Média

**Export Service**
- Génération PDF (ReportLab/python-docx)
- Génération Word
- Formatage
- Watermarking

### 3. Couche Métier

**Modèles Métier**
```python
- User (Enseignant, Inspecteur, Admin)
- Fiche (Leçon, Exercices, Évaluation)
- Curriculum (Programme SMASSE)
- Template (Modèles de fiches)
- Resource (Ressources pédagogiques)
```

### 4. Couche Données

#### PostgreSQL
- Données métier
- Schéma normalisé
- Intégrité des données

#### Redis
- Sessions utilisateurs
- Cache de fiches
- Queues de tâches

#### Object Storage (S3/MinIO)
- PDF générés
- Documents Word
- Images/Média

## Flux de Données

### Génération d'une Fiche

```
1. Utilisateur sélectionne:
   - Niveau (6e, 5e, ...)
   - Discipline (Mathématiques, ...)
   - Chapitre (du curriculum SMASSE)

2. API Fiche Service reçoit la requête

3. Service récupère le template approprié

4. Service récupère les objectifs SMASSE

5. Service génère la structure de fiche

6. Service retourne la fiche au client

7. Client affiche/édite la fiche

8. Utilisateur demande export (PDF/Word)

9. Export Service génère le document

10. Utilisateur télécharge le fichier
```

## Sécurité

- JWT pour authentification
- RBAC (Role-Based Access Control)
- HTTPS obligatoire
- CORS configuré
- Rate limiting
- Input validation
- SQL injection prevention (ORM)

## Scalabilité

- Microservices découplés
- Caching stratégique
- Base de données optimisée
- CDN pour assets statiques
- Load balancing
- Container orchestration (Kubernetes optionnel)

## Technologies

### Backend
- **Framework**: Django REST Framework (Python)
- **Base de données**: PostgreSQL
- **Cache**: Redis
- **Export**: python-docx, ReportLab, WeasyPrint
- **Queues**: Celery
- **API**: REST + GraphQL (optionnel)

### Frontend Web
- **Framework**: React 18
- **State**: Redux Toolkit
- **Styling**: TailwindCSS
- **UI Components**: Material-UI
- **Export Client**: jsPDF, docx

### Frontend Desktop
- **Framework**: Electron
- **Runtime**: Node.js
- **UI**: React (partagé avec web)

### Frontend Mobile
- **Framework**: Flutter/Dart
- **State**: Provider/Riverpod
- **UI**: Material Design

## Deployment

- **Backend**: Docker + Kubernetes
- **Frontend Web**: Vercel/Netlify
- **Desktop**: Electron Updater
- **Mobile**: App Store, Play Store
