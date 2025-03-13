import re
import random
from playwright.sync_api import Page, expect

def test_user_registration(page: Page, testrail):
    """Verify user can successfully create an account"""
    # Generate random email to avoid duplicate registration issues
    random_email = f"tester123+{random.randint(1, 1000000)}@test.com"
    
    # Navigate to homepage
    page.goto("https://automationexercise.com/")
    
    # Accept cookies if present
    try:
        page.get_by_role("button", name="Consent").click()
    except:
        pass  # If consent button is not present, continue
    
    # Navigate to signup page
    page.get_by_role("link", name=" Signup / Login").click()
    
    # Fill signup form
    page.get_by_role("textbox", name="Name").fill("tester")
    page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(random_email)
    page.get_by_role("button", name="Signup").click()
    
    # Fill detailed registration form
    page.get_by_role("radio", name="Mr.").check()
    page.get_by_role("textbox", name="Password *").fill("Tester123!")
    page.locator("#days").select_option("1")
    page.locator("#months").select_option("1")
    page.locator("#years").select_option("1990")
    
    # Personal information
    page.get_by_role("textbox", name="First name *").fill("fname")
    page.get_by_role("textbox", name="Last name *").fill("lname")
    page.get_by_role("textbox", name="Company", exact=True).fill("testcompanysrl")
    
    # Address information
    page.get_by_role("textbox", name="Address * (Street address, P.").fill("Street 12, Testcompanysrl")
    page.get_by_label("Country *").select_option("United States")
    page.get_by_role("textbox", name="State *").fill("Ohio")
    page.get_by_role("textbox", name="City * Zipcode *").fill("Cleveland")
    page.locator("#zipcode").fill("44102")
    page.get_by_role("textbox", name="Mobile Number *").fill("570-805-1784")
    
    # Create account and verify
    page.get_by_role("button", name="Create Account").click()
    
    # Verify account creation was successful
    expect(page.get_by_text("Account Created!")).to_be_visible()
