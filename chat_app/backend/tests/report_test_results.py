import unittest
import sys
import os
import time
import importlib
from collections import defaultdict
import traceback
from termcolor import colored

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def discover_test_modules():
    """Discover all test modules in the current directory."""
    test_files = []
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.startswith('test_') and filename.endswith('.py'):
            module_name = filename[:-3]  # Remove .py extension
            test_files.append(module_name)
    return test_files

def run_test_module(module_name):
    """Run tests from a specific module and return the results."""
    try:
        # Import the module
        module = importlib.import_module(module_name)
        
        # Create a test suite from the module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        # Run the tests with a result collector
        result = unittest.TestResult()
        start_time = time.time()
        suite.run(result)
        elapsed_time = time.time() - start_time
        
        return {
            'module': module_name,
            'total': result.testsRun,
            'failures': [(test.id(), err) for test, err in result.failures],
            'errors': [(test.id(), err) for test, err in result.errors],
            'skipped': [(test.id(), reason) for test, reason in result.skipped],
            'success': result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
            'elapsed_time': elapsed_time
        }
    except Exception as e:
        return {
            'module': module_name,
            'total': 0,
            'failures': [],
            'errors': [('module_import', traceback.format_exc())],
            'skipped': [],
            'success': 0,
            'elapsed_time': 0
        }

def get_test_method_name(test_id):
    """Extract the test method name from test ID for cleaner display."""
    parts = test_id.split('.')
    if len(parts) >= 3:
        class_name = parts[-2]
        method_name = parts[-1]
        return f"{class_name}.{method_name}"
    return test_id

def print_results_table(results):
    """Print a formatted table of results."""
    # Calculate column widths
    module_width = max(len(result['module']) for result in results) + 2
    total_width = 7  # "TOTAL" header length with padding
    success_width = 9  # "SUCCEEDED" header length with padding
    failed_width = 7  # "FAILED" header length with padding
    error_width = 7  # "ERRORS" header length with padding
    skipped_width = 9  # "SKIPPED" header length with padding
    time_width = 9  # "TIME (s)" header length with padding
    
    # Print header
    header = (
        f"{'MODULE':{module_width}} | "
        f"{'TOTAL':{total_width}} | "
        f"{'SUCCEEDED':{success_width}} | "
        f"{'FAILED':{failed_width}} | "
        f"{'ERRORS':{error_width}} | "
        f"{'SKIPPED':{skipped_width}} | "
        f"{'TIME (s)':{time_width}}"
    )
    print("\n" + "=" * len(header))
    print(colored(header, 'cyan', attrs=['bold']))
    print("=" * len(header))
    
    # Print each module's results
    all_totals = defaultdict(int)
    for result in results:
        module_name = result['module'].replace('test_', '')
        
        # Track totals
        all_totals['total'] += result['total']
        all_totals['success'] += result['success']
        all_totals['failures'] += len(result['failures'])
        all_totals['errors'] += len(result['errors'])
        all_totals['skipped'] += len(result['skipped'])
        
        # Print row with color coding based on success
        status_color = 'green' if len(result['failures']) == 0 and len(result['errors']) == 0 else 'red'
        
        print(
            f"{module_name:{module_width}} | "
            f"{result['total']:{total_width}} | "
            f"{colored(str(result['success']), 'green'):{success_width}} | "
            f"{colored(str(len(result['failures'])), 'red' if result['failures'] else 'white'):{failed_width}} | "
            f"{colored(str(len(result['errors'])), 'red' if result['errors'] else 'white'):{error_width}} | "
            f"{colored(str(len(result['skipped'])), 'yellow' if result['skipped'] else 'white'):{skipped_width}} | "
            f"{result['elapsed_time']:.2f}{' '*(time_width-5)}"
        )
    
    # Print footer with totals
    print("-" * len(header))
    print(
        f"{'TOTAL':{module_width}} | "
        f"{all_totals['total']:{total_width}} | "
        f"{colored(str(all_totals['success']), 'green'):{success_width}} | "
        f"{colored(str(all_totals['failures']), 'red' if all_totals['failures'] else 'white'):{failed_width}} | "
        f"{colored(str(all_totals['errors']), 'red' if all_totals['errors'] else 'white'):{error_width}} | "
        f"{colored(str(all_totals['skipped']), 'yellow' if all_totals['skipped'] else 'white'):{skipped_width}} | "
        f"{'':{time_width}}"
    )
    print("=" * len(header))
    
    # Print overall summary
    success_rate = (all_totals['success'] / all_totals['total'] * 100) if all_totals['total'] > 0 else 0
    success_message = f"SUCCESS RATE: {success_rate:.1f}% ({all_totals['success']}/{all_totals['total']})"
    
    if all_totals['failures'] == 0 and all_totals['errors'] == 0:
        print(colored("\n✅ " + success_message, 'green', attrs=['bold']))
    else:
        print(colored("\n❌ " + success_message, 'red', attrs=['bold']))
        print(colored(f"   FAILURES: {all_totals['failures']}, ERRORS: {all_totals['errors']}", 'red'))

