import PySimpleGUI as sg
import os,sys,time
sg.theme('DarkBlack1')
raw_package_list=[]
package_names=[]
layout = [[sg.Text('rodder packages')], [sg.InputText(), sg.Button('Search')]]
#line above has search, uncomment when i feel like adding it
#layout = [[sg.Text('rodder packages')]] #why did i even put this here
tmp = os.listdir(os.getenv('HOME') + '/.config/rodder/repos/')
for i in tmp:
    if os.path.isdir(os.getenv('HOME') + '/.config/rodder/repos/' + i) == False and i != 'master-repo-list.txt':
        with open(os.getenv('HOME') + '/.config/rodder/repos/' + i) as f:
            for line in f:
                raw_package_list.append(line.strip() + ';' + i.split('.')[0])
for i in raw_package_list:
    layout.append([sg.Text(i.split(';')[0]), sg.Button('Install ' + i.split(';')[0]), sg.Button('Remove ' + i.split(';')[0])])
    package_names.append(i.split(';')[0])
# Create the Window
window1,window2 = sg.Window('rodder-gui', layout, finalize=True), None
# Event Loop to process "events" and get the "values" of the inputs
try:
    rodder_file = open(os.getenv('HOME') + '/.local/rodder/rodder').read() #I really need to make rodder a lib, and the cmd tool just be a wrapper around it so i don't have to do *THIS*
except:
    rodder_file = open('/usr/bin/rodder').read() #allow the aur version to be used. this only hammers in my point of making it a lib more
while True:
    window, event, values = sg.read_all_windows()
    #event,values = window1.read()
    if event == sg.WIN_CLOSED and window == window1: # if user closes window or clicks cancel
        break
    for i in package_names:
        if event == 'Install ' + i:
            print("User wants to " + str(event))
            #rodder_file = open(os.getenv('HOME') + '/.local/rodder/rodder').read()
            sys.argv = ['rodder', 'install', i]
            try:
                exec(rodder_file)
            except Exception as e:
                sg.popup('Installation failed!\n' + str(e))
                break
            sg.popup('Installation successful!')
        if event == 'Remove ' + i:
            print("User wants to " + str(event))
            #rodder_file = open(os.getenv('HOME') + '/.local/rodder/rodder').read() #I really need to make rodder a lib, and the cmd tool just be a wrapper around it so i don't have to do *THIS*
            sys.argv = ['rodder', 'remove', i]
            try:
                exec(rodder_file)
            except Exception as e:
                sg.popup('Removal failed!\n' + str(e))
                break
            sg.popup('Removal successful!')
    if event == 'Search' and window == window1:
        print("User wants to " + str(event) + ' {}'.format(values[0]))            
        sys.argv = ['rodder', 'search', values[0]]
        layoutnew = []
        try:
            '''exec(rodder_file)
            with open('{}/.tmp/rodder/search.txt'.format(os.getenv('HOME'))) as f:
                i = f.read()
                print(i)''' #alright, you win, i'll just copy the search code from rodder as this doesnt work (?!)
            tmp = os.listdir(os.getenv('HOME') + '/.config/rodder/repos/')
            for i in tmp:
                if os.path.isdir(os.getenv('HOME') + '/.config/rodder/repos/' + i) == False and i != 'master-repo-list.txt':
                    with open(os.getenv('HOME') + '/.config/rodder/repos/' + i) as f:
                        for line in f:
                            print(line)
                            if values[0] in line:
                                i2 = line.split(';')[0]
                                break
            layoutnew.append([sg.Text(i2), sg.Button('Install ' + i2), sg.Button('Remove ' + i2)])
            layoutnew.append([sg.Button('Back')])
            window2 = sg.Window('rodder-gui search', layoutnew, finalize=True) #this probably isn't good form but /shrug
        except Exception as e:
            sg.popup('Search failed!\n' + str(e))
            break
    #do search window/window 2 stuff
    if event == 'Back' and window == window2:
        window2.close()
    if event ==  sg.WIN_CLOSED and window == window1:
        window2.close()
window1.close()
