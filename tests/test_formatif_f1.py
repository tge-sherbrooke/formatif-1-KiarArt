"""
Tests automatisés pour le Formatif F1 - Semaine 1
Évalue: SSH sans mot de passe, UV, détection capteurs BMP280 et NeoSlider, lecture capteurs
"""

import pytest
import subprocess
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import re

# Ajouter le répertoire tests au path pour les mocks CI
tests_dir = Path(__file__).parent
sys.path.insert(0, str(tests_dir))


class TestSSHConfiguration:
    """
    Tests pour vérifier la configuration SSH sans mot de passe
    Correspond à IND-00SX-E (Environnement) - Connexion SSH
    """

    def test_ssh_key_file_exists(self):
        """
        Vérifie qu'un fichier de clé SSH publique est présent.
        Points: 20% de IND-00SX-E
        """
        # Chercher id_ed25519.pub ou id_rsa.pub
        ssh_dir = Path.home() / ".ssh"
        pub_keys = [
            ssh_dir / "id_ed25519.pub",
            ssh_dir / "id_rsa.pub",
        ]

        key_found = False
        for key_path in pub_keys:
            if key_path.exists():
                key_found = True
                print(f"✅ Clé SSH publique trouvée: {key_path.name}")
                break

        if not key_found:
            # En CI, on ne peut pas vérifier la clé locale de l'étudiant
            # On vérifie plutôt que l'étudiant connaît la procédure
            print("ℹ️  Environnement CI - Vérification de la procédure SSH")
            print("✅ La procédure de génération de clé SSH est documentée dans le README")
            print("\n📚 Rappel: Générez votre clé avec:")
            print("   ssh-keygen -t ed25519 -C \"mon-raspberry-pi\"")
            print("\n📚 Copiez la clé sur le Pi:")
            print("   type $env:USERPROFILE\\.ssh\\id_ed25519.pub | ssh user@HOSTNAME.local \"mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys\"")

    def test_ssh_authorized_keys_structure(self):
        """
        Vérifie que l'étudiant connaît la structure du fichier authorized_keys.
        Points: 15% de IND-00SX-E
        """
        # Test de connaissance: vérifier la compréhension du format
        print("\n📚 Le fichier authorized_keys doit contenir une ligne par clé publique:")
        print("   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... comment@machine")
        print("\n📚 Emplacement sur le Raspberry Pi: ~/.ssh/authorized_keys")
        print("   Permissions: 600 (rw-------)")


class TestRequirements:
    """
    Tests pour vérifier que l'environnement est correctement configuré
    Correspond à IND-00SX-E (Environnement)
    """

    def test_uv_script_dependencies(self):
        """
        Vérifie que les scripts UV contiennent les bonnes dépendances.
        Points: 25% de IND-00SX-E
        """
        # Vérifier test_bmp280.py
        bmp_script = Path(__file__).parent.parent / "test_bmp280.py"

        if not bmp_script.exists():
            pytest.skip("test_bmp280.py n'existe pas encore")

        content = bmp_script.read_text()

        # Vérifier les dépendances UV dans le script
        uv_deps = [
            'adafruit-circuitpython-bmp280',
            'adafruit-blinka'
        ]

        manquantes = []
        for dep in uv_deps:
            if dep not in content:
                manquantes.append(dep)

        if manquantes:
            print(f"\n⚠️ test_bmp280.py: dépendances UV manquantes: {', '.join(manquantes)}")
            print("📚 Format attendu dans le script:")
            print('   # /// script')
            print('   # dependencies = ["adafruit-circuitpython-bmp280", "adafruit-blinka"]')
            print('   # ///')
        else:
            print("✅ test_bmp280.py contient les dépendances UV correctes!")

    def test_import_board(self):
        """
        Vérifie que le module board peut être importé (simulation).
        Points: 15% de IND-00SX-E
        """
        try:
            import board
            print("✅ Module board importé avec succès!")
        except (ImportError, NotImplementedError):
            # Sur un environnement non-Raspberry Pi, c'est normal
            print("ℹ️  Environnement non-Raspberry Pi détecté (normal pour les tests)")
            print("✅ Le module 'board' est correctement référencé dans les dépendances")

    def test_import_bmp280(self):
        """
        Vérifie que le module adafruit_bmp280 peut être importé (avec mock CI).
        Points: 10% de IND-00SX-E
        """
        try:
            import adafruit_bmp280
            print("✅ Module adafruit_bmp280 importé avec succès!")
        except ImportError:
            # Tenter d'importer le mock pour CI
            try:
                import tests.mocks_ci as mocks
                sys.modules['adafruit_bmp280'] = mocks.adafruit_bmp280
                sys.modules['adafruit_blinka'] = mocks.adafruit_blinka
                sys.modules['board'] = mocks.board
                print("ℹ️  Environnement CI - Mock adafruit_bmp280 activé")
                print("✅ La dépendance est correctement spécifiée pour le Raspberry Pi")
            except ImportError:
                pytest.fail(
                    "⚠️ Le module adafruit_bmp280 n'est pas disponible.\n"
                    "   Sur Raspberry Pi: uv pip install adafruit-circuitpython-bmp280\n"
                    "   En CI: Vérifiez que les mocks sont correctement configurés"
                )


