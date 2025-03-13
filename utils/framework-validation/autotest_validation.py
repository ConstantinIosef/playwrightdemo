import re
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page, testrail):
    """Verify that the automation exercise homepage loads correctly"""
    # Navigate to the homepage
    page.goto("https://automationexercise.com/")
    
    # Verify that the homepage loaded correctly
    expect(page).to_have_title(re.compile("Automation Exercise"))
    
    # Verify that key elements are visible
    expect(page.locator(".features_items")).to_be_visible()
    expect(page.locator(".navbar-nav")).to_be_visible()

def test_product_search(page: Page, testrail):
    """Verify product search functionality"""
    # Navigate to the homepage
    page.goto("https://automationexercise.com/")
    
    # Search for a product
    page.fill('#search_product', 'tshirt')
    page.click('#submit_search')
    
    # Verify search results
    expect(page.locator('.features_items')).to_be_visible()
    expect(page.locator('h2.title')).to_contain_text('Searched Products')

def test_add_to_cart(page: Page, testrail):
    """Verify add to cart functionality"""
    # Navigate to the products page
    page.goto("https://automationexercise.com/products")
    
    # Hover over the first product to reveal the "Add to cart" button
    page.hover('.product-image-wrapper:first-child')
    
    # Click "Add to cart" button
    page.locator('.product-image-wrapper:first-child a.add-to-cart').click()
    
    # Click "Continue Shopping" button on the modal
    page.locator('button.btn-success').click()
    
    # View cart
    page.click('a[href="/view_cart"]')
    
    # Verify the product is in the cart
    expect(page.locator('#cart_info')).to_be_visible()
    expect(page.locator('.cart_description')).to_be_visible()
