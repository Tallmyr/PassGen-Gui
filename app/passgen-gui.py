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


def copy_to_clipboard() -> None:
    pyperclip.copy(dpg.get_value(item="Password"))


def main() -> None:
    """Setup DPG and Design UI"""

    # Setup Context
    dpg.create_context()

    # Set Font
    with dpg.font_registry():
        default_font = dpg.add_font(
            "app/resources/Caskaydia Cove Nerd Font Complete Windows Compatible Regular.otf",
            15,
        )

    # Main Window
    with dpg.window(tag="Primary"):
        dpg.bind_font(default_font)

        dpg.add_text("Password Generating software.")

        dpg.add_spacer(height=20)
        dpg.add_text("Please choose your settings:")
        dpg.add_checkbox(label="Letters", default_value=True, tag="Letters")
        dpg.add_checkbox(label="Numbers", default_value=True, tag="Numbers")
        dpg.add_checkbox(label="Symbols", default_value=True, tag="Symbols")

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
        )
        dpg.add_button(label="Generate Password", callback=generate_password)
        dpg.add_spacer(height=20)
        dpg.add_text("Your new password:")
        dpg.add_input_text(tag="Password")
        dpg.add_button(label="Copy to Clipboard", callback=copy_to_clipboard)

    # Display Everything
    dpg.create_viewport(title="PassGen GUI", width=550, height=430)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
