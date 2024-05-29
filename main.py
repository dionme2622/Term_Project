from tkinter import Tk
import Intro
import Bookmark
import requests
import xml.etree.ElementTree as ET

def main():
    root = Tk()
    scene_stack = []
    app = Intro.IntroWindow(root, scene_stack)
    root.mainloop()

if __name__ == "__main__":
    main()
