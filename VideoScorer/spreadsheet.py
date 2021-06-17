from VideoScorer.videoplayer import VideoPlayer
from VideoScorer.scrollableframe import ScrollableFrame
from VideoScorer.popup_entry_window import PopupEntryWindow

from pathlib import Path

import numpy as np
import pandas as pd
import tkinter as tk
from tkinter.font import Font
import tkinter.messagebox as msg
from tkinter import filedialog

class Spreadsheet(tk.Frame):
    ROW_WIDTH = 3
    COLUMN_WIDTH = 10
    PADX=2
    PADY=2
    UNSELECTED_COLOUR='gray'
    SELECTED_COLOUR='green'
    ORIGNAME = 'behaviour.csv'
    NEWNAME = 'behaviour_scored.csv'
    DIRECTIONS = {'<Left>': (-1,0), '<Right>': (1,0), '<Up>': (0,-1), '<Down>': (0,1)}
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.container = container
        self._create_menu()
        self.file_str_template = '{file}.mp4'
        self.video_player = VideoPlayer()

    def _create_menu(self):
        self.menu_font = Font(family="Verdana", size=20)
        self.menubar = tk.Menu(self.container)
        self.menubar.add_command(label='Open', command=self.filedialog)
        self.menubar.add_command(label='Save', command=self.savefile)
        self.menubar.add_command(label='Configure', command=self.configure)
        self.menubar.add_command(label='New Column', command=self.new_column_gui)
        self.menubar.add_command(label='Help', command=self.help)
        self.menubar.config(font=self.menu_font)
        self.container.config(menu=self.menubar)
    def _initialize(self):
        if hasattr(self, 'editor_frame'): self.editor_frame.destroy()
        self.editor_frame = ScrollableFrame(self)
        self.editor = self.editor_frame.scrollable_frame
        self.column_labels = {}
        self.row_labels = []
        self.row_labels_text = []
        self.cells = {}
        for idx, row in enumerate(self.data.index):
            self.row_labels_text.append(tk.StringVar())
            self.row_labels_text[idx].set(row)
            self.row_labels.append(tk.Label(
                self.editor, 
                width=self.ROW_WIDTH, 
                textvariable=self.row_labels_text[idx],
                bg=self.UNSELECTED_COLOUR
            ))
            self.row_labels[idx].grid(row=idx+1,column=0,padx=self.PADX,pady=self.PADY)
        for idx, column in enumerate(self.data.columns):
            self._add_column(column)
        self._populate()
        self.editor_frame.pack(side="left", fill="both", expand=True)
    def _add_column(self, column):
        col = len(self.column_labels)
        self.column_labels[column] = tk.Label(
            self.editor, 
            width=self.COLUMN_WIDTH, 
            text=column
        )
        self.column_labels[column].grid(row=0,column=col+1,padx=self.PADX,pady=self.PADY)
        self.column_labels[column].bind('<Button-1>', lambda e: self.sort_by(column))
        for row in range(len(self.data[column])):
            self.cells[row, col] = tk.Entry(self.editor, width=self.COLUMN_WIDTH)
            self.cells[row, col].grid(row=row+1,column=col+1,padx=self.PADX,pady=self.PADY)
            self._bind_cell_commands(row, col)
    def _populate(self):
        for (row, col), data in np.ndenumerate(self.data):
            self.cells[row, col].delete(0, tk.END)
            self.cells[row, col].insert(0, data)
        for idx, row in enumerate(self.data.index):
            self.row_labels_text[idx].set(row)

    def filedialog(self):
        directory = filedialog.askdirectory(title='Choose Video Directory', mustexist=True, initialdir=Path.cwd())
        self.load_directory(directory)
    def new_column_gui(self):
        if not hasattr(self, 'cells'): 
            msg.showerror("ERROR","Open a file first!")
            return
        popup = PopupEntryWindow(
            self.container, 
            'New Column', 
            {
                'New Column Name': dict(),
                'Default Value': dict(default='')
            }
        )
        self.container.wait_window(popup.frame)
        if not hasattr(popup, 'values'):
            # msg.showerror("ERROR", "pop window closed rudely")
            return
        if popup.values['New Column Name']:
            self.new_column(popup.values['New Column Name'], popup.values['Default Value'])
        else:
            msg.showerror("ERROR", "No new column name provided")
    def configure(self):
        popup = PopupEntryWindow(
            self.container,
            'Configure',
            {
                'File Template': dict(default=self.file_str_template)
            }
        )
        self.container.wait_window(popup.frame)
        if not hasattr(popup, 'values'):
            # msg.showerror("ERROR", "pop window closed rudely")
            return

        file_template = popup.values.get('File Template','')
        if not '{file}' in file_template:
            print(file_template)
            msg.showerror("ERROR", "Invalid template string provided")
        else:
            self.file_str_template = file_template
            if hasattr(self, 'directory'):
                matches = len(list(self.directory.glob(self.file_str_template.replace('{file}', '*'))))
                msg.showinfo('INFO',f'Found {matches} file(s) matching the provided pattern')
    def help(self):
        msg.showerror('ERROR','Help is not yet implemented')
    def savefile(self):
        column_labels = list(self.column_labels.keys())
        row_labels = [label['text'] for label in self.row_labels]
        self.data = pd.Series({(row_labels[row], column_labels[col]): v.get() for (row,col),v in self.cells.items()}).unstack().loc[sorted(row_labels), column_labels]
        self.data.to_csv(self.filepath)
    def load_directory(self, directory):
        self.directory = Path(directory)
        new, orig = self.directory/self.NEWNAME, self.directory/self.ORIGNAME
        if new.is_file():
            filepath = new
        elif orig.is_file():
            filepath = orig
        else:
            msg.showerror("ERROR", f"No behaviour file found in {directory.as_posix()}")
        self.data = pd.read_csv(filepath, header=[0], index_col=[0])
        self.filepath = new
        self.active = None
        self._initialize()
    def new_column(self, column_name, default_value=''):
        self.data[column_name] = default_value
        self._add_column(column_name)
        self._populate()
    def sort_by(self, column):
        if self.active is not None: 
            selected = self.data.index[self.active]
            self.row_labels[self.active].configure(bg=self.UNSELECTED_COLOUR)
        self.data.sort_values(column, inplace=True)
        self._populate()
        if self.active is not None:
            self.active = self.data.index.tolist().index(selected)
            self.row_labels[self.active].configure(bg=self.SELECTED_COLOUR)
    def select(self, e, row, col):
        if self.active is not None: self.row_labels[self.active].configure(bg=self.UNSELECTED_COLOUR)
        self.row_labels[row].configure(bg=self.SELECTED_COLOUR)
        self.active = row
        self.video_player.play_movie(self.directory/self.file_str_template.format(file=int(self.data.index[self.active])))
    def set_focus(self, event, direction, row, col):
        dx, dy = self.DIRECTIONS.get(direction)
        target_cell = row+dx, col+dy
        if target_cell in self.cells:
            self.cells[target_cell].focus_set()
    def _bind_cell_commands(self, row, col):
        self.cells[row, col].config(validate="focusout", validatecommand=self.savefile)
        # for direction in self.DIRECTIONS:
        #     self.cells[row, col].bind(direction, lambda e,direction=direction,row=row,col=col: self.set_focus(e,direction,row,col))
        # self.cells[row, col].bind('<Enter>', lambda e,direction='<Down>',row=row,col=col: self.set_focus(e,direction,row,col))
        self.cells[row, col].bind('<Button-3>', lambda e, row=row, col=col: self.select(e, row, col))
        self.cells[row, col].bind('<Control-Enter>', lambda e, row=row, col=col: self.select(e, row, col))

if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    root = tk.Tk()
    sp = Spreadsheet(root, path)
    sp.pack(side="left", fill="both", expand=True)
    root.mainloop()