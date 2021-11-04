from tkinter import *
import requests
import hashlib


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again!')
    return res


def get_pass_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5)
    return get_pass_leak_count(response, tail)


def mainReply():
    args = questionField.get()
    count = pwned_api_check(args)
    if count:
        textArea.insert(END, f'{args} was found {count} times .... you should probably change your password!')
    else:
        textArea.insert(END, f'{args} was not found. Carry on!')
    questionField.delete(0, END)


def clear():
    textArea.delete(1.0, END)


root = Tk()
root.geometry("530x610+300+10")
root.title("Check My Password")
myColor = "#ff781f"
root.config(bg=myColor)

logoPic = PhotoImage(file="path_new2.png")
logoPicLabel = Label(root, image=logoPic, bg=myColor)
logoPicLabel.pack(pady=5)

centerFrame = Frame(root)
centerFrame.pack()

scrollBar = Scrollbar(centerFrame)
scrollBar.pack(side=RIGHT)

textArea = Text(centerFrame, font=("times new roman", 20, "bold"),
                height=10, yscrollcommand=scrollBar.set, wrap="word")
textArea.pack(side=LEFT)
scrollBar.config(command=textArea.yview)

questionField = Entry(root, font=("verdana", 20, "bold"))
questionField.pack(pady=15, fill=X)

askImage = PhotoImage(file="ask.png")
askButton = Button(root, image=askImage, command=mainReply, fg=myColor,
                   bg=myColor, bd=0, activebackground=myColor,
                   activeforeground=myColor)
askButton.pack(side=LEFT)

clearImage = PhotoImage(file="clear.png")
clearButton = Button(root, image=clearImage, command=clear, fg=myColor,
                     bg=myColor, bd=0, activebackground=myColor,
                     activeforeground=myColor)
clearButton.pack(side=RIGHT)

root.mainloop()
