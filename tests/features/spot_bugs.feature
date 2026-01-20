Feature: Spotting bugs in a an online user registration form
    Scenario Outline: Scenario for validating user form inputs
        Given the user navigates to the URL
        When the user enters <first_name>, <last_name>, <phone_number>, <country>, <email> and <password>
        And the user chooses to <click_checkbox> for I agree with the terms and conditions
        And the user clicks on the Register button
        Then the user gets <confirmation_message> with <registration_status> accompanied with user provided details


        Examples:
            | first_name | last_name | phone_number | country | email   | password | click_checkbox | confirmation_message | registration_status |
            | valid      | valid     | valid        | valid   | valid   | valid    | Yes            | valid                | success             |
            | invalid    | invalid   | invalid      | invalid | invalid | invalid  | No             | invalid              | failure             |
            | invalid    | invalid   | invalid      | invalid | invalid | invalid  | No             | valid                | success             |
