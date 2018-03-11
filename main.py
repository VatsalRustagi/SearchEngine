import Tkinter as tk
from query import QueryHandler, QueryNotFound
import webbrowser

class SearchEngine:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Search")
        self.root.configure(bg = "#4ECDC4")
        self.root.geometry("500x500")
        self.currentLinks = []
        self.queryHandler = QueryHandler()

        self.BACKGROUND = "#4ECDC4"
        self.makeUI()

    def makeUI(self):
        searchLabel = tk.Label(master=self.root, text="Enter search query: ", bg=self.BACKGROUND)
        searchLabel.grid(row=0, column=0, padx=10, pady=10)

        self.inputField = tk.Entry(self.root)
        self.inputField.grid(row=0, column=1, pady=10, padx=10)

        searchButton = tk.Button(self.root, text='Search', command=self.show_query)
        searchButton.grid(row=0, column=2, pady=10, padx=10)

        self.textVars = []

        for i in range(5):
            self.textVars.append(tk.StringVar())
            link = tk.Button(self.root, textvariable=self.textVars[-1],
                             anchor='w', justify='left', cursor='hand1', command=lambda i=i: self.callback(i))
            link.grid(row=1 + i, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)


    def callback(self, i):
        if self.currentLinks != []:
            browser = webbrowser.get('chrome')
            browser.open("{}".format(self.currentLinks[i]))

    def show_query(self):
        query = self.inputField.get()

        try:
            self.currentLinks = self.queryHandler.getLinks(query)
        except QueryNotFound:
            self.popErrorBox()
            return

        for i in range(5):
            el = ""
            if len(self.currentLinks[i]) > 50: el = "..."
            self.textVars[i].set("Link {} : {}{}".format(i+1, self.currentLinks[i][:50], el))

    def popErrorBox(self):
        self.winner = tk.Toplevel()
        self.winner.title("Query Not Found")
        self.winner.config(bg=self.BACKGROUND)

        label = tk.Label(self.winner,bg=self.BACKGROUND, text="Could not find a match for the query!")
        # label.grid(row=0, column=0, padx=10, pady=10)
        label.pack(fill=tk.X, padx=10, pady=10)

        button = tk.Button(master=self.winner, text="Ok", command=self.winner.destroy)
        # button.grid(row=1, column=0, padx=10, pady=10)
        button.pack(fill=tk.X, padx=10, pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    se = SearchEngine()
    se.run()