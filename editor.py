
from mimetypes import init


class Editor:
  def __init__(self):
    self.data = []
    self.pos = 0
    self.end_pos = 0
    self.clipboard = None

  def __str__(self):
    return ''.join([s for s in self.data])

  def append(self, s):
      l = len(s)
      self.data[self.pos:self.end_pos] = list(s)
      self.pos += l
      self.end_pos += l

  def move(self, pos):
      if pos >= len(self.data): 
        return
      self.pos = pos
      self.end_pos = pos

  def forward_delete(self):
      end_pos = self.end_pos
      if self.pos == self.end_pos:
        end_pos = self.pos + 1
      del self.data[self.pos:end_pos]
      self.end_pos = self.pos

  def select(self, start, end):
      if start > end:
          return
      if end >= len(self.data): 
        return
      self.pos = start
      self.end_pos = end

  def cut(self):
      if self.pos >= self.end_pos:
          return
      self.clipboard = self.data[self.pos:self.end_pos]
      del self.data[self.pos:self.end_pos]

  def paste(self):
      if not self.clipboard:
          return
      self.append(self.clipboard)

  def op(self, query):
    if query[0] == "APPEND":
        self.append(query[1])
    if query[0] == "MOVE":
        self.move(int(query[1]))
    if query[0] == "FORWARD_DELETE":
        self.forward_delete()
    if query[0] == "SELECT":
        self.select(int(query[1]), int(query[2]))
    if query[0] == "CUT":
        self.cut()
    if query[0] == "PASTE":
        self.paste()


  def ops(self, queries):
      result = []
      for q in queries:
          self.op(q)
          result.append(self.__str__())
      return result



queries = [
    ["APPEND", "Hey"],                
    ["APPEND", " there"],             
    ["APPEND", "!"]                   
]
e = Editor()
print(e.ops(queries))


queries = [
    ["APPEND", "Hey you"], 
    ["MOVE", "3"], 
    ["APPEND", ","] 
]
e = Editor()
print(e.ops(queries))


queries = [
    ["APPEND", "Hello! world!"], 
    ["MOVE", "5"], 
    ["FORWARD_DELETE"], 
    ["APPEND", ","] 
]
e = Editor()
print(e.ops(queries))



queries = [
    ["APPEND", "!"], 
    ["FORWARD_DELETE"],
    ["MOVE", "0"],
    ["FORWARD_DELETE"],
    ["FORWARD_DELETE"]
]
e = Editor()
print(e.ops(queries))


queries = [
    ["APPEND", "Hello cruel world!"], 
    ["SELECT", "5", "11"],            
    ["APPEND", ","],                                               
    ["SELECT", "5", "12"],           
    ["FORWARD_DELETE"],                                             
    ["SELECT", "4", "6"],             
    ["MOVE", "1"]                     
]
e = Editor()
print(e.ops(queries))


queries = [
    ["APPEND", "Hello, world!"],      
    ["SELECT", "5", "12"],           
    ["CUT"],                                                                
    ["MOVE", "4"],
    ["PASTE"],
    ["PASTE"],
    ["SELECT", "4", "19"],
    ["PASTE"] 
]
e = Editor()
print(e.ops(queries))