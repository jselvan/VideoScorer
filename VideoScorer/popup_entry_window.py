import tkinter as tk

class PopupEntryWindow:
    PADX = PADY = 2
    def __init__(self, master, label, fields):
        self.frame=tk.Toplevel(master)
        self.label=tk.Label(self.frame,text=label)
        self.label.grid(row=0,column=0,padx=self.PADX,pady=self.PADY)

        self.fields = {}
        for idx, (field, values) in enumerate(fields.items()):
            tk.Label(self.frame, text=field).grid(row=idx+1,column=0,padx=self.PADX,pady=self.PADY)
            self.fields[field] = tk.Entry(self.frame)
            default = values.get('default')
            if default is not None:
                self.fields[field].insert(0, default)
            self.fields[field].grid(row=idx+1, column=1,padx=self.PADX,pady=self.PADY)

        self.submit_button=tk.Button(self.frame,text='Submit',command=self.submit)
        self.submit_button.grid(row=idx+2,column=1,padx=self.PADX,pady=self.PADY)
    def submit(self):
        self.values = {field: entry.get() for field, entry in self.fields.items()}
        self.frame.destroy()