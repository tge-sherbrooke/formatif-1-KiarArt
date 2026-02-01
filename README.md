# Formatif F1 — Introduction au Raspberry Pi et capteurs Adafruit

**Cours** : 243-413-SH — Introduction aux objets connectes
**Semaine** : 1
**Type** : Formative (non notee)
**Retries** : Illimites - poussez autant de fois que necessaire!

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Script existe, syntaxe valide, tests locaux executes |
| **Milestone 2** | 35 pts | I2C initialise, capteur BMP280 cree, lecture temperature/pression |
| **Milestone 3** | 40 pts | Fonction main(), gestion d'erreurs, qualite du code |

**Chaque test echoue vous dit**:
- Ce qui etait attendu
- Ce qui a ete trouve
- Une suggestion pour corriger

---

## Objectif

Ce formatif vise a verifier que vous etes capable de :
1. Creer une cle SSH sur le Raspberry Pi et l'ajouter a votre compte GitHub
2. Installer UV et gerer les dependances Python
3. Detecter un capteur I2C avec `i2cdetect`
4. Lire un capteur BMP280 (temperature, pression, altitude)
5. Controler un NeoSlider (potentiometre + LEDs) - optionnel

---

## Workflow de soumission

⚠️ **IMPORTANT** : Pour que votre travail soit accepté, vous devez **exécuter les tests localement sur le Raspberry Pi AVANT de pousser**.

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKLOAD FORMATIF F1                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Sur le Raspberry Pi (via SSH avec mot de passe)            │
│     └─ Créer une clé SSH                                      │
│     └─ Afficher la clé publique                               │
│                                                                  │
│  2. Sur GitHub (via navigateur)                               │
│     └─ Ajouter la clé SSH à votre compte                      │
│     └─ Tester la connexion (ssh -T git@github.com)             │
│                                                                  │
│  3. Sur le Raspberry Pi                                        │
│     └─ Installer UV                                            │
│     └─ Cloner votre dépôt GitHub (avec URL SSH)                │
│     └─ Créer test_bmp280.py                                   │
│     └─ Exécuter: python3 run_tests.py                         │
│     └─ Corriger les erreurs                                    │
│     └─ Pousser: git add, commit, push                         │
│                                                                  │
│  4. GitHub Actions valide automatiquement                     │
│     └─ Vérifie les marqueurs de tests                         │
│     └─ Confirme que vous avez tout complété                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Instructions détaillées

### Étape 1 : Créer une clé SSH sur le Raspberry Pi

Connectez-vous d'abord au Raspberry Pi avec votre mot de passe :

```bash
ssh utilisateur@HOSTNAME.local
```

Puis, générez une clé SSH **directement sur le Raspberry Pi** :

```bash
# Générer la clé avec un commentaire identifiant
ssh-keygen -t ed25519 -C "iot-cegep@etu.cegep.qc.ca" -f ~/.ssh/id_ed25519_iot
```

- Appuyez **Entrée** pour accepter l'emplacement par défaut
- Appuyez **Entrée** deux fois pour laisser la passphrase vide

#### Afficher la clé publique

```bash
cat ~/.ssh/id_ed25519_iot.pub
```

Copiez **toute** la ligne affichée (commence par `ssh-ed25519 ...`)

---

### Étape 2 : Ajouter la clé SSH à votre compte GitHub

1. Allez sur https://github.com et connectez-vous
2. Cliquez sur votre photo → **Settings**
3. Menu gauche → **SSH and GPG keys**
4. Cliquez sur **New SSH key**
5. Remplissez :
   - **Title** : `Raspberry Pi IoT - Cours 243-413-SH`
   - **Key** : Collez la clé publique copiée
   - **Key type** : Authentication Key
6. Cliquez sur **Add SSH key**

#### Configurer SSH pour GitHub

Toujours sur le Raspberry Pi :

```bash
# Ajouter la clé à l'agent SSH
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_iot

# Créer un config pour utiliser cette clé avec GitHub
cat > ~/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_iot
    IdentitiesOnly yes
EOF

# Sécuriser le fichier config
chmod 600 ~/.ssh/config
```

#### Tester la connexion avec GitHub

```bash
ssh -T git@github.com
```

**Résultat attendu** (si succès) :
```
Hi votrenom! You've successfully authenticated, but GitHub does not provide shell access.
```

> 🎉 **Bravo !** Votre clé SSH est configurée et vous pouvez maintenant cloner et pousser directement depuis le Raspberry Pi !

---

### Étape 3 : Installer UV et cloner le dépôt

Une fois la clé SSH configurée :

```bash
# Installer UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recharger le shell
source ~/.bashrc

# Configurer Git (IMPORTANT!)
git config --global user.name "Prénom Nom"
git config --global user.email "votre.email@cegepsherbrooke.qc.ca"
git config --global init.defaultbranch main
```

```bash
# Cloner votre dépôt GitHub Classroom avec l'URL SSH
git clone git@github.com:tge-sherbrooke/semaine-1-f1-votre-username.git
cd semaine-1-f1-votre-username
```

> **Note** : Utilisez l'URL **SSH** affichée sur GitHub (commence par `git@github.com:`)

---

### Étape 4 : Activer I2C et vérifier les capteurs

```bash
# Activer I2C
sudo raspi-config nonint do_i2c 0

# Installer les outils I2C
sudo apt update && sudo apt install -y i2c-tools

# Scanner le bus I2C
sudo i2cdetect -y 1
```

Vous devriez voir :
- `77` pour le BMP280
- `30` pour le NeoSlider

⚠️ **IMPORTANT** : Les capteurs fonctionnent UNIQUEMENT en 3.3V !

---

### Étape 5 : Créer et tester le BMP280

