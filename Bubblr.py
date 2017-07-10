import time
import logging

from Tkinter import *
from tkMessageBox import *
from threading import *
from jira.client import JIRA
from jira import JIRAError

from utils.Config import GeneralConfig, ServerConfig, SaveConfig, SaveWindowConfig
from utils.Bubble import Bubble
from utils.Threads import MainThread, QueryThread
from utils.Dialogs import ServerDialog, OptionsDialog

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s)',);

class Bubblr:
    def __init__(self, parent):
        self.parent = parent;
        
        self.parent.protocol("WM_DELETE_WINDOW", self.CloseWindow);
        
        self.queryThread = None;
        self.mainThread = None;
        
        self.queryCommand = None;
        self.queryEvent = Event();
        self.queryCommand = "";
        self.jqlQuery = "";
        
        self.mainThread = MainThread(name="Main-Thread");
        self.mainThread.setDaemon(True);
        self.parent.bind("<Button-1>", self.mainThread.OnClick);
        
        self.InitUI();
        
        if GeneralConfig.DEBUG_MODE == 0:
            self.queryThread = QueryThread(name="Query-Thread", args=(self,));
            self.queryThread.setDaemon(True);
            self.queryThread.start();
        
            self.ShowConnectDialog();
        
        self.mainThread.start();
        
    def CloseWindow(self):
        SaveWindowConfig(self.parent);
        SaveConfig();
        
        if self.queryThread:
            self.queryThread.EndThread();
        
        if self.mainThread:
            self.mainThread.EndThread();
        
        self.parent.destroy();
        
    def InitUI(self):    
        self.parent.title("Bubblr");
        
        self.InitMenubar();
        
        self.mainframe = Frame(self.parent);
        self.mainframe.pack(expand=1, fill=BOTH);
        
        self.status = StringVar();
        self.status.set("...");
        label = Label(self.mainframe, textvariable=self.status);
        
        label.pack(fill=X);
        
        self.mainThread.canvas = Canvas(self.mainframe, bg=GeneralConfig.backgroundColour);
        
        self.mainThread.canvas.pack(expand=1, fill=BOTH);
        
        inputFrame = Frame(self.mainframe, width=GeneralConfig.windowWidth, height=GeneralConfig.windowHeight);
        inputFrame.pack(fill=X);
        
        self.queryBox = StringVar();
        self.queryBox.set(ServerConfig.lastQuery);
        textbox = Entry(inputFrame, textvariable=self.queryBox);
        
        button = None;
        if GeneralConfig.DEBUG_MODE == 0:
            button = Button(inputFrame, text="Go!", command=self.PrepareQuery);
            self.parent.bind("<Return>", self.PrepareQuery);
        else:
            button = Button(inputFrame, text="Go!", command=self.mainThread.FakeBubbles);
            self.parent.bind("<Return>", self.mainThread.FakeBubbles);
        
        textbox.pack(side=LEFT, anchor=NW, expand=1, fill=X, padx=2, pady=5);
        button.pack(side=LEFT, anchor=NW);
        
    def InitMenubar(self):
        menubar = Menu(self.parent);
        
        filemenu = Menu(menubar, tearoff=0);
        filemenu.add_command(label="Connect...", command=self.ShowConnectDialog);
        filemenu.add_separator();
        #filemenu.add_command(label="Options", command=self.ShowOptions);
        #filemenu.add_separator();
        filemenu.add_command(label="Exit", command=self.CloseWindow);
        menubar.add_cascade(label="File", menu=filemenu);
        
        self.parent.config(menu=menubar);
        
    def ShowConnectDialog(self):
        ServerDialog(self.parent, self);
        
    def ShowOptions(self):
        OptionsDialog(self.parent);
        
    def PrepareQuery(self, event=None, query=None):
        if query == None:
            query = self.queryBox.get();
            
        self.queryCommand = "query";
        self.jqlQuery = query;
        self.queryEvent.set();

def main():
    root = Tk();
    
    if GeneralConfig.windowPos != None:
        root.geometry("{0}x{1}+{2}+{3}".format(*(GeneralConfig.windowWidth, GeneralConfig.windowHeight,\
                                                    GeneralConfig.windowPos[0], GeneralConfig.windowPos[1])));
    else:
        root.geometry("{0}x{1}".format(*(GeneralConfig.windowWidth, GeneralConfig.windowHeight)));

    root.update();
    
    app = Bubblr(root);
    
    root.mainloop();

if __name__ == '__main__':
    main();
