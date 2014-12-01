import os

secret_test_api_key = os.getenv("MANGO_SECRET_TEST_KEY", None)
public_test_api_key = os.getenv("MANGO_PUBLIC_TEST_KEY", None)

if not secret_test_api_key or not public_test_api_key:
    raise Exception("A secret and public API key from test environment is needed to run the tests. Set the environment variables MANGO_SECRET_TEST_KEY/MANGO_PUBLIC_TEST_KEY with you API key to continue.")

if "live" in secret_test_api_key or "live" in public_test_api_key:
    raise Exception("You should never use a live API keys for tests. Use a key from the test environment.")