from playwright.sync_api import sync_playwright

def fill_registration_form(data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://material.playwrightvn.com/01-xpath-register-page.html")
        
        page.fill("#username", data["username"])
        page.fill("#email", data["email"])
        
        page.check(f"#{data['gender']}")
        
        for hobby in data["hobbies"]:
            page.check(f"#{hobby}")
        
        page.click(f"option[value='{data['category']}']")
        
        page.select_option("#country", data["country"])
        page.fill("#dob", data["dob"])
        page.fill("#bio", data["bio"])
        
        page.fill("#rating", str(data["rating"]))
        page.fill("#favcolor", data["favcolor"])
        
        if data["newsletter"]:
            page.check("#newsletter")
        
        if data["toggle_option"]:
            page.evaluate("document.getElementById('toggleOption').checked = true")
    
        page.get_by_role("button", name="Register").click()

        page.locator("#userTable").scroll_into_view_if_needed()
        page.screenshot(path="done-ls1.png")
        
        print("Form submitted successfully!")
        
        input("press to close the browser...")
        
if __name__ == "__main__":
    user_data = {
        "username": "lebatrinh",
        "email": "lebatrinh@example.com",
        "gender": "male",
        "hobbies": ["reading", "traveling"],
        "category": "art",
        "country": "canada",
        "dob": "2000-03-01",
        "bio": "Đây là tiểu sử thử nghiệm.",
        "rating": 10,
        "favcolor": "#80ff00",
        "newsletter": True,
        "toggle_option": True
    }
    
    fill_registration_form(user_data)
