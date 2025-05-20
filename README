# 🛡️ PhishLab — Application d'études de campagnes de phishing

PhishLab est une application web en cours de développement qui permet de **lancer, suivre et analyser des campagnes de phishing à des fins pédagogiques ou de sensibilisation à la cybersécurité**.

Le but de ce projet est de fournir un outil complet pour :
- **Créer et configurer des campagnes de phishing**
- **Collecter les données associées**
- **Visualiser les résultats via un tableau de bord dynamique**

> 💡 Le projet intègre une stack fullstack moderne (Nuxt 3 + Django REST) et doit mettre l’accent sur la sécurité, la modularité du code, et la réutilisabilité des composants.

---

## 🚀 Fonctionnalités principales

✅ **Authentification sécurisée** avec gestion complète des tokens (JWT + refresh)  
✅ **Création de campagnes de phishing** via formulaire dynamique  
✅ **Tableau de bord des campagnes** (dashboard responsive, data-driven)

🎥 Aperçu du fonctionnement :
- Authentification + création de campagne : ![auth](./doc/IMG/auth_and_create_campaign.gif)
- Dashboard des campagnes : ![dashboard](./doc/IMG/dashboard_view.gif)

---

## 🖥️ Frontend — [Nuxt 3, PrimeVue, Pinia]

Le frontend repose sur **Nuxt 3**, avec un code structuré et orienté composabilité :

### 🔐 Authentification complète en JavaScript
- Stockage et rafraîchissement automatique des **tokens JWT / refresh tokens**
- Login/Logout, redirections sécurisées

### 🔄 Middleware & Contrôle d'accès
- Utilisation des middlewares **Nuxt** pour :
  - Protéger les routes sensibles
  - Rediriger automatiquement en fonction du statut d'authentification
  - Centraliser la logique d'accès

### 🧩 Composants & Appels API
- Composables Nuxt (`useApiFetch`, `useAuth`, etc.)
- Appels API centralisés avec gestion des erreurs et loaders

### 📱 UI Responsive & Personnalisation
- Layout responsive basé sur **PrimeFlex** (CSS utility grid system)
- **Sidebar customisée** (CSS + JS natif) avec animations
- Thème léger, séparation des vues et composants

---

## 🛠️ Backend — [Django + Django REST Framework]

Le backend repose sur **Django** avec une API REST structurée et sécurisée :

### 🧱 Architecture
- API construite avec **Django REST Framework**
- Accès aux données via le **Django ORM** et des **managers personnalisés**
- Sérialisation fine via les **serializers DRF**

### 🔐 Sécurité & Auth
- Authentification basée sur JWT (via `djangorestframework-simplejwt`)
- Permissions DRF configurées pour sécuriser les endpoints

### 📊 Base de données & modèles
- Schéma relationnel adapté aux campagnes de phishing (utilisateurs, campagnes, statistiques)
- Logique métier encapsulée dans les modèles (méthodes et managers)

---

## 📚 En cours de développement

SOS Phishing est en phase de prototypage actif. Les fonctionnalités à venir sont :

- [ ] Envoi d’emails de phishing (à intégrer)
- [ ] Statistiques détaillées pour le front : clics, saisies, temps de réponse
- [ ] Export CSV / PDF pour une campagne ou données utilisateur
- [ ] Gestion multi-utilisateurs / rôles

---

## ⚙️ Stack technique

| Frontend             | Backend              | Autres                      |
|----------------------|----------------------|-----------------------------|
| Nuxt 3               | Django 4             | Git / GitHub                |
| PrimeVue             | Django REST Framework| Docker                      |
| PrimeFlex            | PostgreSQL           | JWT / Auth sécurisée        |
| PrimeVue             | Django ORM + Managers| Composables, API Middleware |

---

## 💬 Pourquoi ce projet ?

Ce projet est né d’un double objectif :

1. **Apprentissage avancé** des technologies modernes (Nuxt 3 + DRF)
2. **Création d’un outil utile et concret** de cybersécurité

