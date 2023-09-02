import PySimpleGUI as sg

sg.theme("dark blue 3")

input_column = [
    [sg.Text("Cover Letter Type")],
    [sg.Radio("Web", "RADIO-TYPE", default=True),
     sg.Radio("New", "RADIO-TYPE")],
    [sg.Text("File Format")],
    [sg.Radio("Word", "RADIO-FORMAT", default=True),
     sg.Radio("Text", "RADIO-FORMAT")],
    [sg.Text("Enter Date")],
    [sg.InputText(key="-DATE-", size=(35, 1)), sg.CalendarButton("Calendar", target="-DATE-")],
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
    ]

]

window = sg.Window(title="Cover Letter Generator", layout=layout, margins=(200, 100))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()
