import unittest, json
from utils import *

class TestCycleBasis(unittest.TestCase):

    def test_pairs(self):
        pair_data = get_pair_data()
        
        assert "pairs" in pair_data, "Pair data should be a dict with a key named 'pairs'"
        num_pairs = len(pair_data["pairs"])
        assert num_pairs==32, f"Pair data should have 32 currencies not {num_pairs}"

        

    def test_basis(self):
        basis_cycles=parse_rates()
        maxlen=0
        for c in basis_cycles:
            c_string = json.dumps(c)
            maxlen=max(maxlen, len(c))
            assert "XBT" in c, f"XBT not found in {c_string}"
        assert  maxlen == 3, f"Found a cycle with more than 3 currencies: {c_string}"

        assert len(basis_cycles)==17, "There should be 17 basis cycles in Luno."

    

    

if __name__ == '__main__':
    unittest.main()