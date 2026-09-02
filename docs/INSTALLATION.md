# Guide d'Installation

## Prérequis Système

### Tous les systèmes
- Git
- Docker & Docker Compose (recommandé)
- 4GB RAM minimum
- 2GB espace disque

### Pour développement local (sans Docker)

#### Windows/Mac/Linux
- **Python 3.9+** (Backend)
- **Node.js 16+** (Frontend Web & Desktop)
- **PostgreSQL 12+** (Base de données)
- **Redis 6+** (Cache)

## Installation Rapide (Docker)

```bash
# 1. Cloner le dépôt
git clone https://github.com/ruff78/smasse-fiche-lecon.git
cd smasse-fiche-lecon

# 2. Créer .env
cp .env.example .env

# 3. Démarrer les services
docker-compose up -d

# 4. Migrations de base de données
docker-compose exec backend python manage.py migrate

# 5. Créer un superuser
docker-compose exec backend python manage.py createsuperuser

# 6. Accéder à l'application
# - Web: http://localhost:3000
# - API: http://localhost:8000
# - Admin: http://localhost:8000/admin
```

## Installation Développement (Local)

### 1. Backend Django

```bash
# Naviguer au dossier backend
cd backend/python-django

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Mac/Linux)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer .env
cp .env.example .env

# Migrations
python manage.py migrate

# Créer superuser
python manage.py createsuperuser

# Charger les données SMASSE
python manage.py loaddata fixtures/smasse_curriculum.json

# Démarrer le serveur
python manage.py runserver
# API accessible sur http://localhost:8000
```

### 2. Frontend Web (React)

```bash
# Naviguer au dossier frontend
cd frontend/web-react

# Installer les dépendances
npm install

# Créer .env
cp .env.example .env
# Modifier REACT_APP_API_URL=http://localhost:8000

# Démarrer le serveur de développement
npm start
# Application accessible sur http://localhost:3000
```

### 3. Frontend Desktop (Electron) - Optionnel

```bash
# Naviguer au dossier desktop
cd frontend/desktop-electron

# Installer les dépendances
npm install

# Démarrer en mode développement
npm run start

# Builder pour production
npm run build
```

### 4. Frontend Mobile (Flutter) - Optionnel

```bash
# Naviguer au dossier mobile
cd frontend/mobile-flutter

# Récupérer les dépendances
flutter pub get

# Lancer sur émulateur/device
flutter run

# Builder APK
flutter build apk

# Builder iOS
flutter build ios
```

## Configuration de Base de Données

### PostgreSQL Local

```bash
# Créer la base de données
createdb smasse_fiche_lecon

# Créer l'utilisateur
createuser smasse_user

# Configurer le fichier .env
DATABASE_URL=postgresql://smasse_user:password@localhost:5432/smasse_fiche_lecon
```

### Avec Docker

```yaml
# Le docker-compose.yml inclut déjà PostgreSQL
# Pas de configuration supplémentaire nécessaire
```

## Variables d'Environnement

### Backend (.env)

```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/smasse_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your-jwt-secret

# Email (optionnel)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Export
EXPORT_STORAGE=local  # ou 's3' pour AWS S3
```

### Frontend (.env)

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

## Tests

### Backend

```bash
cd backend/python-django
python manage.py test
```

### Frontend

```bash
cd frontend/web-react
npm test
```

## Troubleshooting

### Port déjà utilisé

```bash
# Django sur port différent
python manage.py runserver 8001

# React sur port différent
PORT=3001 npm start
```

### Problèmes de base de données

```bash
# Réinitialiser la base de données
python manage.py flush
python manage.py migrate
python manage.py loaddata fixtures/smasse_curriculum.json
```

### Dépendances manquantes

```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Vérification d'Installation

```bash
# Backend
curl http://localhost:8000/api/health/

# Frontend
Naviguer à http://localhost:3000

# Admin Django
Naviguer à http://localhost:8000/admin/
Connexion avec le superuser créé
```

C'est prêt ! Vous pouvez commencer à développer. 🚀
