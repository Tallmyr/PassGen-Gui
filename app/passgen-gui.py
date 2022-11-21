import re
import secrets
import string

import dearpygui.dearpygui as dpg
import pyperclip


def generate_password() -> None:
    """Generate Password and update GUI"""

    # Get Values from DPG
    letters = dpg.get_value(item="Letters")
    numbers = dpg.get_value(item="Numbers")
    symbols = dpg.get_value(item="Symbols")
    similar = dpg.get_value(item="Similar")
    length = dpg.get_value(item="Length")

    # Test for valid selections, or return early
    if not letters and not numbers and not symbols:
        dpg.set_value(item="Password", value="Invalid selection.")
        return

    # Set some empty strings
    alpha: str = ""
    remove: str = ""

    # Test Checkbox Values
    if letters:
        alpha += string.ascii_letters
    if numbers:
        alpha += string.digits
    if symbols:
        alpha += string.punctuation
        remove += "\"'`|"

    # Add similar letters to Alpha removal
    if not similar:
        remove += "B8G6I1l0OQDS5Z2"

    # Remove unwanted characters
    alpha = re.sub(f"[{remove}]", "", alpha)

    # Create Password
    password = "".join(secrets.choice(alpha) for _ in range(length))

    # Send password to password field
    dpg.set_value(item="Password", value=password)
    return


def lock_if_invalid():
    letters = dpg.get_value(item="Letters")
    numbers = dpg.get_value(item="Numbers")
    symbols = dpg.get_value(item="Symbols")

    if not letters and not numbers and not symbols:
        dpg.show_item(item="Gen_warning")
        dpg.disable_item(item="Generate")
    else:
        dpg.hide_item(item="Gen_warning")
        dpg.enable_item(item="Generate")


def check_short_password(sender, app_data):
    if sender != "Length":
        return

    if app_data <= 7:
        dpg.show_item(item="length_warning")
    else:
        dpg.hide_item(item="length_warning")


def copy_to_clipboard() -> None:
    pyperclip.copy(dpg.get_value(item="Password"))


def main() -> None:
    """Setup DPG and Design UI"""

    # Setup Context
    dpg.create_context()

    # Main Window
    with dpg.window(tag="Primary"):
        dpg.add_text("Password Generating software.")

        dpg.add_spacer(height=20)
        dpg.add_text("Please choose your settings:")
        dpg.add_checkbox(
            label="Letters", default_value=True, tag="Letters", callback=lock_if_invalid
        )
        dpg.add_checkbox(
            label="Numbers", default_value=True, tag="Numbers", callback=lock_if_invalid
        )
        dpg.add_checkbox(
            label="Symbols", default_value=True, tag="Symbols", callback=lock_if_invalid
        )
        dpg.add_text(
            "Invalid Selection, please select one or more character types",
            tag="Gen_warning",
            color=[255, 0, 0],
            show=False,
        )

        dpg.add_spacer(height=10)
        dpg.add_text("Allow similar Letters and symbols? (B/8, G/6, I/1 etc)")
        dpg.add_checkbox(label="Similar", default_value=False, tag="Similar")

        dpg.add_spacer(height=10)
        dpg.add_slider_int(
            label="Password Length",
            min_value=1,
            max_value=50,
            default_value=12,
            tag="Length",
            callback=check_short_password
        )
        dpg.add_text(
            "This is a short password. Are you sure you wish to do this?",
            tag="length_warning",
            show=False,
            color=[255, 0, 0]
        )
        dpg.add_button(
            label="Generate Password", callback=generate_password, tag="Generate"
        )
        dpg.add_spacer(height=20)
        dpg.add_text("Your new password:")
        dpg.add_input_text(tag="Password")
        dpg.add_button(label="Copy to Clipboard", callback=copy_to_clipboard)

    # Display Everything
    dpg.create_viewport(title="PassGen GUI", width=550, height=500)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
