from tkinter import * 
import importlib


sshModule = importlib.import_module('ssh')
sessionsModule = importlib.import_module('sessions')
sessions = sessionsModule.Sessions()


def openTerminal(ssh):
    window.destroy()

    def sendCommand():
        command = terminalInput.get()
        terminalInput.delete(0, END)

        output = ssh.sendCommand(command)
        text1.config(state=NORMAL)
        text1.insert(END, '\n' + output)
        text1.config(state=DISABLED)

    terminal = Tk()
    terminal.title('Terminal')
    
    text1 = Text(master=terminal, state=DISABLED)
    text1.grid(row=0)

    terminalInput = Entry(terminal)
    terminalInput.grid(row=1, column=0)

    terminalButton = Button(terminal, text='Send', command=sendCommand)
    terminalButton.grid(row=1, column=1)

    terminal.bind('<Return>', sendCommand)
    terminal.mainloop()

def connect():
    host, username, password = hostInput.get(), usernameInput.get(), passwordInput.get()
    ssh = sshModule.SSH(host, username, password)
    openTerminal(ssh)

def saveSession():
    host, username, password = hostInput.get(), usernameInput.get(), passwordInput.get()

    if not host or not username or not password:
        return

    sessions.storeSession(host, username, password)
    refreshWindow()

def replaceText(session):
    host, username, password = session.split('-')

    hostInput.delete(0, END)
    usernameInput.delete(0, END)
    passwordInput.delete(0, END)

    hostInput.insert(0, host)
    usernameInput.insert(0, username)
    passwordInput.insert(0, password)


def refreshWindow():
    hostInput.delete(0, END)
    usernameInput.delete(0, END)
    passwordInput.delete(0, END)
    text.delete(1.0, END)

    currentSessions = sessions.getSessions()
    for session in currentSessions:
        host, username, password = session
        displayName = host + '@' + username
        sessionName = host + '-' + username + '-' + password

        text.insert(END, displayName + "\n", sessionName)
        text.tag_configure(sessionName, foreground="blue", underline=True)
        text.tag_bind(sessionName, "<1>", lambda event, session=sessionName: replaceText(session))

window = Tk()
window.title('SSH')

hostLabel = Label(window, text="Host")
hostLabel.grid(row=0)
hostInput = Entry(window)
hostInput.grid(row=1)

usernameLabel = Label(window, text="Username")
usernameLabel.grid(row=2)
usernameInput = Entry(window)
usernameInput.grid(row=3)

passwordLabel = Label(window, text="Password")
passwordLabel.grid(row=4)
passwordInput = Entry(window, show='*')
passwordInput.grid(row=5)

connectButton = Button(window, text="CONNECT", command=connect).grid(row=6, column=0)
saveSession = Button(window, text="SAVE", command=saveSession).grid(row=6, column=1)

Label(window, text="Saved Sessions").grid(row=7)
text = Text(master=window)
scroll =Scrollbar(window, orient=VERTICAL, command=text.yview)
scroll.grid(row=8, column=2, sticky=NS)
text.grid(row=8, column=1, sticky=W)
text.config(yscrollcommand=scroll.set,font=('Arial', 8, 'bold', 'italic'))

refreshWindow()
window.mainloop()