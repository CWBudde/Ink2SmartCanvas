# coding=utf-8
#
# Copyright (C) 2011 Karlisson Bezerra <contact@hacktoon.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Canvas module for ink2canvas extension
"""

from inkex import Color

class Canvas(object):
    """Canvas API helper class"""

    def __init__(self, parent, width, height, precision, context="Context"):
        self.obj = context
        self.code = []  # stores the code
        self.style = {}
        self.styleCache = {}  # stores the previous style applied
        self.parent = parent
        self.width = width
        self.height = height
        self.precision = precision

    def write(self, text):
        self.code.append("\t" + text.replace("Context", self.obj) + "\n")

    def output(self):
        from textwrap import dedent
        pas = """  var Canvas := JHTMLCanvasElement(Document.createElement('canvas'));
          Canvas.width := %d;
          Canvas.height := %d;
          var Context := JCanvasRenderingContext2D(Canvas.getContext('2d'));
          %s
        """
        return dedent(pas) % (self.width, self.height, "".join(self.code))

    def equalStyle(self, style, key):
        """Checks if the last style used is the same or there's no style yet"""
        if key in self.styleCache:
            return True
        if key not in style:
            return True
        return style[key] == self.styleCache[key]

    def beginPath(self):
        self.write("Context.beginPath;")

    def createLinearGradient(self, href, x1, y1, x2, y2):
        data = (href, x1, y1, x2, y2)
        self.write("var %s := Context.createLinearGradient(%f, %f, %f, %f);" % data)

    def createRadialGradient(self, href, cx1, cy1, rx, cx2, cy2, ry):
        data = (href, cx1, cy1, rx, cx2, cy2, ry)
        self.write("var %s = Context.createRadialGradient(%f, %f, %f, %f, %f, %f);" % data)

    def addColorStop(self, href, pos, color):
        self.write("%s.addColorStop(%f, %s);" % (href, pos, color))

    def getColor(self, rgb, alpha):
        return "'{}'".format(str(Color(rgb).to_rgba(alpha)))

    def setGradient(self, href):
        """
        for stop in gstops:
            style = simplestyle.parseStyle(stop.get("style"))
            stop_color = style["stop-color"]
            opacity = style["stop-opacity"]
            color = self.getColor(stop_color, opacity)
            pos = float(stop.get("offset"))
            self.addColorStop(href, pos, color)
        """
        return None  # href

    def setOpacity(self, value):
        self.write("Context.globalAlpha := %.1f;" % float(value))

    def setFill(self, value):
        try:
            alpha = self.style["fill-opacity"]
        except:
            alpha = 1
        if not value.startswith("url("):
            fill = self.getColor(value, alpha)
            self.write("Context.fillStyle = %s;" % fill)

    def setStroke(self, value):
        try:
            alpha = self.style["stroke-opacity"]
        except:
            alpha = 1
        self.write("Context.strokeStyle := %s;" % self.getColor(value, alpha))

    def setStrokeWidth(self, value):
        self.write("Context.lineWidth := %f;" % self.parent.svg.unittouu(value))

    def setStrokeLinecap(self, value):
        self.write("Context.lineCap := '%s';" % value)

    def setStrokeLinejoin(self, value):
        self.write("Context.lineJoin := '%s';" % value)

    def setStrokeMiterlimit(self, value):
        self.write("Context.miterLimit := %s;" % value)

    def setFont(self, value):
        self.write("Context.font := \"%s\";" % value)

    def moveTo(self, x, y):
        self.write("Context.moveTo(%f, %f);" % (round(x, self.precision), round(y, self.precision)))

    def lineTo(self, x, y):
        self.write("Context.lineTo(%f, %f);" % (round(x, self.precision), round(y, self.precision)))

    def quadraticCurveTo(self, cpx, cpy, x, y):
        data = (round(cpx, self.precision), round(cpy, self.precision), round(x, self.precision), round(y, self.precision))
        self.write("Context.quadraticCurveTo(%f, %f, %f, %f);" % data)

    def bezierCurveTo(self, x1, y1, x2, y2, x, y):
        data = (round(x1, self.precision), round(y1, self.precision), round(x2, self.precision), round(y2, self.precision), round(x, self.precision), round(y, self.precision))
        self.write("Context.bezierCurveTo(%f, %f, %f, %f, %f, %f);" % data)

    def rect(self, x, y, w, h, rx=0, ry=0):
        if rx or ry:
            # rounded rectangle, starts top-left anticlockwise
            self.moveTo(x, y + ry)
            self.lineTo(x, y + h - ry)
            self.quadraticCurveTo(x, y + h, x + rx, y + h)
            self.lineTo(x + w - rx, y + h)
            self.quadraticCurveTo(x + w, y + h, x + w, y + h - ry)
            self.lineTo(x + w, y + ry)
            self.quadraticCurveTo(x + w, y, x + w - rx, y)
            self.lineTo(x + rx, y)
            self.quadraticCurveTo(x, y, x, y + ry)
        else:
            self.write("Context.rect(%f, %f, %f, %f);" % (x, y, w, h))

    def arc(self, x, y, r, a1, a2, flag):
        data = (x, y, r, a1, a2, flag)
        self.write("Context.arc(%f, %f, %f, %f, %.8f, %d);" % data)

    def fillText(self, text, x, y):
        self.write("Context.fillText(\"%s\", %f, %f);" % (text, x, y))

    def translate(self, cx, cy):
        self.write("Context.translate(%f, %f);" % (cx, cy))

    def rotate(self, angle):
        self.write("Context.rotate(%f);" % angle)

    def scale(self, rx, ry):
        self.write("Context.scale(%f, %f);" % (rx, ry))

    def transform(self, m11, m12, m21, m22, dx, dy):
        data = (m11, m12, m21, m22, dx, dy)
        self.write("Context.transform(%f, %f, %f, %f, %f, %f);" % data)

    def save(self):
        self.write("Context.save;")

    def restore(self):
        self.write("Context.restore;")

    def closePath(self):
        if "fill" in self.style and self.style["fill"] != "none":
            self.write("Context.fill;")
        if "stroke" in self.style and self.style["stroke"] != "none":
            self.write("Context.stroke;")
