from Tkinter import *

from BubblrConfig import GeneralConfig, ServerConfig

class ServerDialog:
    def __init__(self, root, parent):
        self.parent = parent;
        
        self.top = Toplevel(root);
        self.top.title("");
        
        width = 320;
        height = 110;
        self.top.geometry("{0}x{1}+{2}+{3}".format(width, height,\
                                            (root.winfo_x() + (root.winfo_width() / 2)) - (width / 2),\
                                            (root.winfo_y() + (root.winfo_height() / 2)) - (height / 2)));
        
        self.top.lift(aboveThis=root);
        
        self.top.grab_set();
        self.top.focus_set();
        
        self.top.attributes("-toolwindow",1);
        
        self.top.bind("<Return>", self.OK);
        
        self.top.protocol("WM_DELETE_WINDOW", self.CloseWindow);
        
        topFrame = Frame(self.top);
        bottomFrame = Frame(self.top);
        
        topFrame.grid(column=0, row=0);
        bottomFrame.grid(column=0, row=1);
        
        sLabel = Label(topFrame, text="Server:");
        self.serv = StringVar();
        self.serv.set(ServerConfig.URL);
        sEntry = Entry(topFrame, textvariable=self.serv, width=40);
        
        uLabel = Label(topFrame, text="Username:");
        self.user = StringVar();
        self.user.set(ServerConfig.username);
        uEntry = Entry(topFrame, textvariable=self.user, width=40);
        
        pLabel = Label(topFrame, text="Password:");
        self.password = StringVar();
        pEntry = Entry(topFrame, textvariable=self.password, show="*", width=40);
        
        if ServerConfig.URL == "":
            sEntry.focus_set();
        elif ServerConfig.username == "":
            uEntry.focus_set();
        else:
            pEntry.focus_set();
        
        ok = Button(bottomFrame, text="OK", command=self.OK, width=15);
        
        sLabel.grid(column=0, row=0);
        sEntry.grid(column=1, row=0);
    
        uLabel.grid(column=0, row=1);
        uEntry.grid(column=1, row=1);
    
        pLabel.grid(column=0, row=2);
        pEntry.grid(column=1, row=2);
        
        ok.grid(column=1, row=3);
        
    def OK(self, event=None):
        self.parent.queryCommand = "connect";

        self.parent.jqlQuery = "{0},{1},{2}".format(self.serv.get(), self.user.get(), self.password.get());
        self.parent.queryEvent.set();
            
        self.top.destroy();
        
    def CloseWindow(self):
        self.top.destroy();
        
class OptionsDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent);
        self.top.title("");
        
        width = 500;
        height = 760;
        
        self.top.geometry=("{0}x{1}+{2}+{3}".format(width, height,\
                                            (parent.winfo_x() + (parent.winfo_width() / 2)) - (width / 2),\
                                            (parent.winfo_y() + (parent.winfo_height() / 2)) - (height / 2)));
                                            
        self.top.lift(aboveThis=parent);
        
        self.top.grab_set();
        self.top.focus_set();
        
        self.top.attributes("-toolwindow",1);
        
        self.top.bind("<Return>", self.OK);
        self.top.protocol("WM_DELETE_WINDOW", self.CloseWindow);
        
    def OK(self):
        self.CloseWindow();
        
    def CloseWindow(self):
        self.top.destroy();