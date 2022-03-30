import json
from graphics import GraphWin, Point, Rectangle, Text
import os
from layout_parts.Widgets.controllers import Calendar
from notifier import NotifyService

##CONSTS
cluster_resolution = 33

class Cluster():
    def __init__(self, anchor : Point, end : Point, display_number : int, x : int, y : int):
        self.row = y
        self.column = x
        self.anchor = anchor
        self.end = end
        self.display_number = display_number

    def out(self):
        return "(" + str(self.anchor.y) + "|" + str(self.anchor.x) + ")-(" + str(self.end.y) + "|" + str(self.end.x) + ")"

    @property
    def gridcoords(self):
        return str(self.row) + "|" + str(self.column)

    def giveWidget(self, obj):
        self.widget = obj

    @property
    def rect(self):
        output = Rectangle(p1=self.anchor, p2=self.end)
        output.setFill("blue")
        return output



class DISPLAY():
    def __init__(self):
        with open(str(os.path.dirname(os.path.abspath(__file__))) + r"/displayarrangement.json", "r") as jfile:
            self.matrix = json.loads(jfile.read())["clusters"]
            height = len(self.matrix)
            width = 0
            for row in self.matrix:
                if len(row) > width:
                    width = len(row)
            print(str(height * cluster_resolution) + "x" + str(width * cluster_resolution))
        self.wallpaper = GraphWin("WallPaper", width=width * cluster_resolution, height=height * cluster_resolution)
        displaycount = 0
        self.clusters = []
        for i in range(height):
            self.clusters.append([None for i in range(width)])
        print("Rows:" + str(len(self.clusters)))
        print("Columns:" + str(len(self.clusters[0])))
        for row in range(height):
            for element in range(width):
                display_id = self.matrix[row][element]
                if display_id > displaycount:
                    displaycount = display_id
                if self.matrix[row][element] == -1:
                    pointAnchor = Point(x = element * cluster_resolution, y = row * cluster_resolution)
                    pointStretcher = Point(x = (element + 1) * cluster_resolution, y = (row + 1) * cluster_resolution)
                    cluster : Cluster = Cluster(anchor = pointAnchor, end = pointStretcher, display_number=display_id, x = element, y = row)
                    self.clusters[row][element] = cluster
                    obj = Rectangle(p1 = pointAnchor, p2 = pointStretcher)
                    obj.setFill("black")
                    obj.draw(self.wallpaper)
                else:
                    pointAnchor = Point(x = element * cluster_resolution, y = row * cluster_resolution)
                    pointStretcher = Point(x = (element + 1) * cluster_resolution, y = (row + 1) * cluster_resolution)
                    obj = Rectangle(p1 = pointAnchor, p2 = pointStretcher)
                    obj.draw(self.wallpaper)
                    cluster : Cluster = Cluster(anchor = pointAnchor, end = pointStretcher, display_number=display_id, x = element, y = row)
                    self.clusters[row][element] = cluster
                    if NotifyService.get("debug.display-show_cluster_coordinates"):
                        txt = Text(p = Point((pointAnchor.x + pointStretcher.x) / 2, (pointAnchor.y + pointStretcher.y) / 2) , text = str(cluster.gridcoords))
                        txt.draw(self.wallpaper)
        if NotifyService.get("debug.display-show_display_boundaries"):
            with open(str(os.path.dirname(os.path.abspath(__file__))) + r"/displayarrangement.json", "r") as jfile:
                for display_coordinates in json.loads(jfile.read())["displays"]:
                    coordinate_one = display_coordinates[0]
                    coordinate_two = display_coordinates[1]
                    startingPoint = Point(x = coordinate_one[0] * cluster_resolution, y = coordinate_one[1] * cluster_resolution)
                    endpoint = Point(x = (coordinate_two[0] + 1) * cluster_resolution, y = (coordinate_two[1] + 1) * cluster_resolution)
                    rect = Rectangle(p1 = startingPoint, p2=endpoint)
                    rect.setOutline("red")
                    rect.draw(self.wallpaper)

    def load_layout(self, name:str):
        currently_loaded_widgets = []
        NotifyService.change("ram.currently_loaded_layout", name)
        with open(str(os.path.dirname(os.path.abspath(__file__))) + r"/layouts.json", "r") as jfile:
            layoutdata = json.loads(jfile.read())[name]
        cluster_map = layoutdata["widget-cluster-map"]
        for widgetname in cluster_map:
            clusters_inhibited = []
            if len(cluster_map[widgetname]["coords"]) / 2 == 1:
                for y in range(cluster_map[widgetname]["coords"][0][0], cluster_map[widgetname]["coords"][1][0] + 1):
                    for x in range(cluster_map[widgetname]["coords"][0][1], cluster_map[widgetname]["coords"][1][1] + 1):
                        selected_cluster : Cluster = self.clusters[y][x]
                        if NotifyService.get("debug.display-show_widget_color"):
                            marker = selected_cluster.rect
                            marker.setFill("Green")
                            marker.draw(self.wallpaper)
                        clusters_inhibited.append(selected_cluster)
            elif len(cluster_map[widgetname]["coords"]) / 2 > 1:
                for i in range(0, len(cluster_map[widgetname]["coords"]) - 1, 2):
                    first_coordinate = cluster_map[widgetname]["coords"][i]
                    second_coordinate = cluster_map[widgetname]["coords"][i+1]
                    for y in range(first_coordinate[0], second_coordinate[0] + 1):
                        for x in range(first_coordinate[1], second_coordinate[1] + 1):
                            selected_cluster : Cluster = self.clusters[y][x]
                            if NotifyService.get("debug.display-show_widget_color"):
                                marker = selected_cluster.rect
                                marker.setFill("blue")
                                marker.draw(self.wallpaper)
                            clusters_inhibited.append(selected_cluster)
            if widgetname == "Calendar":   
                widget : Calendar = Calendar(clusters = clusters_inhibited)
            else:
                widget = None
            for cluster in clusters_inhibited:
                cluster.giveWidget(widget)
            currently_loaded_widgets.append(widget)
        self.currently_loaded_widgets = currently_loaded_widgets
                        
                        
        
            
                    

                

        
