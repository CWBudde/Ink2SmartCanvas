#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Copyright (C) 2012 Karlisson Bezerra, contact@hacktoon.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

from lib import inkex
from lib import simplestyle

class Canvas:
    """Canvas API helper class"""

    def __init__(self, width, height, precision = 2, context = "Context"):
        self.precision = precision
        self.prec = "%." + str(precision) + "f"
        self.obj = context
        self.code = []  #stores the code
        self.style = {}
        self.styleCache = {}  #stores the previous style applied
        self.width = width
        self.height = height
        if not hasattr(self, 'unittouu'): 
            self.unittouu = inkex.unittouu

    def write(self, text):
        self.code.append("  " + text.replace("Context", self.obj) + "\n")

    def output(self):
        from textwrap import dedent
        pas = """  var Canvas := JHTMLCanvasElement(Document.createElement('canvas'));
  Canvas.width := %d;
  Canvas.height := %d;
  var Context := JCanvasRenderingContext2D(Canvas.getContext('2d'));
  %s
"""
        return pas % (self.width, self.height, "".join(self.code))

    def putStyleInCache(self, style):
        #Checks if the last style used is the same or there's no style yet
        for x in style.values():
            if x != "":
                self.styleCache.update(style)
    
    def f2rs(self, value):
        #Round supplied value and convert to string
        rounded = round(value, self.precision) 
        return self.prec % rounded       

    def beginPath(self):
        self.write("Context.beginPath;")

    def createLinearGradient(self, href, x1, y1, x2, y2):
        data = (href, self.f2rs(x1), self.f2rs(y1), self.f2rs(x2), self.f2rs(y2))
        self.write("var %s := Context.createLinearGradient(%s, %s, %s, %s);" % data)

    def createRadialGradient(self, href, cx1, cy1, rx, cx2, cy2, ry):
        data = (href, self.f2rs(cx1), self.f2rs(cy1), self.f2rs(rx), f2rs(cx2), self.f2rs(cy2), self.f2rs(ry))
        self.write("var %s := Context.createRadialGradient(%s, %s, %s, %s, %s, %s);" % data)

    def addColorStop(self, href, pos, color):
        data = (href, self.f2rs(pos), color) 
        self.write("%s.addColorStop(%s, %s);" % data)

    def getColor(self, rgb, a):
        r, g, b = simplestyle.parseColor(rgb)
        a = float(a)
        if a < 1:
            return "'rgba(%d, %d, %d, %s)'" % (r, g, b, self.f2rs(a))
        else:
            return "'#%02x%02x%02x'" % (r, g, b)

    def setOpacity(self, value):
        data = self.f2rs(float(value))
        self.write("Context.globalAlpha := %s;" % data)

    def setFill(self, value):
        try:
            alpha = self.style["fill-opacity"]
        except:
            alpha = 1
        if not value.startswith("url(") and not value.startswith("gradient="):
            fill = self.getColor(value, alpha)
            self.write("Context.fillStyle := %s;" % fill)
        else:
            if value.startswith("gradient="):
                value = value.replace("gradient=", "")
                self.write("Context.fillStyle := %s;" % value)

    def setStroke(self, value):
        try:
            alpha = self.style["stroke-opacity"]
        except:
            alpha = 1
        if not value.startswith("url(") and not value.startswith("gradient="):
            stroke = self.getColor(value, alpha)
            self.write("Context.strokeStyle := %s;" % stroke)
        else:
            if value.startswith("gradient="):
                value = value.replace("gradient=", "")
                self.write("Context.strokeStyle := %s;" % value)

    def setStrokeWidth(self, value):        
        data = self.f2rs(self.unittouu(value))
        self.write("Context.lineWidth := %s;" % data)

    def setStrokeLinecap(self, value):
        self.write("Context.lineCap := '%s';" % value)

    def setStrokeLinejoin(self, value):
        self.write("Context.lineJoin := '%s';" % value)

    def setStrokeMiterlimit(self, value):
        self.write("Context.miterLimit := %s;" % value)

    def setFont(self, value):
        self.write("Context.font := \"%s\";" % value)

    def moveTo(self, x, y):
        data = (self.f2rs(x), self.f2rs(y))
        self.write("Context.moveTo(%s, %s);" % data)

    def lineTo(self, x, y):
        data = (self.f2rs(x), self.f2rs(y))
        self.write("Context.lineTo(%s, %s);" % data)

    def quadraticCurveTo(self, cpx, cpy, x, y):
        data = (self.f2rs(cpx), self.f2rs(cpy), self.f2rs(x), self.f2rs(y))
        self.write("Context.quadraticCurveTo(%s, %s, %s, %s);" % data)

    def bezierCurveTo(self, x1, y1, x2, y2, x, y):
        data = (self.f2rs(x1), self.f2rs(y1), self.f2rs(x2), self.f2rs(y2), self.f2rs(x), self.f2rs(y))
        self.write("Context.bezierCurveTo(%s, %s, %s, %s, %s, %s);" % data)

    def rect(self, x, y, w, h, rx = 0, ry = 0):
        if rx or ry:
            #rounded rectangle, starts top-left counterclockwise
            self.moveTo(x, y + ry)
            self.lineTo(x, y + h - ry)
            self.quadraticCurveTo(x, y+h, x+rx, y+h)
            self.lineTo(x+w-rx, y+h)
            self.quadraticCurveTo(x+w, y+h, x+w, y+h-ry)
            self.lineTo(x+w, y+ry)
            self.quadraticCurveTo(x+w, y, x+w-rx, y)
            self.lineTo(x+rx, y)
            self.quadraticCurveTo(x, y, x, y+ry)
        else:
            data = (self.f2rs(x), self.f2rs(y), self.f2rs(w), self.f2rs(h)) 
            self.write("Context.rect(%s, %s, %s, %s);" % data)

    def arc(self, x, y, r, a1, a2, flag):
        if flag:
          dflag = "True"
        else:
          dflag = "False"  
        data = (self.f2rs(x), self.f2rs(y), self.f2rs(r), self.f2rs(a1), self.f2rs(a2), dflag)
        self.write("Context.arc(%s, %s, %s, %s, %s, %s);" % data)

    def fillText(self, text, x, y):
        data = (text, self.f2rs(x), self.f2rs(y))
        self.write("Context.fillText(\"%s\", %s, %s);" % data)

    def translate(self, cx, cy):
        if (cx != 0.0) and (cy != 0.0): 
            data = (self.f2rs(cx), self.f2rs(cy))
            self.write("Context.translate(%s, %s);" % data)

    def rotate(self, angle):
        if (angle != 0.0): 
            data = self.f2rs(angle)
            self.write("Context.rotate(%s);" % data)

    def scale(self, rx, ry):
        if (rx != 1.0) and (ry != 1.0): 
            data = (self.f2rs(rx), self.f2rs(ry))
            self.write("Context.scale(%s, %s);" % data)

    def transform(self, m11, m12, m21, m22, dx, dy):
        if (m11 == 1.0) and (m12 == 0.0) and (m21 == 0.0) and (m22 == 1.0):
            data = (self.f2rs(dx), self.f2rs(dy)) 
            self.write("Context.translate(%s, %s);" % data)
        elif (dx == 0.0) and (m12 == 0.0) and (m21 == 0.0) and (dy == 0.0):
            data = (self.f2rs(m11), self.f2rs(m22)) 
            self.write("Context.scale(%s, %s);" % data)
        else:    
            data = (self.f2rs(m11), self.f2rs(m12), self.f2rs(m21), self.f2rs(m22), self.f2rs(dx), self.f2rs(dy))
            self.write("Context.transform(%s, %s, %s, %s, %s, %s);" % data)

    def save(self):
        self.write("Context.save;")

    def restore(self):
        self.write("Context.restore;")

    def fill(self):
        if "fill" in self.style and self.style["fill"] != "none":
            self.write("Context.fill;")
        
    def stroke(self):
        if "stroke" in self.style and self.style["stroke"] != "none":
            self.write("Context.stroke;")
        
    def closePath(self, is_closed=False):
        if is_closed:
            self.write("Context.closePath;")
    def clip(self):
        self.write("Context.clip;")
