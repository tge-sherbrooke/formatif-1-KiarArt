"""
Mocks pour les bibliothèques matérielles (Adafruit) dans l'environnement CI.

Ces mocks permettent de tester la structure du code sans avoir le matériel.
Ils sont utilisés uniquement dans GitHub Actions pour les tests formaitifs.
"""

from unittest.mock import MagicMock, Mock


class MockI2C:
    """Mock pour le bus I2C."""
    def __init__(self):
        self.address = 0x77
        self.scan_called = False

    def scan(self):
        """Simule la détection de périphériques I2C."""
        self.scan_called = True
        return [0x77]

    def try_lock(self):
        return True

    def unlock(self):
        pass

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        pass

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *, out_start=0, out_end=None, in_start=0, in_end=None):
        pass


# Mock pour le module board
board = MagicMock()
board.I2C = MockI2C
board.SCL = 5
board.SDA = 6


# Mock pour la classe BMP280_I2C
class MockBMP280_I2C:
    """Mock pour le capteur BMP280."""

    def __init__(self, i2c_bus, address=0x77):
        self._i2c = i2c_bus
        self._address = address
        # Valeurs réalistes pour un environnement intérieur
        self._temperature = 22.5  # °C
        self._pressure = 1013.25  # hPa
        self._altitude = 30.5  # mètres

    @property
    def temperature(self):
        """Retourne la température en °C."""
        return self._temperature

    @property
    def pressure(self):
        """Retourne la pression en hPa."""
        return self._pressure

    @property
    def altitude(self):
        """Retourne l'altitude en mètres."""
        return self._altitude

    # Attribut de classe pour la pression au niveau de la mer
    sea_level_pressure = 1013.25


# Module adafruit_bmp (alias pour compatibilité)
adafruit_bmp = MagicMock()
adafruit_bmp.BMP280_I2C = MockBMP280_I2C

# Module adafruit_bmp280 (nom correct du paquet)
adafruit_bmp280 = MagicMock()
adafruit_bmp280.Adafruit_BMP280_I2C = MockBMP280_I2C
adafruit_bmp280.BMP280_I2C = MockBMP280_I2C  # Alias pour compatibilité

# Module adafruit_blinka (module de compatibilité)
adafruit_blinka = MagicMock()
adafruit_blinka.__version__ = "8.0.0"
