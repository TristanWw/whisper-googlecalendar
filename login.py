from pathlib import Path
from playwright.sync_api import sync_playwright

state_file = Path("state/state.json")

#check if state exists
def state_exists():
    return state_file.exists()


# check if Session still works
def google_session_valid(p):
    try:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(storage_state="state/state.json")
        page = context.new_page()
        page.goto("https://calendar.google.com", wait_until="domcontentloaded")
        

        # if redirect to login page, means session expires
        #if "accounts.google.com" in page.url or "ServiceLogin" in page.url or "workspace.google.com" in page.url:
        return "calendar.google.com" in page.url:
    except:
        return False
    finally:
        if context:
            context.close()
        if browser:
            browser.close()


# manual login
def launch_manual_login_browser(p):
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
    )
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://accounts.google.com")

    # wait for user to close the window
    try:
        page.wait_for_timeout(99999999)
    except:
        state_file.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path="state/state.json")
        context.close()
        browser.close()



# ensure login session work
def ensure_google_session():
    """
    see if state exists and session works, if not then manual login
    """   
    with sync_playwright() as p:
        # if profile does not exist, need manual login
        if not state_exists():
            launch_manual_login_browser(p)
        # profile exists here, load profile, check if session still works
        while not google_session_valid(p):
            # if session expires, manual login until session works
            launch_manual_login_browser(p)
        
        print("we are here Tristan")