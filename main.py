import Tkinter as tk
from query import QueryHandler
import webbrowser

root = tk.Tk()
root.title("Search")
root.configure(bg = "#4ECDC4")
root.geometry("500x500")
currentLinks = []
queryHandler = QueryHandler()

def callback(i):
    if currentLinks != []:
        browser = webbrowser.get('chrome')
        browser.open("{}".format(currentLinks[i]))

def show_query():
    query = inputField.get()
    print query
    global currentLinks
    currentLinks = queryHandler.getLinks(query)
    print(currentLinks)
    for i in range(5):
        el = ""
        if len(currentLinks[i]) > 50: el = "..."
        textVars[i].set("Link {} : {}{}".format(i+1, currentLinks[i][:50], el))

searchLabel = tk.Label(master=root, text="Enter search query: ", bg = "#4ECDC4")
searchLabel.grid(row = 0, column = 0, padx = 10, pady = 10)

inputField = tk.Entry(root)
inputField.grid(row=0, column=1, pady=10, padx=10)

searchButton = tk.Button(root, text='Search', command=show_query, bg='#4ECDC4')
searchButton.grid(row=0, column=2, pady=10, padx=10)

textVars = []

for i in range(5):
    textVars.append(tk.StringVar())
    link = tk.Button(root, textvariable= textVars[-1],
                    anchor='w', justify='left', cursor='hand1', command=lambda i=i: callback(i), bg='#4ECDC4')
    link.grid(row=1 + i, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

root.mainloop()