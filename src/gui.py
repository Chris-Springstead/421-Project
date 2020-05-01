import PySimpleGUI as sg
import hashtagClassifier as hashTClass

sg.theme('Dark Blue 3')	# Add a touch of color
# All the stuff inside your window.
tab2_layout = [ 
            [sg.Input(key='-IN2-', do_not_clear=True)] ,
            [sg.Button('Label Tweet')] ,
            [sg.Output(key="-OUTPUT2-" , size=(70,27))]]


layout = [[sg.TabGroup([[sg.Tab('Label', tab2_layout)]])],    
          [sg.Button('Read')]]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):	# if user closes window or clicks cancel
        break
    if event  == "Label Tweet":
        userInput = values['-IN2-']
        window["-OUTPUT2-"].update(hashTClass.driver(userInput))

window.close()