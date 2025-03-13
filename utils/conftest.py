import pytest
import os
from datetime import datetime
from utils.testrail_integration import TestRailReporter
from playwright.sync_api import sync_playwright

# Status IDs in TestRail:
# 1 = Passed
# 2 = Blocked
# 3 = Untested
# 4 = Retest
# 5 = Failed

@pytest.fixture(scope="session")
def testrail():
    """Fixture to handle TestRail integration"""
    reporter = TestRailReporter()
    
    # Create a test run with timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_id = reporter.create_test_run(f"Playwright Run - {timestamp}", 
                                     "Automated test run from Playwright portfolio demo")
    
    print(f"Created TestRail run with ID: {run_id}")
    
    yield reporter

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    
    # Get the test case name
    test_fn = item.function.__name__
    test_description = item.function.__doc__ or test_fn
    
    # If the test was setup, call, or teardown and has the testrail fixture
    if rep.when == "call" and 'testrail' in item.fixturenames:
        testrail = item.funcargs['testrail']
        
        # Get or create a TestRail test case
        case_id = testrail.get_or_create_test_case(test_description)
        
        # Map pytest result to TestRail status
        status_id = 1 if rep.passed else 5  # 1 = Passed, 5 = Failed
        
        # Add test result with elapsed time
        elapsed = f"{rep.duration}s" if hasattr(rep, 'duration') else "0s"
        comment = f"Automated test result from Playwright. {'Passed' if rep.passed else 'Failed'}"
        if not rep.passed:
            if hasattr(rep, 'longrepr'):
                comment += f"\n\nError: {rep.longrepr}"
        
        testrail.add_test_result(case_id, status_id, comment, elapsed)
