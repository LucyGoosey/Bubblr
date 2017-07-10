import time, math, webbrowser, logging

from random import random
from math import ceil
from threading import Thread
from Tkinter import *
from tkMessageBox import *

from BubblrConfig import GeneralConfig, ServerConfig
from Bubble import Bubble

from jira.client import JIRA
from jira import JIRAError

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s)',);

class MainThread(Thread):
    MIN_BUBBLE_MOD = 0.66;

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        Thread.__init__(self, group=group, target=target, name=name, verbose=verbose);
        
        self.args = args;
        self.kwargs = kwargs;
        
        self.bubbles = [];
        self.canvas = None;
        
        self.sleepTime = float(1) / float(GeneralConfig.framesPerSecond);
        
        self.lastTick = time.clock();
        
        self.bEnd = False;
        
        self.clickPos = None;

        return;
        
    def EndThread(self):
        self.bEnd = True;
        del self.bubbles[:];
        
    def run(self):
        self.FakeBubbles();
        
        while not self.bEnd:
            if self.bubbles == [] or self.canvas == None:
                continue;
                
            t = time.clock();
            self.Tick();
            self.Draw();
            time.sleep(max(0, self.sleepTime - (time.clock() - t)));
            
    def FakeBubbles(self, event=None):
        self.canvas.delete("all");
        del self.bubbles[:];
        
        minBubbles = GeneralConfig.maxBubbles * MainThread.MIN_BUBBLE_MOD;

        for i in range(0, int(ceil(random() * (GeneralConfig.maxBubbles - minBubbles) + minBubbles))):
            self.bubbles.append(Bubble(self.canvas, None, 0, "", ""));
            
    def InitBubbles(self, issues):
        self.canvas.delete("all");
        del self.bubbles[:];
        for issue in issues:
            self.bubbles.append(Bubble(self.canvas, issue.key, 0, issue.fields.summary, issue.self));
            
    def Tick(self):
        if self.clickPos != None:
            self.CheckClick();
            
        for bubble in self.bubbles:
            bubble.CheckCollisions(self.bubbles);
        for bubble in self.bubbles:
            bubble.Tick(time.clock() - self.lastTick);
        self.lastTick = time.clock();
        
    def Draw(self):        
        for bubble in self.bubbles:
            bubble.Draw();
            
        self.canvas.update();
        
    def CheckClick(self):
        for bubble in self.bubbles:
            dist = math.sqrt(math.pow(self.clickPos[0] - bubble.posX, 2) + math.pow(self.clickPos[1] - bubble.posY, 2));
            if bubble.link != "" and dist < bubble.halfSize:
                webbrowser.open_new_tab(bubble.link);
                break;
                
        self.clickPos = None;
            
    def OnClick(self, event):
        self.clickPos = (event.x, event.y);            
        
class QueryThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        Thread.__init__(self, group=group, target=target, name=name, verbose=verbose);
        
        self.args = args;
        self.kwargs = kwargs;
        
        self.parent = args[0];
        
        self.bConnected = False;
        
        self.bEnd = False;
        
        return;
        
    def EndThread(self):
        self.parent.queryEvent.set();
        self.bEnd = True;
        
    def ConnectToJIRA(self, server, username, password):
        ServerConfig.URL = server;
        ServerConfig.username = username;
        
        if server == "" or username == "" or password == "":
            if GeneralConfig.DEBUG_MODE == 0:
                showerror("Input Error!", "All fields are required");
                return False;
            else:
                return True;

        self.parent.status.set("Connecting to {0}...".format(server));
        self.bConnected = False;
        
        try:
            self.jira = JIRA(server=server, basic_auth=(username, password));
            self.parent.status.set("Connected!");
            
            self.bConnected = True;
            return True;
        except Exception as err:
            showerror("Connection Error!", err.message);
            self.parent.ShowConnectDialog();
            return False;
        
    def run(self):            
        while not self.bEnd:
            self.parent.queryEvent.wait();
            
            if "connect" in self.parent.queryCommand:
                spl = self.parent.jqlQuery.split(",");
                self.ConnectToJIRA(spl[0], spl[1], spl[2]);
                
                self.parent.queryEvent.clear();
                continue;
            
            if not self.bConnected or self.bEnd:
                self.parent.queryEvent.clear();
                continue;
                
            if not "query" in self.parent.queryCommand:
                self.parent.queryEvent.clear();
                continue;
                
            jqlQuery = self.parent.jqlQuery;
            
            self.parent.status.set("Querying: {0}".format(jqlQuery));
            try:
                issues = self.jira.search_issues(jqlQuery, maxResults=GeneralConfig.maxBubbles);
                
                self.parent.status.set(jqlQuery);
                
                ServerConfig.lastQuery = jqlQuery;
            
                self.parent.mainThread.InitBubbles(issues);
            except JIRAError as err:
                showwarning("Query Error!", err.text);
                self.parent.status.set("Query error");
            
            self.parent.queryEvent.clear();