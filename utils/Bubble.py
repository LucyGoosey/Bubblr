from random import random
from threading import Lock
import math, logging
import tkFont

from BubblrConfig import GeneralConfig, BubblesConfig

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s)',);

class Bubble:
    def __init__(self, canvas, key, weight, summary, link, assignee="None"):
        self.lock = Lock();
        
        self.posX = 0.0;
        self.posY = 0.0;
        
        self.velX = 0.0;
        self.velY = 0.0;
        
        self.accel = 0.0;
        
        self.circ = None;
        self.text = None;
        
        self.bChangeWeight = False;
        self.displayWeight = 0.0;
        self.startWeight = 0.0;
        self.weight = 0.0;
        self.changeTime = 0.0;
        
        self.weightPct = 0;
        
        self.key = "";
        self.link = "";
        
        self.canvas = canvas;
        
        self.SetWeight(weight);
        
        if GeneralConfig.DEBUG_MODE == 0:
            self.key = key;
            self.link = link;
        else:
            self.key = self.weight;
            self.link = "http://google.co.uk";
        
        self.summary = summary;
        
        self.assignee = assignee;
        
        self.CalcSuggestedHeight();
        
        self.font = tkFont.Font(family="Arial", size=8);
        
        self.CreateBubble();
                                        
    def SetWeight(self, weight=None):
        self.startWeight = self.weight;
        self.changeTime = 0;
        
        if self.startWeight < BubblesConfig.minSize:
            self.startWeight = BubblesConfig.minSize;
    
        if not weight:
            self.weight = random() * BubblesConfig.maxWeight;
        else:
            self.weight = weight;
            
        self.weightPct = self.weight / BubblesConfig.maxWeight;

        if self.weight != self.displayWeight:
            self.bChangeWeight = True;
            
        if GeneralConfig.DEBUG_MODE != 0:
            self.key = self.displayWeight;
        
        self.accel = max(BubblesConfig.accelForce * self.weightPct,\
                            BubblesConfig.accelForce * BubblesConfig.minAccel);
        
        self.CalcSize();
        
    def ChangeWeight(self):
        self.changeTime += BubblesConfig.growthSpeed * self.weightPct;
        
        if self.changeTime < 1:
            self.displayWeight = self.startWeight + ((self.weight - self.startWeight) * self.changeTime);
        else:
            self.displayWeight = self.weight;
            self.bChangeWeight = False;
            
        if GeneralConfig.DEBUG_MODE != 0:
            self.canvas.itemconfig(self.text, text="{:3.0f}".format(self.displayWeight));
        
        self.CalcSize();
        
    def CalcSize(self):
        if self.displayWeight > BubblesConfig.maxSize:
            self.size = BubblesConfig.maxSize;
        elif self.displayWeight < BubblesConfig.minSize:
            self.size = BubblesConfig.minSize;
        else:
            self.size = self.displayWeight;
            
        self.halfSize = self.size / 2;        
                                        
    def CreateBubble(self):
        self.posX = random() * (self.canvas.winfo_width() - self.size) + self.halfSize;
        self.posY = random() * (self.canvas.winfo_height() / 4) + self.canvas.winfo_height() / 2;
        
        if GeneralConfig.DEBUG_MODE == 0:
            key = self.key;
        else:
            key = "{:3.0f}".format(self.key);
    
        self.circ = self.canvas.create_oval(self.posX - self.halfSize, self.posY - self.halfSize,\
                                        self.posX + self.halfSize, self.posY + self.halfSize,\
                                        outline=GeneralConfig.bubbleColour);
        self.text = self.canvas.create_text((self.posX, self.posY), text=key,\
                                        fill=GeneralConfig.bubbleColour, font=self.font);
    
    def DeleteBubble(self):
        self.canvas.delete(self.circ);
        self.canvas.delete(self.text);
        
    def CalcSuggestedHeight(self):
        self.suggestedHeight = (self.canvas.winfo_height() - self.halfSize)\
                                * (math.log(BubblesConfig.maxWeight - self.weight, 10) - 1);
                                
        if self.suggestedHeight < self.halfSize:
            self.suggestedHeight = self.halfSize;
        elif self.suggestedHeight > self.canvas.winfo_height() - self.halfSize:
            self.suggestedHeight = self.canvas.winfo_height() - self.halfSize;
        
    def CalcDistance(self, bubble):
        return math.sqrt(math.pow(self.posX - bubble.posX, 2) + math.pow(self.posY - bubble.posY, 2));
        
    def CheckCollisions(self, bubbles):
        for bubble in bubbles:
            if self == bubble or self.weight > bubble.weight:
                continue;
                
            dist = self.CalcDistance(bubble);
            if dist < self.halfSize + bubble.halfSize:
                self.HandleCollision(bubble);
        
    def HandleCollision(self, bubble):
        midX = (self.posX + bubble.posX) / 2.0;
        midY = (self.posY + bubble.posY) / 2.0;
        
        x = midX - bubble.posX;
        y = midY - bubble.posY;
        
        mag = math.sqrt(math.pow(x, 2) + math.pow(y, 2));
        dirX = x / mag;
        dirY = y / mag;
        
        x = (bubble.halfSize - x) / bubble.halfSize;
        y = (bubble.halfSize - y) / bubble.halfSize;
        
        pushForce = BubblesConfig.pushForce * (math.log(max(bubble.weight, 10), 10) - 1);
        otherPushForce = BubblesConfig.pushForce * (math.log(max(self.weight, 10), 10) - 1);
        
        self.velX = (self.velX + (dirX * x * pushForce)) / 2.0;
        self.velY = (self.velY + (dirY * y * pushForce)) / 2.0;
        
        bubble.velX = (bubble.velX + (-dirX * x * otherPushForce)) / 2.0;
        bubble.velY = (bubble.velY + (-dirY * y * otherPushForce)) / 2.0;
        
    def Tick(self, deltaTime):
        if self.canvas == None:
            return;
            
        if self.bChangeWeight:
            self.ChangeWeight();
            
        if self.posY - self.suggestedHeight > 0:
            self.velY -= self.accel * (abs(self.posY - self.suggestedHeight) / BubblesConfig.slowDistance);
        else:
            self.velY += self.accel * (abs(self.posY - self.suggestedHeight) / BubblesConfig.slowDistance);
                
        self.velX -= self.velX * BubblesConfig.drag;
        self.velY -= self.velY * BubblesConfig.drag;
        
        try:
            if self.posX + self.velX > self.canvas.winfo_width() - self.halfSize:
                self.velX = -self.velX;
                self.posX = self.canvas.winfo_width() - self.halfSize;
            elif self.posX + self.velX < self.halfSize:
                self.velX = -self.velX;
                self.posX = self.halfSize;
                
            if self.posY + self.velY > self.canvas.winfo_height() - self.halfSize\
                or self.posY + self.velY < self.halfSize:
                self.velY = 0;
        except:
            pass;
        
        self.posX += self.velX * max(deltaTime, 0);
        self.posY += self.velY * max(deltaTime, 0);
        
        return;
        
    def Draw(self):
        if self.canvas == None:
            return;
            
        try:
            # TODO Highlight bubbles in circle not square
            if self.canvas.winfo_pointerx() - self.canvas.winfo_rootx() > self.posX - self.halfSize\
                and self.canvas.winfo_pointerx() - self.canvas.winfo_rootx() < self.posX + self.halfSize\
                and self.canvas.winfo_pointery() - self.canvas.winfo_rooty() > self.posY - self.halfSize\
                and self.canvas.winfo_pointery() - self.canvas.winfo_rooty() < self.posY + self.halfSize:
                self.canvas.itemconfig(self.circ, outline=GeneralConfig.highlightColour);
                self.canvas.itemconfig(self.text, fill=GeneralConfig.highlightColour);
            else:
                self.canvas.itemconfig(self.circ, outline=GeneralConfig.bubbleColour);
                self.canvas.itemconfig(self.text, fill=GeneralConfig.bubbleColour);

            pos = (self.posX - self.halfSize, self.posY - self.halfSize,\
                                        self.posX + self.halfSize, self.posY + self.halfSize);
            self.canvas.coords(self.circ, pos);
            self.canvas.coords(self.text, (self.posX, self.posY));
        except:
            pass;