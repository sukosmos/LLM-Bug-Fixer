def run_tests(test_directory):
    import unittest
    import os

    # Discover and run tests in the specified directory
    loader = unittest.TestLoader()
    suite = loader.discover(test_directory)

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Collect results
    test_results = {
        'tests_run': result.testsRun,
        'errors': len(result.errors),
        'failures': len(result.failures),
        'was_successful': result.wasSuccessful()
    }

    return test_results