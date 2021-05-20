import threading
from queue import Queue
from attr import attrs, attrib
import sys


class ThreadBot(threading.Thread):
    def __init__(self):
        super().__init__(target=self.manage_table)
        self.cutlery = Cutlery(knives=0, forks=0)
        self.tasks = Queue()

    def manage_table(self):
        while True:
            task = self.tasks.get()
            if task == 'prepare table':
                kitchen.give(to=self.cutlery, knives=4, forks=4)
            elif task == 'clear table':
                self.cutlery.give(to=kitchen, knives=4, forks=4)
            elif task == 'shutdown':
                return


@attrs
class Cutlery:
    knives = attrib(default=0)
    forks = attrib(default=0)
    lock = attrib(default=threading.Lock)

    def give(self, to: "Cutlery", knives=0, forks=0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    def change(self, knives, forks):
        # delete this if you need to watch the thread race
        with self.lock():
            self.knives += knives
            self.forks += forks


kitchen = Cutlery(knives=100, forks=100)
bots = [ThreadBot() for _ in range(10)]

for bot in bots:
    for _ in range(int(sys.argv[1])):
        bot.tasks.put("prepare table")
        bot.tasks.put("clear table")
    bot.tasks.put("shutdown")

print("kitchen inventory before service:", kitchen)
for bot in bots:
    bot.start()

for bot in bots:
    bot.join()

print('Kitchen inventory after service:', kitchen)

"""
without with self.lock:
python3 'Example 2-2. ThreadBot programming for table service.py' 100
kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=100, forks=100)

python3 'Example 2-2. ThreadBot programming for table service.py' 10000
kitchen inventory before service: Cutlery(knives=100, forks=100)
Kitchen inventory after service: Cutlery(knives=88, forks=96)

with self.lock():
python3 'Example 2-2. ThreadBot programming for table service.py' 10000
kitchen inventory before service: Cutlery(knives=100, forks=100, lock=<built-in function allocate_lock>)
Kitchen inventory after service: Cutlery(knives=100, forks=92, lock=<built-in function allocate_lock>)

"""
