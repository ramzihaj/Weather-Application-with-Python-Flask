# 🌤️ Weather App - Application Météo Moderne

Une application météo moderne et complète construite avec Flask, offrant des fonctionnalités avancées et une interface utilisateur élégante.

## ✨ Fonctionnalités

### 🎯 **Fonctionnalités Principales**
- **Météo actuelle** avec informations détaillées
- **Prévisions sur 5 jours** avec données horaires
- **Recherche par ville** avec sélection de pays
- **Géolocalisation GPS** pour la météo locale
- **Qualité de l'air** (AQI) en temps réel
- **Historique des recherches** (10 dernières)

### 🌍 **Recherche Avancée**
- **Autocomplétion** des villes avec l'API Geocoding
- **Sélection de pays** pour des résultats précis
- **Support de 50+ pays** avec codes ISO
- **Recherche par coordonnées** GPS (latitude/longitude)

### 🌡️ **Unités de Mesure**
- **Celsius (°C)** - Système métrique
- **Fahrenheit (°F)** - Système impérial  
- **Kelvin (K)** - Système scientifique
- **Conversion automatique** entre unités

### 📊 **Données Météorologiques Complètes**
- Température actuelle et ressentie
- Humidité et pression atmosphérique
- Vitesse et direction du vent
- Visibilité et conditions météo
- Heures de lever/coucher du soleil
- Index de qualité de l'air (AQI)

### 🎨 **Interface Moderne**
- **Design glassmorphisme** avec effets de flou
- **Animations fluides** et transitions CSS
- **Responsive design** (mobile, tablette, desktop)
- **Icônes météo dynamiques** selon les conditions
- **Thème sombre** avec dégradés modernes

### ⚡ **Fonctionnalités Avancées**
- **Raccourcis clavier** (Ctrl+K pour recherche)
- **Actualisation automatique** toutes les 10 minutes
- **Particules flottantes** et effets visuels
- **Historique persistant** avec sessions Flask
- **API endpoints** pour intégrations externes

## 🚀 Installation

### Prérequis
- Python 3.7+
- Clé API OpenWeatherMap (gratuite)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/ramzihaj/Weather-Application-with-Python-Flask.git
cd Weather-Application-with-Python-Flask
```

2. **Installer les dépendances**
```bash
pip install -r requirements_new.txt
```

3. **Configurer l'API Key**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter votre clé API
API_KEY=votre_cle_api_openweathermap
```

4. **Obtenir une clé API gratuite**
- Aller sur [OpenWeatherMap](https://openweathermap.org/api)
- Créer un compte gratuit
- Générer une clé API
- Copier la clé dans le fichier `.env`

5. **Lancer l'application**
```bash
python server.py
```

6. **Ouvrir dans le navigateur**
```
http://localhost:8000
```

## 📱 Utilisation

### Recherche Basique
1. Entrer le nom d'une ville
2. Sélectionner un pays (optionnel)
3. Choisir l'unité de température
4. Cliquer sur "Get Weather"

### Géolocalisation
1. Cliquer sur "📍 Use My Location"
2. Autoriser l'accès à la localisation
3. La météo locale s'affiche automatiquement

### Prévisions
1. Sur la page météo, cliquer "📅 5-Day Forecast"
2. Voir les prévisions détaillées jour par jour
3. Informations sur température, humidité, vent

### Historique
1. Cliquer "🕒 Search History"
2. Voir les 10 dernières recherches
3. Cliquer sur une entrée pour revoir la météo

## 🛠️ Structure du Projet

```
Weather-Application-with-Python-Flask/
├── server.py              # Serveur Flask principal
├── weather.py             # Module API météo
├── requirements_new.txt   # Dépendances Python
├── .env.example          # Configuration d'exemple
├── README.md             # Documentation
├── static/
│   ├── styles/
│   │   └── style.css     # Styles CSS modernes
│   └── js/
│       └── weather.js    # JavaScript interactif
└── templates/
    ├── index.html        # Page d'accueil
    ├── weather.html      # Affichage météo
    ├── forecast.html     # Prévisions 5 jours
    ├── history.html      # Historique recherches
    └── city-not-found.html # Page d'erreur
```

## 🔧 API Endpoints

### Routes Principales
- `GET /` - Page d'accueil
- `GET /weather` - Météo actuelle
- `GET /forecast` - Prévisions 5 jours
- `GET /history` - Historique des recherches

### API JSON
- `GET /api/search_cities?q=paris` - Recherche de villes
- `GET /api/convert_temperature` - Conversion d'unités

### Paramètres Supportés
- `city` - Nom de la ville
- `country` - Nom du pays
- `units` - Unités (metric/imperial/kelvin)
- `lat`, `lon` - Coordonnées GPS
- `days` - Nombre de jours de prévision

## 🌟 Fonctionnalités Techniques

### Backend (Flask)
- **Sessions** pour l'historique utilisateur
- **Gestion d'erreurs** robuste
- **API RESTful** avec endpoints JSON
- **Validation** des données d'entrée
- **Cache** et optimisations

### Frontend (JavaScript/CSS)
- **Fetch API** pour requêtes asynchrones
- **Geolocation API** pour GPS
- **Local Storage** pour préférences
- **CSS Grid/Flexbox** pour layouts
- **Animations CSS3** avancées

### APIs Externes
- **OpenWeatherMap Current Weather** - Météo actuelle
- **OpenWeatherMap Forecast** - Prévisions 5 jours
- **OpenWeatherMap Geocoding** - Recherche de villes
- **OpenWeatherMap Air Pollution** - Qualité de l'air

## 🎯 Raccourcis Clavier

- `Ctrl + K` - Focus sur la recherche
- `Escape` - Effacer la recherche
- `Enter` - Lancer la recherche

## 📱 Responsive Design

### Breakpoints
- **Desktop** : > 768px - Layout complet
- **Tablet** : 481px - 768px - Layout adapté
- **Mobile** : < 480px - Layout mobile

### Optimisations Mobile
- Interface tactile optimisée
- Boutons plus grands
- Navigation simplifiée
- Chargement rapide

## 🔮 Fonctionnalités Futures

- [ ] **Notifications push** pour alertes météo
- [ ] **Widgets personnalisables** sur dashboard
- [ ] **Comparaison de villes** côte à côte
- [ ] **Graphiques interactifs** des tendances
- [ ] **Mode sombre/clair** commutable
- [ ] **PWA** (Progressive Web App)
- [ ] **Base de données** pour favoris
- [ ] **Authentification utilisateur**

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Ramzi Haj** - [GitHub](https://github.com/ramzihaj)

## 🙏 Remerciements

- [OpenWeatherMap](https://openweathermap.org/) pour l'API météo
- [Flask](https://flask.palletsprojects.com/) pour le framework web
- [Google Fonts](https://fonts.google.com/) pour la typographie Inter
- Communauté open source pour l'inspiration

---

⭐ **N'hésitez pas à donner une étoile si ce projet vous plaît !**