Créez le fichier `test_bmp280.py` :

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-bmp280", "adafruit-blinka"]
# ///
"""Test du capteur BMP280 via STEMMA QT/I2C."""

import board
import adafruit_bmp280

i2c = board.I2C()
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)

print(f"Température: {sensor.temperature:.1f} °C")
print(f"Pression: {sensor.pressure:.1f} hPa")
print(f"Altitude: {sensor.altitude:.1f} m")
```

Testez-le :

```bash
uv run test_bmp280.py
```

---

### Étape 6 : Créer et tester le NeoSlider (optionnel)

Créez le fichier `test_neoslider.py` :

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-seesaw", "adafruit-blinka"]
# ///
"""Test du NeoSlider - Animation arc-en-ciel sur les LEDs."""

import board
import time
from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw import neopixel

# Configuration NeoSlider
i2c = board.I2C()
neoslider = Seesaw(i2c, 0x30)
pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

# Position dans la roue des couleurs
color_pos = 0

while True:
    pixels.fill(colorwheel(color_pos))
    color_pos = (color_pos + 1) % 256
    time.sleep(0.02)
```

Testez-le :

```bash
uv run test_neoslider.py
```

---

### Étape 7 : ⭐ Exécuter les tests locaux

**Ceci est l'étape obligatoire avant de pousser!**

```bash
python3 run_tests.py
```

Le script `run_tests.py` va :
1. ✅ Vérifier que votre clé SSH existe
2. ✅ Vérifier que `test_bmp280.py` est correct
3. ✅ Vérifier que `test_neoslider.py` est correct (optionnel)
4. ✅ Scanner le bus I2C pour détecter les capteurs
5. ✅ Créer des fichiers marqueurs dans `.test_markers/`

Si tous les tests passent, vous verrez :
```
🎉 TOUS LES TESTS SONT PASSÉS!
```

---

### Étape 8 : Pousser votre travail

Une fois les tests passés :

```bash
git add .
git commit -m "feat: tests BMP280 et NeoSlider complétés"
git push
```

GitHub Actions validera automatiquement que vous avez exécuté les tests.

---

## Câblage STEMMA QT

| Fil | Raspberry Pi |
|-----|--------------|
| Rouge (VIN) | 3.3V |
| Noir (GND) | GND |
| Bleu (SDA) | GPIO 2 |
| Jaune (SCL) | GPIO 3 |

⚠️ **VIN doit être connecté à 3.3V, PAS 5V !**

---

## Comprendre la validation

### Pourquoi exécuter `run_tests.py` AVANT de pousser ?

Le formatif F1 utilise une validation en deux temps :

| Étape | Où | Ce qui est validé |
|-------|----|-------------------|
| **run_tests.py** | Sur Raspberry Pi | - Clé SSH créée sur le Pi<br>- Connexion GitHub fonctionnelle<br>- Scripts créés<br>- Capteurs détectés |
| **GitHub Actions** | Automatique après push | - Les marqueurs existent<br>- Syntaxe Python valide |

Cette approche garantit que vous avez **réellement** travaillé sur le matériel tout en bénéficiant de l'automatisation GitHub.

### Que se passe-t-il si je pousse sans exécuter les tests ?

GitHub Actions affichera une erreur :
```
❌ ERREUR: Les tests locaux n'ont pas été exécutés!
```

Vous devrez alors exécuter `python3 run_tests.py` sur le Raspberry Pi et repousser.

---

## Livrables

Dans ce dépôt, vous devez avoir :

- [ ] `test_bmp280.py` — Script de lecture du capteur BMP280
- [ ] `test_neoslider.py` — Script de test du NeoSlider (optionnel)
- [ ] `.test_markers/` — Dossier créé par `run_tests.py` (ne pas éditer manuellement!)

---

## Résumé des commandes

```bash
# ===== SUR RASPBERRY PI (connexion initiale) =====
ssh utilisateur@HOSTNAME.local

# ===== CRÉER LA CLÉ SSH =====
ssh-keygen -t ed25519 -C "iot-cegep@etu.cegep.qc.ca" -f ~/.ssh/id_ed25519_iot

# ===== AFFICHER LA CLÉ (à copier pour GitHub) =====
cat ~/.ssh/id_ed25519_iot.pub

# ===== AJOUTER LA CLÉ À GITHUB =====
# Allez sur https://github.com → Settings → SSH and GPG keys → New SSH key

# ===== CONFIGURER SSH SUR LE PI =====
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_iot
cat > ~/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_iot
    IdentitiesOnly yes
EOF
chmod 600 ~/.ssh/config

# ===== TESTER LA CONNEXION GITHUB =====
ssh -T git@github.com

# ===== INSTALLER UV =====
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc

# ===== CONFIGURER GIT =====
git config --global user.name "Prénom Nom"
git config --global user.email "votre.email@etu.cegep.qc.ca"

# ===== CLONER LE DÉPÔT (AVEC URL SSH) =====
git clone git@github.com:tge-sherbrooke/semaine-1-f1-votre-username.git
cd semaine-1-f1-votre-username

# ===== ACTIVER I2C =====
sudo raspi-config nonint do_i2c 0
sudo apt install -y i2c-tools

# ===== SCANNER I2C =====
sudo i2cdetect -y 1

# ===== TESTER LES CAPTEURS =====
uv run test_bmp280.py
uv run test_neoslider.py

# ===== EXÉCUTER LES TESTS =====
python3 run_tests.py

# ===== POUSSER =====
git add .
git commit -m "feat: tests complétés"
git push
```

---

## Ressources

- [Guide de l'étudiant](../deliverables/activites/semaine-1/labo/guide-étudiant.md)
- [Guide de dépannage](../deliverables/activites/semaine-1/labo/guide-depannage.md)

---

Bonne chance ! 🚀
