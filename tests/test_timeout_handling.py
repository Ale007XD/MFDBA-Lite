import unittest
from unittest.mock import patch

from mfdballm.providers.openrouter import OpenRouterProvider
from mfdballm.exceptions import ProviderTimeoutError


class TimeoutTest(unittest.TestCase):

    @patch("mfdballm.providers.openrouter.requests.post")
    def test_timeout(self, mock_post):
        mock_post.side_effect = Exception("timeout simulation")

        provider = OpenRouterProvider()
        with self.assertRaises(Exception):
            provider.chat([{"role": "user", "content": "hi"}])


if __name__ == "__main__":
    unittest.main()
