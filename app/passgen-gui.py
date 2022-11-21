import dearpygui.dearpygui as dpg
import re
import secrets
import string


def generate_password(sender, data) -> None:
    alpha: str = ""
    remove: str = ""

    if dpg.get_value(item="Letters"):
        alpha += string.ascii_letters
    if dpg.get_value(item="Numbers"):
        alpha += string.digits
    if dpg.get_value(item="Symbols"):
        alpha += string.punctuation
        remove += "\"'`|"

    if alpha == "":
        dpg.set_value(item="Password", value="Invalid options.")
        return

    if not dpg.get_value(item="Similar"):
        remove += "B8G6I1l0OQDS5Z2"

    alpha = re.sub(f"[{remove}]", "", alpha)  # Remove unwanted characters

    password = "".join(
        secrets.choice(alpha) for _ in range(dpg.get_value(item="Length"))
    )
    print(password)

    dpg.set_value(item="Password", value=password)


dpg.create_context()
dpg.create_viewport(title="PassGen GUI", width=600, height=400)

with dpg.window(tag="Primary"):
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

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary", True)
dpg.start_dearpygui()
dpg.destroy_context()
