from VideoScorer.spreadsheet import Spreadsheet

import click
import tkinter as tk

@click.command()
@click.option('-d','--directory',default=None, help='Optionally specify a directory to load')
@click.option('-v','--verbose',default=False, is_flag=True, help='Print more info')
def main(directory, verbose):
    """ Launch the VideoScorer GUI """
    root = tk.Tk()
    root.title('VideoScorer')
    sp = Spreadsheet(root, width=600, height=200, verbose=verbose)
    sp.pack(side="left", fill="both", expand=True)
    if directory is not None:
        sp.load_directory(directory)
    root.mainloop()

if __name__ == '__main__':
    main()