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
        text1.insert(END, '> ' + output)
        text1.config(state=DISABLED)
        text1.yview(END)

    terminal = Tk()
    terminal.geometry('600x415')
    terminal.title('Terminal')
    
    text1 = Text(master=terminal, state=DISABLED)
    text1.grid(row=0)

    terminalInput = Entry(terminal)
    terminalInput.place(x=10, y=390, width=500)

    terminalButton = Button(terminal, text='Send', command=sendCommand)
    terminalButton.place(x=515, y=389, width=60)

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
window.geometry("450x550")

hostLabel = Label(window, text="Host")
hostLabel.grid(row=0, padx=215, pady=3)

hostInput = Entry(window)
hostInput.grid(row=1, pady=3)

usernameLabel = Label(window, text="Username")
usernameLabel.grid(row=2, pady=3)
usernameInput = Entry(window)
usernameInput.grid(row=3, pady=3)

passwordLabel = Label(window, text="Password")
passwordLabel.grid(row=4, pady=3)
passwordInput = Entry(window, show='*')
passwordInput.grid(row=5, pady=3)

connectButton = Button(window, text="CONNECT", command=connect, width=10).grid(row=6, pady=3)
saveSession = Button(window, text="SAVE", command=saveSession, width=10).grid(row=7, pady=3)

Label(window, text="Saved Sessions").grid(row=8, pady=(10, 0))
text = Text(master=window)
scroll =Scrollbar(window, orient=VERTICAL, command=text.yview)
scroll.place(x=430, y=250, height=280)
text.place(x=10, y=250, height=280, width=430)
text.config(yscrollcommand=scroll.set, font=('Arial', 11, 'bold', 'italic'))

refreshWindow()
window.mainloop()