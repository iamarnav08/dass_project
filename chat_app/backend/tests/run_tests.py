import unittest
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """Run all tests with proper error handling."""
    # Try to import the report module first
    try:
        from report_test_results import run_all_tests_with_report
        return run_all_tests_with_report()
    except ImportError:
        print("Test reporter module not found, falling back to standard test runner")
        return run_tests_standard()

def run_tests_standard():
    """Run all tests using the standard unittest discovery."""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    
    # First create the test suite
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    print(f"⚙️  Found {suite.countTestCases()} tests to run")
    
    start_time = time.time()
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Calculate elapsed time
    elapsed = time.time() - start_time
    
    # Print summary with colors
    print("\n" + "="*50)
    print(f"🔍 TEST SUMMARY (completed in {elapsed:.2f} seconds)")
    print("="*50)
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ FAILURES: {len(result.failures)}")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"  {i}. {test}")
    
    if result.errors:
        print(f"\n⚠️  ERRORS: {len(result.errors)}")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"  {i}. {test}")
    
    if result.skipped:
        print(f"\n⏩ SKIPPED: {len(result.skipped)}")
        for i, (test, reason) in enumerate(result.skipped, 1):
            print(f"  {i}. {test} - {reason}")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    # Return success if no failures or errors
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
