import os

class GeneralConfig:
    DEBUG_MODE = 1;
    
    windowWidth = 456;
    windowHeight = 640;
    windowPos = None;
    
    framesPerSecond = 30;
    maxBubbles = 50;
    
    backgroundColour = "#006994";
    bubbleColour = "#FFFFFF";
    highlightColour = "#FF2233";
    
class ServerConfig:
    URL = "";
    username = "";
    lastQuery = "";

class BubblesConfig:
    maxWeight = 100;
    accelForce = 15;
    minAccel = 0.15;
    pushForce = 25;
    slowDistance = 200;
    drag = 0.15;
    
    minSize = 33;
    maxSize = 80;
    growthSpeed = 0.0015;

def SaveConfig():
    with open(CONF_PATH, 'w+') as file:
        file.write("General:\n");
        file.write("\tWindowWidth:{0}\n".format(GeneralConfig.windowWidth));
        file.write("\tWindowHeight:{0}\n".format(GeneralConfig.windowHeight));
        if GeneralConfig.windowPos != None:
            file.write("\tWindowPos:{0},{1}\n".format(GeneralConfig.windowPos[0], GeneralConfig.windowPos[1]));
        file.write("\n");
        file.write("\tFramesPerSecond:{0}\n".format(GeneralConfig.framesPerSecond));
        file.write("\tMaxBubbles:{0}\n".format(GeneralConfig.maxBubbles));
        file.write("\n");
        file.write("\tBackgroundColour:{0}\n".format(GeneralConfig.backgroundColour));
        file.write("\tBubbleColour:{0}\n".format(GeneralConfig.bubbleColour));
        file.write("\tHighlightColour:{0}\n".format(GeneralConfig.highlightColour));
        file.write(":end\n\n");
        
        file.write("Server:\n");
        file.write("\tURL:{0}\n".format(ServerConfig.URL));
        file.write("\tUsername:{0}\n".format(ServerConfig.username));
        file.write("\tLastQuery:{0}\n".format(ServerConfig.lastQuery));
        file.write(":end\n\n");
        
        file.write("Bubbles:\n");
        file.write("\tMaxWeight:{0}\n".format(BubblesConfig.maxWeight));
        file.write("\tAccelForce:{0}\n".format(BubblesConfig.accelForce));
        file.write("\tMinAccel:{0}\n".format(BubblesConfig.minAccel));
        file.write("\tPushForce:{0}\n".format(BubblesConfig.pushForce));
        file.write("\tSlowDistance:{0}\n".format(BubblesConfig.slowDistance));
        file.write("\tDrag:{0}\n".format(BubblesConfig.drag));
        file.write("\n");
        file.write("\tMinSize:{0}\n".format(BubblesConfig.minSize));
        file.write("\tMaxSize:{0}\n".format(BubblesConfig.maxSize));
        file.write("\tGrowthSpeed:{0}\n".format(BubblesConfig.growthSpeed * 1000));
        file.write(":end\n");
        
def SaveWindowConfig(root):
    GeneralConfig.windowWidth = root.winfo_width();
    GeneralConfig.windowHeight = root.winfo_height();
    
    GeneralConfig.windowPos = (root.winfo_x(), root.winfo_y());
        
def ReadConfigFile():
    with open(CONF_PATH, 'r') as file:
        line = file.readline();
        while line:
            if "General:" in line:
                ReadGeneralSection(file);
            elif "Server:" in line:
                ReadServerSection(file);
            elif "Bubbles:" in line:
                ReadBubblesSection(file);
                
            line = file.readline();
                
def ReadGeneralSection(file):
    line = file.readline();
    while line and not ":end" in line:
        spl = line.split(":", 1);
        if "WindowWidth" in spl[0]:
            GeneralConfig.windowWidth = int(spl[1]);
        elif "WindowHeight" in spl[0]:
            GeneralConfig.windowHeight = int(spl[1]);
        elif "WindowPos" in spl[0]:
            spl = spl[1].split(",");
            GeneralConfig.windowPos = (int(spl[0]), int(spl[1]));
        elif "FramesPerSecond" in spl[0]:
            GeneralConfig.framesPerSecond = int(spl[1]);
        elif "MaxBubbles" in spl[0]:
            GeneralConfig.maxBubbles = int(spl[1]);
        elif "BackgroundColour" in spl[0]:
            GeneralConfig.backgroundColour = spl[1].strip(" \t\n");
        elif "BubbleColour" in spl[0]:
            GeneralConfig.bubbleColour = spl[1].strip(" \t\n");
        elif "HighlightColour" in spl[0]:
            GeneralConfig.highlightColour = spl[1].strip(" \t\n");
            
        line = file.readline();
            
def ReadServerSection(file):
    line = file.readline()
    while line and not ":end" in line:
        first = line.split(":", 1);
        second = first[1].strip(" \t\n");
        first = first[0];
        
        if "URL" in first:
            ServerConfig.URL = second;
        elif "Username" in first:
            ServerConfig.username = second;
        elif "LastQuery" in first:
            ServerConfig.lastQuery = second;
            
        line = file.readline()
            
def ReadBubblesSection(file):
    line = file.readline()
    while line and not ":end" in line:
        spl = line.split(":", 1);
        if "MaxWeight" in spl[0]:
            BubblesConfig.maxWeight = float(spl[1]);
        elif "AccelForce" in spl[0]:
            BubblesConfig.accelForce = float(spl[1]);
        elif "MinAccel" in spl[0]:
            BubblesConfig.minAccel = float(spl[1]);
        elif "PushForce" in spl[0]:
            BubblesConfig.pushForce = float(spl[1]);
        elif "SlowDistance" in spl[0]:
            BubblesConfig.slowDistance = float(spl[1]);
        elif "Drag" in spl[0]:
            BubblesConfig.drag = float(spl[1]);
        elif "MinSize" in spl[0]:
            BubblesConfig.minSize = float(spl[1]);
        elif "MaxSize" in spl[0]:
            BubblesConfig.maxSize = float(spl[1]);
        elif "GrowthSpeed" in spl[0]:
            BubblesConfig.growthSpeed = float(spl[1]) / 1000;
            
        line = file.readline()
    
CONF_PATH = "./Bubblr.conf";
    
if not os.path.isfile(CONF_PATH):
    SaveConfig();
else:
    ReadConfigFile();