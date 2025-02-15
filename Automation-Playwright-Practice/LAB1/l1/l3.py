from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://material.playwrightvn.com/03-xpath-todo-list.html")
        
        for i in range(100):
            page.fill("#new-task","Todo " + str(i + 1))
            page.click("button#add-task")
          
        page.on("dialog", lambda dialog: dialog.accept()) 
        
        for i in range(1, 101, 2):
            todo_selector = f"li:has-text('Todo {i}') button"
            page.click(todo_selector)    
        
        page.screenshot(path="done-ls3.png")
        input("press to close the browser...")

if __name__ == "__main__":
    main()
