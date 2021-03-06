from layout_parts.Widgets.bodies import BODIES
from layout_parts.Widgets.uNodes.uHead import uHEAD
import time
from layout_parts.Widgets.bodies import BODIES
from layout_parts.Widgets.uNodes.unode_util.decorators import *
from layout_parts.Widgets.uNodes.unode_util.helperclasses import uPoint
from notifier import NotifyService
from layout_parts.Widgets.uNodes.unode_util.helperfunctions import *


class WIDGET():
    def __init__(self, clusters : list, header : str, headercontent : str = None, headershape : str = "rect", settings : dict = None, number : int = None, widgetname : str = "Dummy"):
        t = time.time()
        self.settings  = settings
        self.clusters = clusters
        self.widgetname = widgetname
        self.number = number
        self.head : uHEAD = uHEAD(
            headershape=headershape,
            header = header,
            parentwidget=self,
            headercontent = headercontent if headercontent != None else self.__class__.__name__,
            anchor = self.clusters[0].anchor,
            width = self.clusters[-1].end.x - self.clusters[0].anchor.x,
            height = self.clusters[-1].end.y - self.clusters[0].anchor.y,
            body = getattr(BODIES, self.widgetname.split("_")[0])(self),
            settings = settings
        )
        self.finish(self.settings, self.clusters[0].anchor)
        return

    @n
    def notify_Touched(self):
        self.head.notify_Touched()

    @property
    def drawcalls(self):
        return self.head.draw()
    
    @tlog
    def output(self):
        print(self.widgetname + " (" + str(self.head.anchor.x) + "|" + str(self.head.anchor.y) + ")", end = "")
        print("\n-------------------")
        print("Type" + " " * (100 - len("Type")) + "Depth" + " " + "Constraints")
        self.head.output()
        print(" ")
        if self.head.controlcenter != None:
            print(self.widgetname + ".Controlcenter:")
            self.head.controlcenter.output()
        if self.head.popup != None:
            print(" ")
            print(self.widgetname + ".Popup(" + self.head.popup.__class__.__name__ + ")")
            self.head.popup.output()
        print("----------------------")


    @tlog
    def finish(self, settings, anchor:uPoint):
        wait = self.head.assign_depth(0)
        wait = self.head.constrainmod()
        wait = self.passTreeData()

        if NotifyService.get("debug.widget-output_widget_tree"):
            self.output()
        else:
            print(self.widgetname + " (" + str(self.head.anchor.x) + "|" + str(self.head.anchor.y) + ")", end = "")
            print("*collapsed*")



    @tlog
    def constraincheck(self):
        return self.head.constraincheck(self.head.constraint, 0)

    def passTreeData(self):
        self.head.passTreeData(widgetname = self.widgetname)
