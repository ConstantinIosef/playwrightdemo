import os
from testrail_api import TestRailAPI
from datetime import datetime

class TestRailReporter:
    def __init__(self):
        # Get TestRail credentials from environment variables for security
        # You'll need to set these environment variables or replace with your actual values
        self.testrail_url = os.environ.get('TESTRAIL_URL', 'https://yourinstance.testrail.io')
        self.testrail_email = os.environ.get('TESTRAIL_EMAIL', 'your_email@example.com')
        self.testrail_password = os.environ.get('TESTRAIL_PASSWORD', 'your_api_key')
        self.project_id = os.environ.get('TESTRAIL_PROJECT_ID', '1')
        self.suite_id = os.environ.get('TESTRAIL_SUITE_ID', '1')
        self.run_id = None
        
        # Initialize TestRail API client
        self.client = TestRailAPI(self.testrail_url, self.testrail_email, self.testrail_password)
    
    def create_test_run(self, name=None, description="Run created by Playwright automation"):
        """Create a new test run in TestRail"""
        if name is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            name = f"Playwright Run - {timestamp}"
            
        response = self.client.runs.add_run(
            project_id=self.project_id,
            suite_id=self.suite_id,
            name=name,
            description=description
        )
        self.run_id = response['id']
        return self.run_id
    
    def get_or_create_test_case(self, title, section_id=None):
        """Get an existing test case or create a new one if it doesn't exist"""
        # Search for the test case by title
        cases = self.client.cases.get_cases(project_id=self.project_id, suite_id=self.suite_id)
        for case in cases:
            if case['title'] == title:
                return case['id']
        
        # Create a new test case if not found
        if section_id is None:
            # Get the first section if none is specified
            sections = self.client.sections.get_sections(project_id=self.project_id, suite_id=self.suite_id)
            if sections:
                section_id = sections[0]['id']
            else:
                # Create a default section if none exists
                section = self.client.sections.add_section(
                    project_id=self.project_id, 
                    suite_id=self.suite_id, 
                    name="Automated Tests"
                )
                section_id = section['id']
        
        # Create new test case
        case = self.client.cases.add_case(
            section_id=section_id,
            title=title,
            type_id=1,  # 1 for Automated test
            priority_id=2,  # 2 for Medium priority
            estimate="5m",
            refs=""
        )
        return case['id']
    
    def add_test_result(self, case_id, status_id, comment="", elapsed="", **kwargs):
        """Add a test result to the current test run"""
        if not self.run_id:
            self.create_test_run()
        
        result = {
            "status_id": status_id,
            "comment": comment,
            "elapsed": elapsed,
            **kwargs
        }
        
        return self.client.results.add_result_for_case(run_id=self.run_id, case_id=case_id, **result)