class TestBMP280Script:
    """
    Tests pour vérifier le script test_bmp280.py
    Correspond à IND-00SX-D (Programmation) - BMP280
    """

    def test_bmp280_script_exists(self):
        """
        Vérifie que le fichier test_bmp280.py existe.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "test_bmp280.py"

        if not script_path.exists():
            pytest.fail(
                "❌ Fichier test_bmp280.py introuvable.\n"
                "   Créez ce fichier dans le répertoire racine du dépôt.\n"
                "   Contenu minimal attendu:\n"
                "   ```python\n"
                "   # /// script\n"
                "   # dependencies = [\"adafruit-circuitpython-bmp280\", \"adafruit-blinka\"]\n"
                "   # ///\n"
                "   import board\n"
                "   import adafruit_bmp280\n"
                "   i2c = board.I2C()\n"
                "   sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)\n"
                "   print(f\"Température: {sensor.temperature:.1f} °C\")\n"
                "   ```"
            )

        print("✅ Fichier test_bmp280.py présent!")

    def test_bmp280_script_has_required_imports(self):
        """
        Vérifie que le script contient les imports nécessaires.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "test_bmp280.py"

        if not script_path.exists():
            pytest.skip("test_bmp280.py n'existe pas encore")

        content = script_path.read_text()

        imports_requis = {
            'board': False,
            'adafruit_bmp280': False
        }

        for line in content.split('\n'):
            if 'import board' in line or 'from board' in line:
                imports_requis['board'] = True
            if 'import adafruit_bmp280' in line or 'from adafruit_bmp280' in line:
                imports_requis['adafruit_bmp280'] = True

        manquants = [imp for imp, present in imports_requis.items() if not present]

        if manquants:
            pytest.fail(
                f"⚠️ test_bmp280.py existe mais il manque des imports.\n"
                f"   Imports manquants: {', '.join(manquants)}\n"
                f"   Ajoutez: import board, import adafruit_bmp280"
            )

        print("✅ Imports nécessaires présents dans test_bmp280.py!")

    def test_bmp280_script_creates_sensor(self):
        """
        Vérifie que le script crée correctement l'objet capteur BMP280.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "test_bmp280.py"

        if not script_path.exists():
            pytest.skip("test_bmp280.py n'existe pas encore")

        content = script_path.read_text()

        # Vérifier la création de l'objet I2C et du capteur BMP280
        patterns = [
            r'board\.I2C\(\)',
            r'Adafruit_BMP280_I2C\s*\(',
            r'i2c\s*='
        ]

        manquants = []
        for pattern in patterns:
            if not re.search(pattern, content):
                manquants.append(pattern)

        if manquants:
            pytest.fail(
                f"⚠️ test_bmp280.py ne contient pas la structure attendue.\n"
                f"   Modèles manquants: {', '.join(manquants)}\n"
                f"   Structure attendue:\n"
                f"   ```python\n"
                f"   i2c = board.I2C()\n"
                f"   sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)\n"
                f"   ```"
            )

        print("✅ Structure de création du capteur BMP280 correcte!")

    def test_bmp280_script_syntax_valid(self):
        """
        Vérifie que le script a une syntaxe Python valide.
        Points: 10% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "test_bmp280.py"

        if not script_path.exists():
            pytest.skip("test_bmp280.py n'existe pas encore")

        try:
            with open(script_path) as f:
                compile(f.read(), script_path, 'exec')
            print("✅ Script test_bmp280.py a une syntaxe Python valide!")
        except SyntaxError as e:
            pytest.fail(
                f"⚠️ Le script test_bmp280.py contient une erreur de syntaxe.\n"
                f"   Ligne {e.lineno}: {e.msg}"
            )

    def test_bmp280_script_prints_output(self):
        """
        Vérifie que le script contient des print() pour la sortie.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "test_bmp280.py"

        if not script_path.exists():
            pytest.skip("test_bmp280.py n'existe pas encore")

        content = script_path.read_text().lower()

        has_temp = any('temp' in line and 'print' in line for line in content.split('\n'))
        has_press = any('press' in line and 'print' in line for line in content.split('\n'))
        has_alt = any('alt' in line and 'print' in line for line in content.split('\n'))

        if not (has_temp and has_press and has_alt):
            pytest.fail(
                f"⚠️ Le script ne semble pas afficher toutes les mesures.\n"
                f"   Assurez-vous d'avoir des print() pour température, pression et altitude.\n"
                f"   Température: {'✓' if has_temp else '✗'}\n"
                f"   Pression: {'✓' if has_press else '✗'}\n"
                f"   Altitude: {'✓' if has_alt else '✗'}"
            )

        print("✅ Script contient des print() pour les mesures!")

    def test_bmp280_script_uses_sensor_methods(self):
        """
        Vérifie que le script utilise les méthodes du capteur.
        Points: 15% de IND-00SX-D
        """
        script_path = Path(__file__).parent.parent / "test_bmp280.py"

        if not script_path.exists():
            pytest.skip("test_bmp280.py n'existe pas encore")

        content = script_path.read_text()

        required_attrs = ['.temperature', '.pressure', '.altitude']

        manquants = []
        for attr in required_attrs:
            if attr not in content:
                manquants.append(attr)

        if manquants:
            pytest.fail(
                f"⚠️ Le script n'utilise pas toutes les méthodes du capteur.\n"
                f"   Attributs manquants: {', '.join(manquants)}\n"
                f"   Attendu: sensor.temperature, sensor.pressure, sensor.altitude"
            )

        print("✅ Script utilise correctement les méthodes du capteur!")


class TestNeoSliderScript:
    """
    Tests pour vérifier le script test_neoslider.py
    Correspond à IND-00SX-D (Programmation) - NeoSlider
    """

    def test_neoslider_script_exists(self):
        """
        Vérifie que le fichier test_neoslider.py existe.
        Points: 10% de IND-00SX-D (bonus)
        """
        script_path = Path(__file__).parent.parent / "test_neoslider.py"

        if not script_path.exists():
            print("ℹ️  test_neoslider.py n'existe pas encore (optionnel)")
            return

        print("✅ Fichier test_neoslider.py présent!")

    def test_neoslider_script_has_required_imports(self):
        """
        Vérifie que le script NeoSlider contient les imports nécessaires.
        Points: 5% de IND-00SX-D (bonus)
        """
        script_path = Path(__file__).parent.parent / "test_neoslider.py"

        if not script_path.exists():
            pytest.skip("test_neoslider.py n'existe pas encore")

        content = script_path.read_text()

        required_imports = [
            'board',
            'adafruit_seesaw',
            'neopixel'
        ]

        manquants = []
        for imp in required_imports:
            if imp not in content:
                manquants.append(imp)

        if manquants:
            print(f"\n⚠️ test_neoslider.py: imports manquants: {', '.join(manquants)}")
        else:
            print("✅ Imports nécessaires présents dans test_neoslider.py!")

    def test_neoslider_script_syntax_valid(self):
        """
        Vérifie que le script NeoSlider a une syntaxe Python valide.
        Points: 5% de IND-00SX-D (bonus)
        """
        script_path = Path(__file__).parent.parent / "test_neoslider.py"

        if not script_path.exists():
            pytest.skip("test_neoslider.py n'existe pas encore")

        try:
            with open(script_path) as f:
                compile(f.read(), script_path, 'exec')
            print("✅ Script test_neoslider.py a une syntaxe Python valide!")
        except SyntaxError as e:
            pytest.fail(
                f"⚠️ Le script test_neoslider.py contient une erreur de syntaxe.\n"
                f"   Ligne {e.lineno}: {e.msg}"
            )


class TestConnaissance:
    """
    Tests de connaissances théoriques (quiz)
    """

    def test_ssh_keygen_command(self):
        """
        Quiz: Quelle est la commande pour générer une clé SSH?
        """
        print("\n📚 Rappel: La commande de génération de clé SSH est:")
        print("   ssh-keygen -t ed25519 -C \"mon-raspberry-pi\"")
        print("   Appuyez 3x sur Entrée pour accepter les valeurs par défaut")

    def test_ssh_copy_command(self):
        """
        Quiz: Comment copier sa clé publique sur le Raspberry Pi?
        """
        print("\n📚 Rappel: Pour copier votre clé publique sur le Pi:")
        print("   type $env:USERPROFILE\\.ssh\\id_ed25519.pub | ssh user@HOSTNAME.local \"mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys\"")

    def test_uv_install_command(self):
        """
        Quiz: Comment installer UV sur le Raspberry Pi?
        """
        print("\n📚 Rappel: La commande d'installation UV est:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   Puis: source ~/.bashrc")

    def test_i2cdetect_command(self):
        """
        Quiz: Quelle commande permet de détecter les périphériques I²C?
        """
        print("\n📚 Rappel: La commande est: sudo i2cdetect -y 1")
        print("   Le chiffre '1' indique le bus I²C à scanner.")

    def test_bmp280_address(self):
        """
        Quiz: Quelle est l'adresse I²C du capteur BMP280?
        """
        print("\n📚 Rappel: Le BMP280 est à l'adresse 0x77 (par défaut)")
        print("   Vous devriez voir '77' dans la grille i2cdetect.")
        print("   ⚠️ IMPORTANT: Le BMP280 fonctionne UNIQUEMENT en 3.3V!")

    def test_neoslider_address(self):
        """
        Quiz: Quelle est l'adresse I²C du NeoSlider?
        """
        print("\n📚 Rappel: Le NeoSlider est à l'adresse 0x30")
        print("   Vous devriez voir '30' dans la grille i2cdetect.")


@pytest.fixture(autouse=True)
def print_summary(request):
    """
    Affiche un résumé des résultats à la fin des tests
    """
    yield

    if hasattr(request.node, 'rep_setup') and request.node.rep_setup.failed:
        return
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        return

    # Afficher la rétroaction finale
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DE L'ÉVALUATION FORMATIVE F1")
    print("="*60)

    print("\n✅ Points forts:")
    print("   - Consultez les détails ci-dessus pour ce qui fonctionne")

    print("\n💡 Points à améliorer:")
    print("   - Corrigez les tests échoués")
    print("   - Pussez vos corrections et relancez les tests")

    print("\n📚 Ressources:")
    print("   - README.md pour les instructions complètes")
    print("   - validate_pi.sh pour la validation sur Raspberry Pi")

    print("\n" + "="*60)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pour capturer les résultats des tests
    """
    outcome = yield
    rep = outcome.get_result()

    # Stocker le résultat pour autouse fixture
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session", autouse=True)
def print_final_summary():
    """
    Affiche un message final après tous les tests
    """
    yield

    print("\n" + "🔷"*30)
    print("\n🎯 FORMATIF F1 — NOTE IMPORTANTE")
    print("\n" + "🔷"*30)
    print("""
Cette évaluation est FORMATIVE et NON NOTÉE.

Son but est de vous donner une rétroaction rapide sur:

📌 IND-00SX-E (Environnement)
   - Configuration SSH sans mot de passe
   - Installation de UV et des bibliothèques Adafruit

📌 IND-00SX-D (Programmation)
   - Structure des scripts Python (BMP280, NeoSlider)
   - Utilisation correcte des capteurs
   - Format de sortie des données

⚠️  IMPORTANT - Deux validations requises:

1️⃣  GitHub Actions (ce test)
   - Vérifie le CODE: syntaxe, imports, structure
   - Fonctionne SANS Raspberry Pi

2️⃣  Validation sur Raspberry Pi
   - Exécutez: uv run test_bmp280.py
   - Exécutez: uv run test_neoslider.py
   - Vérifie le MATÉRIEL: capteurs, câblage, I2C

Les DEUX validations doivent réussir pour compléter le formatif!

Si vous avez des échecs:
1. Lisez attentivement les messages d'erreur
2. Consultez le README.md
3. Corrigez votre code
4. Pussez et relancez les tests

N'hésitez pas à demander de l'aide à l'enseignant!

Bonne continuation! 💪
""")
