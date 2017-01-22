from engine import System
from TestScene import TestScene
from PongScene import PongScene
from GameScene1 import GameScene1
from Intro import Intro
from TextureTestScene import TextureTestScene

system = System()
#scene = TestScene()
#scene = PongScene()
scene = Intro()
system.push_scene(scene)
system.run() # entra no laço principal do jogo
