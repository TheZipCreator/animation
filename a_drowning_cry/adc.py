# acloudyskye - A Drowning Cry
# Animation by TheZipCreator
# open source under GNU GPLv3

from pydub import AudioSegment;
from pydub.playback import play;
import os;
import _thread;
import time;
from curses import wrapper;
import curses;
import math;
import random;
import itertools;
import sys;
import opensimplex;

random.seed(time.time());

song = AudioSegment.from_mp3("song.mp3");
bpm = 90;
offset = 150*1000; # offset from start of song in milliseconds (for debug)
song = song[offset:];
start_time = time.time()-(offset/1000.0);

def beat():
  return (time.time()-start_time)*(bpm/60.0);

def play_song():
  start_time = time.time()-(offset/1000.0);
  play(song);

_thread.start_new_thread(play_song, ());

opensimplex.seed(6502);


def main(s):
  s.clear();
  # init color pairs
  cols = [curses.COLOR_BLACK, curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_YELLOW, curses.COLOR_BLUE, curses.COLOR_MAGENTA, curses.COLOR_CYAN, curses.COLOR_WHITE];
  for i in range(len(cols)):
    for j in range(len(cols)):
      curses.init_pair(i*len(cols)+j+1, cols[i], cols[j]);
  def get_color(i, j):
    return curses.color_pair(i*len(cols)+j+1);
  BLACK = 0;
  RED = 1;
  GREEN = 2;
  YELLOW = 3;
  BLUE = 4;
  MAGENTA = 5;
  CYAN = 6;
  WHITE = 7;

  curses.curs_set(0);
  height, width = s.getmaxyx();
  width -= 1; # for some reason going full width causes a crash
  prevq = 0; # previous quarter note
  preve = 0; # previous eighth note
  if(not curses.has_colors()):
    print("Your terminal does not support color");
    sys.exit(1);
  scene0 = {
    "backcol": get_color(CYAN, BLACK),
  };
  scene1 = {
    "hashes": False,
    "fallers": []
  };
  scene2 = {
    "yoff": 0,
    "zoff": 0,
    "hashes": False
  };
  scene3 = {
    "drops": [],
    "text_x": 0
  };
  scene4 = {
    "col": 1,
    "blocks": [],
    "hashes": False
  };
  scene5 = {
    "col": 1,
    "col2": 2,
    "xoff": 0,
    "m": 1,
    "zoff": 0
  };
  scene6 = {
    "fallers": [],
    "x": 0,
    "y": height,
    "hashes": False,
    "col": 1
  }
  for i in range(30):
    scene4["blocks"].append([[random.randint(0, width-1), random.randint(0, height-1)], [0,0]])
  while True:
    b = (math.floor(beat()*4)/4); # round to nearest quarter note
    b8 = (math.floor(beat()*8)/8); # round to nearest eighth note
    if(-1 < b < 32):
      if(prevq != b):
        #every quarter note
        if(b == 8.25):
          s.addstr(math.floor(height/2), 5, "A Drowning Cry", get_color(WHITE, BLACK));
          scene0["backcol"] = get_color(GREEN, 0);
        elif(b == 16.25):
          s.addstr(math.floor(height/2)+1, 5, "by acloudyskye", get_color(WHITE, BLACK));
          scene0["backcol"] = get_color(CYAN, 0);
        elif(b == 24.25):
          text = "Animation by";
          s.addstr(math.floor(height/2), width-len(text)-5, text, get_color(WHITE, BLACK));
          scene0["backcol"] = get_color(BLUE, 0);
        elif(b == 28.25):
          text = "TheZipCreator";
          s.addstr(math.floor(height/2)+1, width-len(text)-5, text, get_color(WHITE, BLACK));
          scene0["backcol"] = get_color(MAGENTA, 0);
        elif(b == 30.25):
          text = "Running python3 with curses in the terminal";
          s.addstr(math.floor(height/2)+3, math.floor((width/2)-len(text)/2), text, get_color(WHITE, BLACK));
          scene0["backcol"] = get_color(RED, 0);
        for i in itertools.chain(range(10),range(height-10,height)):
          s.addstr(i, 0, chr(random.randint(32, 126))*width, scene0["backcol"]);
        prevq = b;
        s.refresh();
    elif(32 <= b < 64):
      if(b == 32):
        s.clear();
      if(prevq != b):
        prevq = b;
        scene1["hashes"] = not scene1["hashes"];
        hits = [32, 38, 40, 48, 56, 60, 62]
        for i in range(height):
          char = '#' if scene1["hashes"] else '.';
          col = get_color(YELLOW, BLACK) if scene1["hashes"] else get_color(MAGENTA, BLACK);
          for j in range(3):
            s.addstr(i, 1+j, char, col);
            s.addstr(i, (width-4)+j, char, col);
          s.addstr(i, 4, " "*(width-8));
        if(b in hits):
          scene1["fallers"] += [0];
        for (i, f) in enumerate(scene1["fallers"]):
          if(f >= height):
            scene1["fallers"].pop(i);
          else:
            s.addstr(f, 4, "-"*(width-8), get_color(CYAN, BLACK));
            scene1["fallers"][i] = f+1;
        s.refresh();
    elif(64 <= b < 128):
      if(b == 64):
        s.clear();
      if(prevq != b):
        prevq = b;
        scene2["yoff"] -= 2;
        if(b >= 96):
          scene2["hashes"] = not scene2["hashes"];
      if(preve != b8):
        preve = b8;
        hits = [0, 0.5, 0.75, 1, 1.5, 2, 2.25, 2.5, 2.875, 3, 3.25, 3.5, 3.75];
        if(b8%4 in hits):
          scene2["zoff"] += 0.25;
        noiseScale = 0.1;
        for i in range(math.floor(width/7)):
          for j in range(math.floor(height/2)):
            n = opensimplex.noise3(x=i*noiseScale, y=(j+scene2["yoff"])*noiseScale, z=scene2["zoff"]);
            if(n > 0.25):
              s.addstr(j*2, (i*7), "#######" if scene2["hashes"] else "       ", get_color(RED, WHITE));
              s.addstr(j*2+1, (i*7), "#######" if scene2["hashes"] else "       ", get_color(RED, WHITE));
            else:
              s.addstr(j*2, (i*7), "       ", get_color(WHITE, RED));
              s.addstr(j*2+1, (i*7), "       ", get_color(WHITE, RED));
        text = "";
        if(64 < b < 69.5):
          text = "I used to want to fly";
        elif(73 < b < 78):
          text = "I'd jump with all my might";
        elif(81 < b < 85.5):
          text = "Reaching towards the roof";
        elif(88.75 < b < 94):
          text = "To leave this world behind";
        elif(97 < b < 101):
          text = "Framings in the dark";
        elif(105 < b < 110):
          text = "Held a broken light";
        elif(113 < b < 117):
          text = "Keeping in a fight";
        elif(121 < b < 126):
          text = "Struggling as I try";
        if(len(text) > 0):
          s.addstr(math.floor(height/2), math.floor((width/2)-len(text)/2), text, get_color(WHITE, RED));

            
        s.refresh();
    elif(128 <= b < 160):
      if(b == 128):
        s.clear();
      if(preve != b8):
        preve = b8;
        # clear screen with cyan
        for i in range(height):
          s.addstr(i, 0, " "*width, get_color(BLACK, CYAN));
        # each drop is an array containg 1. a string, then 2. an array containg x and y coords
        # e.g. ["|", [2, 3]]
        # a drop with text "|" should appear blue, otherwise red
        for (i, d) in enumerate(scene3["drops"]):
          if(d[1][1] >= height):
            scene3["drops"].pop(i);
          elif(d[1][1] > 0):
            s.addstr(d[1][1], d[1][0], d[0], get_color(BLUE, CYAN) if d[0] == "|" else get_color(RED, CYAN) | curses.A_BOLD);
            scene3["drops"][i][1][1] += 1;
          else:
            scene3["drops"][i][1][1] += 1;
        if(random.random() < 0.5):
          scene3["drops"].append(["|", [random.randint(0, width-1), random.randint(-10, 0)]]);
        # custom text
        # python doesn't have a switch statement. apparently it has match statements but I don't have python 3.10
        # don't know why they just didn't have a switch statement before then, like even C has one
        text = "";
        if(b8 == 130):         text = "where";
        elif(b8 == 130.75):    text = "will";
        elif(b8 == 131+(3/8)): text = "I";
        elif(b8 == 132):       text = "go";
        elif(b8 == 133.5):     text = "when";
        elif(b8 == 134):       text = "I'm";
        elif(b8 == 134+(5/8)): text = "not";
        elif(b8 == 135+(3/8)): text = "around";

        elif(b8 == 137+(4/8)): text = "I'll";
        elif(b8 == 138):       text = "fall";
        elif(b8 == 138+(5/8)): text = "without";
        elif(b8 == 140):       text = "hope";

        elif(b8 == 141+(4/8)): text = "I";
        elif(b8 == 142):       text = "land";
        elif(b8 == 142+(5/8)): text = "with";
        elif(b8 == 143+(2/8)): text = "no";
        elif(b8 == 143+(6/8)): text = "sound";

        elif(b8 == 146):       text = "head";
        elif(b8 == 146+(6/8)): text = "in";
        elif(b8 == 147+(2/8)): text = "your";
        elif(b8 == 148):       text = "arms";

        elif(b8 == 149+(4/8)): text = "I'm";
        elif(b8 == 150):       text = "screaming";
        elif(b8 == 151+(2/8)): text = "out";
        elif(b8 == 152+(6/8)): text = "loud";

        elif(b8 == 154):       text = "gasping";
        elif(b8 == 155+(2/8)): text = "for";
        elif(b8 == 156):       text = "air";
        elif(b8 == 157):       text = "as";
        elif(b8 == 157+(3/8)): text = "I";
        elif(b8 == 158):       text = "fall";
        elif(b8 == 158+(5/8)): text = "through";
        elif(b8 == 159+(2/8)): text = "the";
        elif(b8 == 160):       text = "ground";
        # feels disgusting but it's the only way to do it


        if(text != ""):
          scene3["drops"].append([text, [scene3["text_x"], 0]]);
          scene3["text_x"] += len(text);
          if(scene3["text_x"]+(len(text)*2) >= width):
            scene3["text_x"] = 0;
        
        s.refresh();
    elif(160 <= b < 224 or 241 < b < 256):
      if(b == 160):
        s.clear();
      #c = get_color(BLACK, scene4["col"]);
      if(prevq != b):
        prevq = b;
        hits = [168, 176, 184, 188, 190, 192, 193, 198, 200, 208, 216, 219.75, 222, 224, 241,
                248, 252, 254];
        c = scene4["col"];
        if(b in hits):
          scene4["col"] += 1;
          if(scene4["col"] > len(cols)):
            scene4["col"] = 1; # 1 because 0 is black
        c = scene4["col"] if b%1 == 0 else (scene4["col"]+4)%len(cols);
        if(b%1 == 0):
          maxVel = 0.05;
          for i in range(len(scene4["blocks"])):
            scene4["blocks"][i][1][0] = random.uniform(-maxVel, maxVel);
            scene4["blocks"][i][1][1] = random.uniform(-maxVel, maxVel);
        if(b >= 193):
          scene4["hashes"] = not scene4["hashes"];
      for i in range(height):
        s.addstr(i, 0, ("#" if scene4["hashes"] else " ")*width, get_color(BLACK if c == WHITE else WHITE, c));
      # each block is an array containg 1. a position and 2. a velocity

      for (i, block) in enumerate(scene4["blocks"]):
        if(block[0][0] >= 0 and block[0][0] < width and block[0][1] >= 0 and block[0][1] < height):
          # extra check to make sure the block is still on the screen, to avoid crashing
          s.addstr(math.floor(block[0][1]), math.floor(block[0][0]), " ", get_color(c, (c+2)%len(cols)));
        if(block[0][0] < 0 or block[0][0] >= width):
          scene4["blocks"][i][1][0] *= -1;
        if(block[0][1] < 0 or block[0][1] >= height):
          scene4["blocks"][i][1][1] *= -1;
        scene4["blocks"][i][0][0] += scene4["blocks"][i][1][0];
        scene4["blocks"][i][0][1] += scene4["blocks"][i][1][1];
        scene4["blocks"][i][1][0] *= 0.999;
        scene4["blocks"][i][1][1] *= 0.999;
        #s.addstr(0, 0, "len: "+str(len(scene4["blocks"]))+"     ");
        #s.addstr(i%height, 0, "x: "+str(block[0][0])+" y: "+str(block[0][1])+" vx: "+str(block[1][0])+" vy: "+str(block[1][1]));
      s.refresh();
    elif(224 <= b < 241):
      if(prevq != b):
        prevq = b;
        multipliers = [1.5, 0.5, 2.8, 9.5, 0.2, 5.6, 2.1, 2.1, 0.5];
        index = ((b-1)%2)*4;
        scene5["m"] = multipliers[math.floor(index)];
        if(b%1 == 0 or b%1 == 0.25):
          scene5["col"] = (scene5["col"]+1)%len(cols);
        hits = [230, 232]
        if b in hits:
          scene5["col2"] = (scene5["col2"]+1)%len(cols);
      if(preve != b8):
        preve = b8;
        scene5["zoff"] += 0.1;
        scene5["xoff"] += 1;
      s.clear();
      noiseScale = 0.1;
      for i in range(width):
        h = (math.sin(((((i+scene5["xoff"])*scene5["m"])/width))*(math.pi*2))+1)*(height/2);
        for j in range(height):
          if(j < h):
            s.addstr(height-j-1, i, " ", get_color(BLACK, scene5["col"]));
          else:
            n = opensimplex.noise3(x=(i+(scene5["xoff"]*0.75))*noiseScale, y=j*noiseScale, z=scene5["zoff"]);
            if n > 0.25:
              s.addstr(height-j-1, i, " ", get_color(BLACK, scene5["col2"]));
            else:
              s.addstr(height-j-1, i, " ", get_color(BLACK, WHITE));
      if(b < 225 or b >= 240):
        s.clear();
      s.refresh();
    elif(256 <= b < 360):
      if(prevq != b):
        prevq = b;
        # each scene6 faller contains:
        # 1. a position (x and y)
        # 2. a color
        notes = [0, 0.25, 0.75, 1, 1.5];
        if(b%2 in notes and b < 352):
          scene6["fallers"].append([[scene6["x"], 1], CYAN]);
          scene6["x"] += 7;
          if(scene6["x"]+7 >= width):
            scene6["x"] = 0;
        #s.addstr(0, 0, "length:"+str(len(scene6["fallers"])), get_color(WHITE, BLACK));
        hits = [264, 272, 280, 284, 286, 288, 296, 304, 312, 316, 318, 328, 336, 344];
        if(b in hits):
          for i in range(math.floor(width/7)):
            scene6["fallers"].append([[i*7, 1], (i+scene6["col"])%len(cols)]);
          scene6["col"] += 1;
        if(288 <= b <= 321):
          scene6["hashes"] = not scene6["hashes"];
        for (i, f) in enumerate(scene6["fallers"]):
          for j in range(7):
           s.addstr(f[0][1], f[0][0]+j, "-", get_color(f[1], BLACK));
           s.addstr(f[0][1]-1, f[0][0]+j, " ", get_color(BLACK, BLACK));
          scene6["fallers"][i][0][1] += 1;
          if(f[0][1] >= height):
            scene6["fallers"].pop(i);
            continue;
          #s.addstr(i, 0, "fallers["+str(i)+"] = "+str(scene6["fallers"][i]));
        for i in range(height-3, height):
          s.addstr(i, 0, ("#" if scene6["hashes"] else ".")*width, get_color(YELLOW, BLACK) if scene6["hashes"] else get_color(MAGENTA, BLACK));
        if(b == 357):
          text = "A Drowning Cry";
          s.addstr(math.floor(height/2), math.floor((width/2)-len(text)/2), text, get_color(WHITE, BLACK));
        elif(b == 359):
          text = "by acloudyskye";
          s.addstr(math.floor(height/2)+1, math.floor((width/2)-len(text)/2), text, get_color(WHITE, BLACK));
      s.refresh();
    elif(b < 370):
      x = random.randint(0, width-1);
      y = random.randint(0, height-1);
      s.addstr(y, x, " ", get_color(WHITE, BLACK));
      s.refresh();

    else:
      exit();
          
    
      

wrapper(main);
