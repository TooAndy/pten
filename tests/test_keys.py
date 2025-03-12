from .conftest import use_real_keys
from pten.keys import Keys
import pytest


pytestmark = pytest.mark.skipif(use_real_keys, reason="Skipping when using real keys")


def test_key_path_not_exist():
    keys = Keys("not_exist.ini")
    with pytest.raises(FileNotFoundError):
        keys.get_bot_weebhook_key()


@pytest.mark.parametrize(
    "section,option,expected",
    [
        ("bot", "webhook_key", "7a276454-52a4-43d7-a252-0ddb8635e80c"),
        ("wwapi", "corpid", "wwdb63ff5ae01cd4b4"),
    ],
)
def test_get_key(key_filepath_example, section, option, expected):
    keys = Keys(key_filepath_example)
    assert keys.get_key(section, option) == expected


@pytest.mark.parametrize(
    "section,options,expected",
    [
        (
            "proxies",
            ["http", "https"],
            {
                "http": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
                "https": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
            },
        ),
        (
            "app",
            ["aes_key", "app_token"],
            {
                "aes_key": "9z1Cj9cSd7WtEV3hOWo5iMQlFkSP9Td1ejzsV9WhCmO",
                "app_token": "zJdPmXg8E4J1mMdnzP8d",
            },
        ),
    ],
)
def test_get_keys(key_filepath_example, section, options, expected):
    keys = Keys(key_filepath_example)
    assert keys.get_keys(section, options) == expected


def test_get_debug_mode(key_filepath_example):
    keys = Keys(key_filepath_example)
    assert keys.get_debug_mode() is False

    keys_no_debug_mode = Keys("pten_keys_example_min.ini")
    assert keys_no_debug_mode.get_debug_mode() is False


def test_proxies(key_filepath_example):
    keys = Keys(key_filepath_example)
    proxies_expected = {
        "http": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
        "https": "http://xxx:xxx@xxx.xxx.xxx.xxx:8888",
    }
    assert keys.get_proxies() == proxies_expected

    keys_no_proxies = Keys("pten_keys_example_min.ini")
    assert keys_no_proxies.get_proxies() is None


def test_bot_weebhook_key(key_filepath_example):
    keys = Keys(key_filepath_example)
    assert keys.get_bot_weebhook_key() == "7a276454-52a4-43d7-a252-0ddb8635e80c"
