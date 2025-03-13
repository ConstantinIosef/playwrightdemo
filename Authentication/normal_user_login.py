from playwright.sync_api import Page, expect

def test_login_with_valid_credentials(page: Page, testrail):
    """Verify user can login with valid credentials"""
    # Navigate to homepage
    page.goto("https://automationexercise.com/")
   
    # Accept cookies if present
    try:
        page.get_by_role("button", name="Consent").click()
    except:
        pass
   
    # Navigate to login page
    page.get_by_role("link", name=" Signup / Login").click()
   
    # Use an existing account
    page.get_by_placeholder("Email Address", exact=True).fill("tester123+testautomationplaywrightdemo@test.com")
    page.get_by_placeholder("Password").fill("Tester123!")
    page.get_by_role("button", name="Login").click()
   
    # Verify successful login by checking if "Logged in as" text is visible
    expect(page.get_by_text("Logged in as tester")).to_be_visible()
    
    # Also verify the Logout button is visible
    expect(page.get_by_role("link", name=" Logout")).to_be_visible()
