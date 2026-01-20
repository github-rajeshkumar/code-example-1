from pytest_bdd import given, when, then, parsers
from playwright.sync_api import expect

TEST_DATA = {
    "valid": {
        "first_name": "Rajesh",
        "last_name": "Kumar",
        "phone_number": "0412345678",
        "country": "Australia",
        "email": "rajesh.kumar@example.com",
        "password": "Welcome@123"
    },

    "invalid": {
        "first_name": "123@@",
        "last_name": "",
        "phone_number": "abc",
        "country": "Albania",
        "email": "wrong-email",
        "password": "1"
    }
}

@given("the user navigates to the URL")
def navigate_to_url(page):
    page.goto("/")
    page.wait_for_load_state("networkidle")
    page.click("a[id='bugs-form']")




@when(parsers.parse(
    "the user enters {first_name}, {last_name}, {phone_number}, {country}, {email} and {password}"
))
def enter_details(page, first_name, last_name, phone_number, country, email, password):

    fn  = TEST_DATA[first_name]["first_name"]
    ln  = TEST_DATA[last_name]["last_name"]
    ph  = TEST_DATA[phone_number]["phone_number"]
    ct  = TEST_DATA[country]["country"]
    em  = TEST_DATA[email]["email"]
    pw  = TEST_DATA[password]["password"]

    page.fill("input[id='firstName']", fn)
    page.fill("input[id='lastName']", ln)
    page.fill("input[id='phone']", ph)

    expect(page.locator("#countries_dropdown_menu")).to_have_value("Select a country...")
    page.locator("#countries_dropdown_menu").select_option(ct)
    dropdown = page.locator("#countries_dropdown_menu")
    current = dropdown.input_value()
    if current.strip() == "Select a country...":
        dropdown.select_option(label=ct)
    else:
        print(f"Country already selected: {current}")

    dropdown.press("Enter")    
    page.wait_for_load_state("networkidle")
    page.fill("input[id='emailAddress']", em)
    page.fill("input[id='password']", pw)

        
    

@when(parsers.parse(
    "the user chooses to {click_checkbox} for I agree with the terms and conditions"
))
def choose_terms_checkbox(page, click_checkbox):
    checkbox = page.locator("#exampleCheck1")

    if checkbox.is_disabled():
        print("Checkbox is disabled – skipping interaction")
        return

    if click_checkbox.lower() == "yes":
        checkbox.check()
    else:
        checkbox.uncheck()

@when("the user clicks on the Register button")
def click_register_button(page):
    page.click("button[id='registerBtn']")

@then(parsers.parse(
    "the user gets {confirmation_message} with {registration_status} accompanied with user provided details"
))
def verify_registration_result(page, confirmation_message, registration_status):

    page.wait_for_selector("#result, .alert, .message", timeout=5000)

    result_text = page.inner_text("#result, .alert, .message")

    print("ALERT TEXT:", result_text)

    valid_confirmation_message = "Successfully registered the following information"
    
    assert valid_confirmation_message.lower() in result_text.lower()


    fields = {
        "First Name":  "#resultFn",
        "Last Name":   "#resultLn",
        "Phone Number":"#resultPhone",
        "Country":     "#country",
        "Email":       "#resultEmail"
    }


    captured_values = {}

    for field_name, selector in fields.items():
        value = page.locator(selector).inner_text().strip()
        captured_values[field_name] = value
        print(f"{field_name}: {value}")

    
    for name, value in captured_values.items():
        assert value, f"{name} is empty on result page"