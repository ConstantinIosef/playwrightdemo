import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.youtube.com/")
    page.get_by_role("dialog", name="Before you continue to YouTube").click()
    page.get_by_role("button", name="Accept the use of cookies and").click()
    page.get_by_role("link", name="Sign in").click()
    page.get_by_role("textbox", name="Email or phone").click()
    page.get_by_role("textbox", name="Email or phone").fill("costiplaywrightdemo@gmail.com")
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Enter your password").click()
    page.get_by_role("textbox", name="Enter your password").fill("Tester123!")
    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Not now").click()
    page.get_by_role("button", name="Account menu").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Google Account").click()
    page1 = page1_info.value
