import PySimpleGUI as sg
import subprocess as sp
from cover_letter import CoverLetter

sg.theme("dark blue 3")

input_column = [
    [
        sg.Text("Cover Letter Type", size=(15, 1)),
        sg.Radio("Web", "RADIO-TYPE", default=True, key="-WEB-"),
        sg.Radio("New", "RADIO-TYPE", key="-NEW-")
    ],
    [
        sg.Text("File Format", size=(15, 1)),
        sg.Radio("Word", "RADIO-FORMAT", default=True, key="-WORD-"),
        sg.Radio("Text", "RADIO-FORMAT", key="-TEXT-")
    ],
    [sg.Text("Enter Date")],
    [
        sg.InputText(key="-DATE-", size=(34, 1)),
        sg.CalendarButton("Calendar", target="-DATE-")
    ],
    [sg.Text("Enter Company")],
    [sg.InputText(key="-COMPANY-")],
    [sg.Text("Enter Job Role Name")],
    [sg.InputText(key="-JOBNAME-")]
]

view_column = []

layout = [
    [
        sg.Column(input_column),
        sg.VSeparator(),
        sg.Column(view_column)
    ],
    [sg.Button("Create"), sg.Button("Cancel")]

]

window = sg.Window(title="Cover Letter Generator", layout=layout, margins=(200, 100))

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Cancel"):
        break
    elif event == "Create":
        if values["-WEB-"]:
            new_cover_letter = CoverLetter("web")
        else:
            new_cover_letter = CoverLetter("new")

        try:
            new_cover_letter.set_date(values["-DATE-"])
            new_cover_letter.set_job_role(values["-JOBNAME-"])
            new_cover_letter.set_company(values["-COMPANY-"])
            new_cover_letter.insert_data()

            if values["-WORD-"]:
                new_cover_letter.generate_word_doc()
            else:
                new_cover_letter.generate_text_doc()

            new_cover_letter.clean_up()
            sp.call(["open", "./cover_letter_outputs"])

        except Exception as e:
            print(e)
            sg.popup_error(f"An error occurred:\n {str(e)}")

window.close()
