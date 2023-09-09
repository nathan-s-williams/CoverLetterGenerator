import PySimpleGUI as sg
import subprocess as sp
from datetime import datetime
from cover_letter import CoverLetter
from typing import List, Dict, Union, Tuple


# ********************************************************************
# --Helper Functions
# ********************************************************************

def register_field_data(
        cover_letter: CoverLetter,
        fields: List[str],
        value_list: Dict[str, Union[str, List[str], Tuple[str, ...]]]
) -> None:
    for field in fields:
        if field == "version":
            if value_list["-WEB-"]:
                cover_letter.set_version(CoverLetter.VERSION_TYPE_WEB)
            else:
                pass  # Need to add a version for "new" in CoverLetter class
        elif field == "date":
            cover_letter.set_date(value_list["-DATE-"])
        elif field == "job":
            cover_letter.set_job_role(value_list["-JOBNAME-"])
        elif field == "company":
            cover_letter.set_company(value_list["-COMPANY-"])


# ********************************************************************
# --GUI
# ********************************************************************
sg.theme("dark blue 3")

# ***************************
# --Input Fields
# ***************************
input_column = [
    [sg.Text("Enter Cover Letter Details")],
    [
        sg.Text("Cover Letter Type", size=(15, 1)),
        sg.Radio("Web", "RADIO-TYPE", key="-WEB-", enable_events=True),
        sg.Radio("New", "RADIO-TYPE", key="-NEW-", enable_events=True)
    ],
    [
        sg.Text("File Format", size=(15, 1)),
        sg.Radio("Word", "RADIO-FORMAT", key="-WORD-"),
        sg.Radio("Text", "RADIO-FORMAT", key="-TEXT-")
    ],
    [sg.Text("Enter Date")],
    [
        sg.InputText(key="-DATE-", size=(34, 1), enable_events=True),  # Enable event to change datetime to date
        sg.CalendarButton("Calendar", target="-DATE-")
    ],
    [sg.Text("Enter Company")],
    [sg.InputText(key="-COMPANY-")],
    [sg.Text("Enter Job Role Name")],
    [sg.InputText(key="-JOBNAME-")],
    [sg.Button("Create"), sg.Button("Cancel")]
]

# ***************************
# --Cover Letter Viewer
# ***************************
view_column = [
    [sg.Multiline("Cover Letter content...", size=(100, 50), key="-CONTENT-")]
]

# ***************************
# --Layout with both columns
# ***************************
layout = [
    [
        sg.Column(input_column),
        sg.Column(view_column)
    ]

]

# ***************************
# --Instantiate window and Cover Letter
# ***************************
window = sg.Window(title="Cover Letter Generator", layout=layout, margins=(100, 50))
new_cover_letter = CoverLetter()

# ********************************************************************
# --Event Loop
# ********************************************************************
while True:
    event, values = window.read()
    # ***************************
    # --Close Window
    # ***************************
    if event in (sg.WINDOW_CLOSED, "Cancel"):
        break
    # ***************************
    # --Create Cover Letter
    # ***************************
    elif event == "Create":
        fields_to_populate = ["date", "job", "company"]
        if new_cover_letter.get_version() is None or new_cover_letter.get_version() == "":
            fields_to_populate.append("version")
        register_field_data(new_cover_letter, fields_to_populate, values)

        try:
            new_cover_letter.insert_data()
            if values["-WORD-"]:
                new_cover_letter.generate_word_doc()
            else:
                new_cover_letter.generate_text_doc()

            new_cover_letter = CoverLetter()
            sp.call(["open", "./cover_letter_outputs"])

        except Exception as e:
            print(e)
            sg.popup_error(f"An error occurred:\n {str(e)}")
        finally:
            CoverLetter.clean_up()
    # ***************************
    # --Update Date Field
    # ***************************
    elif event == "-DATE-":
        if values["-DATE-"] != '':
            date_string = values["-DATE-"]
            date_format = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date()
            date_format = date_format.strftime("%B %d, %Y")
            window["-DATE-"].update(date_format)
    # ***************************
    # --Update View Content
    # ***************************
    elif values["-WEB-"]:
        register_field_data(new_cover_letter, ["version"], values)
        window["-CONTENT-"].update(new_cover_letter.get_cover_letter_content())
    elif values["-NEW-"]:
        register_field_data(new_cover_letter, ["version"], values)

window.close()
