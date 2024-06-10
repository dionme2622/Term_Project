from tkinter import Tk
import Intro
import Bookmark
import requests
import xml.etree.ElementTree as ET

def main():
    root = Tk()
    scene_stack = []
    bookmarks = []
    app = Intro.IntroWindow(root, scene_stack, bookmarks)
    root.mainloop()

if __name__ == "__main__":
    main()
