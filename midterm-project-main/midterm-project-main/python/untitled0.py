from maze import Action, Maze
from BTinterface import BTInterface
BT = BTInterface("COM10")
a = Maze("data/maze.csv")
b = int(input("enter start node"))
c = int(input("enter end node"))
BT.send_action(a.actions_to_str(a.getActions(a.BFS_2(b,c))))
while True:
    a = BT.get_UID()
    if (a!=0):
        print(a)