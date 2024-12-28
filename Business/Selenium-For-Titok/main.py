from gologin import GoLogin
from playwright.sync_api import sync_playwright
import os
import shutil
import json
import time

# Cấu hình GoLogin
gl = GoLogin({
    "token": "YOUR_TOKEN",
    "profile_id": "YOUR_PROFILE",
})

def wait_for_element(page, selector, timeout=30000):
    try:
        page.wait_for_selector(selector, timeout=timeout)
        print(f"Element with selector '{selector}' is ready.")
        return page.query_selector(selector)
    except Exception as e:
        print(f"Error waiting for element '{selector}': {e}")
        return None


def clear_temp_folder(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Cleared temporary folder: {folder_path}")
    except Exception as e:
        print(f"Failed to clear temporary folder {folder_path}: {e}")

def enter_main_image(folder_url, page):
    files = [os.path.join(folder_url, f) for f in os.listdir(folder_url) if os.path.isfile(os.path.join(folder_url, f))]
    if not files:
        print("No files found in the specified folder.")
        return
    
    print(f"Found {len(files)} files in folder: {folder_url}")
    
    file_input = page.query_selector(".index__dndContainer--WQKEF input[type='file']") 
    if file_input:
        file_input.set_input_files(files)
        print(f"Main images uploaded from: {folder_url}")
    else:
        print(f"File input element not found for selector '{file_input_selector}'.")

def enter_option_image(folder_url, page):
    # Map file names to their full paths
    file_map = {
        os.path.basename(f): os.path.join(folder_url, f)
        for f in os.listdir(folder_url)
        if os.path.isfile(os.path.join(folder_url, f))
    }

    if not file_map:
        print("No files found in the specified folder.")
        return

    # Print the file map
    print(f"Found {len(file_map)} files in folder '{folder_url}':")
    for file_name, file_path in file_map.items():
        print(f"- {file_name}: {file_path}")

    # Parent container selector
    parent_selector = ".Property__Container-sc-16fbzyl-0.hYXwqd"
    parent_element = page.query_selector(parent_selector)

    if parent_element:
        # Select child divs
        div_selector = 'div[role="button"][tabindex="0"][aria-disabled="false"][aria-roledescription="sortable"]'
        child_divs = parent_element.query_selector_all(div_selector)

        print(f"Found {len(child_divs)} child divs to process.")
        for index, child_div in enumerate(child_divs):
            try:
                # Find the input element inside the child div
                input_selector = "input[data-id^='product.publish.sale_property.value.name.']"
                input_element = child_div.query_selector(input_selector)

                if input_element:
                    # Get the value of the input
                    input_value = input_element.get_attribute("value")
                    print(f"Child {index + 1}: Input value is '{input_value}'")

                    if input_value and f"{input_value}.jpeg" in file_map:
                        file_path = file_map[f"{input_value}.jpeg"]
                        print(f"File '{file_path}' matches input value '{input_value}'.")

                        # Find the file input element inside the child div
                        file_input_selector = "input[type='file']"
                        file_input_element = child_div.query_selector(file_input_selector)

                        if file_input_element:
                            file_input_element.set_input_files(file_path)
                            print(f"Set file '{file_path}' for child {index + 1}.")
                            time.sleep(1)
                        else:
                            print(f"File input not found in child {index + 1}.")
                    else:
                        print(f"No matching file found for input value '{input_value}' in child {index + 1}.")
                else:
                    print(f"No input element found in child {index + 1}.")
            except Exception as e:
                print(f"Error processing child {index + 1}: {e}")
    else:
        print(f"Parent element with selector '{parent_selector}' not found.")
        
def enter_name_product(input_content, page):
    input_selector = "input[data-id='product.publish.product_name']"
    input_element = wait_for_element(page, input_selector)
    if input_element:
        input_element.fill(input_content)
        print(f"Product name entered: {input_content}")
    else:
        print(f"Input element for product name not found with selector '{input_selector}'.")

def enter_desc_product(input_content, page):
    input_element = page.query_selector(".ProseMirror")
    if input_element:
        page.evaluate("(element) => element.scrollIntoView()", input_element)

        page.evaluate(
            """(args) => { args.element.innerHTML = args.value; }""",
            {"element": input_element, "value": input_content}
        )

        print(f"Input filled with: {input_content}")
    else:
        print("Input element with selector '.ProseMirror' not found.")

def click_element_with_event(page, selector):
    try:
        element = page.query_selector(selector)
        if element:
            # Dùng evaluate để mô phỏng sự kiện click
            page.evaluate(
                """(el) => {
                    const event = new MouseEvent("click", {
                        bubbles: true,
                        cancelable: true,
                        view: window,
                    });
                    el.dispatchEvent(event);
                    console.log("Element clicked successfully!");
                }""",
                element,
            )
            print("Element clicked successfully!")
        else:
            print("Element clear...")
    except Exception as e:
        print(f"An error occurred while clicking the element: {e}")

def clear_main_images(page):
    try:
        print("Starting to check and remove images...")

        while True:
            check_selector = "#main_image_item_0 > div > div > div.theme-arco-space.theme-arco-space-horizontal.theme-arco-space-align-center.theme-m4b-space.index__mask--Uk6PR > div:nth-child(3) > svg"
            element = page.query_selector(check_selector)
            if element:
                click_element_with_event(page, check_selector)
                time.sleep(1)
            else:
                print("Image element not found. Exiting loop.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

def clear_option_images(page):
    try:
        print("Starting to check and remove option images...")
        lastIndex = 9 
        parent_element = page.query_selector(".Property__Container-sc-16fbzyl-0.hYXwqd")
        if parent_element:
            div_selector = 'div[role="button"][tabindex="0"][aria-disabled="false"][aria-roledescription="sortable"]'
            child_divs = parent_element.query_selector_all(div_selector)
            lastIndex = len(child_divs) + 2
            print(lastIndex)
            
        for i in range(2, lastIndex):
            check_selector = f"#sale_properties > div:nth-child(1) > div.Property__Container-sc-16fbzyl-0.hYXwqd > div:nth-child(1) > div:nth-child({i}) > div > div.flex.flex-row.flex-grow-\\[1\\] > div.mr-12 > div > div > div > div.theme-arco-space.theme-arco-space-horizontal.theme-arco-space-align-center.theme-m4b-space.index__hoverButton--uegr0 > div:nth-child(2) > svg"
            element = page.query_selector(check_selector)
            
            if element:
                print(f"Found option image at index {i}, attempting to click...")
                try:
                    click_element_with_event(page, check_selector)
                except Exception as click_error:
                    print(f"Error clicking element at index {i}: {click_error}")
            else:
                print(f"No image found for selector at index {i}. Skipping...")
                continue

        print("Option image clearing completed.")

    except Exception as e:
        print(f"An error occurred while clearing option images: {e}")

def enter_sku(sku, page):
    batch_edit_button_selector = "button[data-id='product.publish.skus.batch_edit']"
    batch_edit_button = wait_for_element(page, batch_edit_button_selector)
    if batch_edit_button:
        batch_edit_button.click()
        print("Batch Edit button clicked successfully.")
        input_selector = "input[data-tid='m4b_input'][placeholder='Seller SKU']"
        input_element = wait_for_element(page, input_selector)
        if input_element:
            input_element.fill(sku)
            print(f"SKU entered: {sku}")
            done_button_selector = "#skus button.theme-arco-btn span:text-is('Apply')"
            done_button = wait_for_element(page, done_button_selector)
            if done_button:
                done_button.click()
                print("Apply button clicked.")
            else:
                print(f"Apply button not found with selector '{done_button_selector}'.")
    else:
        print(f"Batch Edit button not found with selector '{batch_edit_button_selector}'.")
            
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("Data loaded successfully!")
            return data
    except Exception as e:
        print(f"An error occurred while loading the JSON file: {e}")
        return []
      
      
def push_product(data, page, index):
    print("Starting push product " + str(index + 1))
    page.goto('https://seller-us.tiktok.com/product/create/1730367985084043325', wait_until="domcontentloaded", timeout=250000)
    try:
        print("Waiting for page to fully load...")
        page.wait_for_selector(".index__dndContainer--WQKEF", timeout=200000)
        print("Page loaded successfully.")
    except Exception as e:
        print(f"Page did not load properly or timeout occurred: {e}")
        return

    time.sleep(5)
    clear_main_images(page)
    enter_main_image(data['folder_path'], page)
    enter_name_product(data["name"], page)
    enter_desc_product(data["description"], page)
    clear_option_images(page)
    enter_option_image(data['folder_path'], page)
    enter_sku(data["sku"], page)

    print("Checking if any 'Uploading' elements exist before submission...")
    while True:
        uploading_elements = page.query_selector_all('div:has-text("Uploading")')
        if len(uploading_elements) == 0:
            print("No 'Uploading' elements found. Proceeding to submit.")
            break
        else:
            print(f"Found {len(uploading_elements)} 'Uploading' elements. Waiting...")
            time.sleep(1) 

    submit_element = page.query_selector('span:has-text("Submit for review")')
    if submit_element:
        submit_element.click()
        print("Clicked 'Submit for review'.")
    else:
        print("'Submit for review' button not found.")
        
    while True:
        checked = page.query_selector('span:has-text("Congratulations!")')
        if checked:
            print("List product " + str(index + 1) + " successfully...")
            break
        else: 
            print("wait submitting product...")
            time.sleep(1) 
        
          

def main():
    try:
        # Bắt đầu GoLogin
        temp_folder = "C:\\Users\\corsn\\AppData\\Local\\Temp"
        clear_temp_folder(temp_folder)
        print("Starting GoLogin...")
        debugger_address = gl.start()
        if not debugger_address.startswith("http"):
            debugger_address = f"http://{debugger_address}"
        print(f"Connected to GoLogin profile: {debugger_address}")

        # Sử dụng Playwright
        with sync_playwright() as p:
            # Kết nối đến GoLogin profile
            print("Connecting to browser...")
            browser = p.chromium.connect_over_cdp(debugger_address)
            context = browser.contexts[-1] if browser.contexts else browser.new_context()
            page = context.pages[-1] if context.pages else context.new_page()

            data = load_json_file("data.json")
            for index, item in enumerate(data):
                push_product(item, page, index)
           
            
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Stopping GoLogin profile and closing browser...")
        # try:
            # browser.close()
        # except Exception as close_error:
            # print(f"Error closing browser: {close_error}")
        # gl.stop()
        # print("Profile stopped.")

if __name__ == "__main__":
    main()
