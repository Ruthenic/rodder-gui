import PySimpleGUI as sg
import os,sys
sg.theme('DarkAmber')
raw_package_list=[]
package_names=[]
#layout = [[sg.Text('rodder packages')], [sg.InputText(), sg.Button('Search')]]
#line above has search, uncomment when i feel like adding it
layout = [[sg.Text('rodder packages')]]
tmp = os.listdir(os.getenv('HOME') + '/.config/rodder/repos/')
for i in tmp:
    if os.path.isdir(os.getenv('HOME') + '/.config/rodder/repos/' + i) == False and i != 'master-repo-list.txt':
        with open(os.getenv('HOME') + '/.config/rodder/repos/' + i) as f:
            for line in f:
                raw_package_list.append(line.strip() + ';' + i.split('.')[0])
for i in raw_package_list:
    layout.append([sg.Text(i), sg.Button('Install ' + i.split(';')[0])])
    package_names.append(i.split(';')[0])
# Create the Window
window = sg.Window('rodder-gui', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED : # if user closes window or clicks cancel
        break
    try:
        print('You entered ', values[0])
    except:
        pass
    for i in package_names:
        if event == 'Install ' + i:
            print("User wants to " + str(event))
            rodder_file = open(os.getenv('HOME') + '/.local/rodder/rodder').read()
            sys.argv = ['rodder', 'install', i]
            exec(rodder_file)
window.close()
