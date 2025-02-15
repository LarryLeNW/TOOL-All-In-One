from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://material.playwrightvn.com/02-xpath-product-page.html")
        
        for _ in range(2):
            page.click("button.add-to-cart[data-product-id='1']")
        
        for _ in range(3):
            page.click("button.add-to-cart[data-product-id='2']")
        
        page.click("button.add-to-cart[data-product-id='3']")
        
        page.screenshot(path="done-ls2.png")
        print("Products added to cart successfully!")
        
        input("press to close the browser...")

if __name__ == "__main__":
    main()