def print_detailed_results(results):
    """Print detailed results for failed and error tests."""
    has_failures_or_errors = any(
        len(result['failures']) > 0 or len(result['errors']) > 0 
        for result in results
    )
    
    if not has_failures_or_errors:
        return
    
    print("\n" + "=" * 80)
    print(colored("DETAILED FAILURE AND ERROR INFORMATION", 'white', attrs=['bold']))
    print("=" * 80)
    
    for result in results:
        module_name = result['module'].replace('test_', '')
        
        # Process failures
        if result['failures']:
            print(f"\n{colored('FAILURES', 'red', attrs=['bold'])} in {colored(module_name, 'cyan')}:")
            for test_id, failure in result['failures']:
                test_name = get_test_method_name(test_id)
                print(f"  • {colored(test_name, 'yellow')}")
                # Print just the first few lines of the failure traceback
                traceback_lines = failure.split("\n")
                # Show the assertion error line
                for line in traceback_lines:
                    if "AssertionError" in line:
                        print(f"    {colored(line.strip(), 'red')}")
                        break
        
        # Process errors
        if result['errors']:
            print(f"\n{colored('ERRORS', 'red', attrs=['bold'])} in {colored(module_name, 'cyan')}:")
            for test_id, error in result['errors']:
                test_name = get_test_method_name(test_id)
                print(f"  • {colored(test_name, 'yellow')}")
                # Print just the error type and message
                traceback_lines = error.split("\n")
                # Find the last exception line
                for line in reversed(traceback_lines):
                    if line.startswith("Exception") or "Error:" in line:
                        print(f"    {colored(line.strip(), 'red')}")
                        break

def run_all_tests_with_report():
    """Run all tests and generate a nice report."""
    print(colored("\n📋 RUNNING ALL TESTS", 'cyan', attrs=['bold']))
    print(colored("==================", 'cyan'))
    
    # Discover test modules
    test_modules = discover_test_modules()
    test_modules.sort()  # Sort modules alphabetically
    
    # Run each module's tests
    results = []
    overall_start_time = time.time()
    
    for i, module in enumerate(test_modules, 1):
        print(f"Running {i}/{len(test_modules)}: {module}...", end="\r")
        sys.stdout.flush()
        result = run_test_module(module)
        results.append(result)
    
    overall_elapsed_time = time.time() - overall_start_time
    print(" " * 80, end="\r")  # Clear the status line
    
    # Print results table
    print_results_table(results)
    
    # Print detailed information for failed tests
    print_detailed_results(results)
    
    # Print overall timing
    print(f"\nTotal test execution time: {overall_elapsed_time:.2f} seconds\n")
    
    # Determine exit code based on whether all tests passed
    all_tests_passed = all(
        len(result['failures']) == 0 and len(result['errors']) == 0 
        for result in results
    )
    
    return all_tests_passed

if __name__ == '__main__':
    # Try to install termcolor if not available
    try:
        import termcolor
    except ImportError:
        print("Installing termcolor package for colored output...")
        os.system(f"{sys.executable} -m pip install termcolor")
        try:
            import termcolor
        except ImportError:
            # Define fallback colored function if termcolor can't be installed
            def colored(text, *args, **kwargs):
                return text
    
    success = run_all_tests_with_report()
    sys.exit(0 if success else 1)
