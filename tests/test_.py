from sound_effect import doorbell_ring
import unittest
from unittest.mock import patch, MagicMock

MockRPi = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
}

patcher = patch.dict("sys.modules", modules)
patcher.start()


class TestDoorBell(unittest.TestCase):
    
    def test_ring(self):
        doorbell_ring.main()
        
    def teardownModule():
        patcher.stop

if __name__ == '__main__':
    unittest.main()
