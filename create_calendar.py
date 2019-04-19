#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
# create_calendar.py
Create post size calendar file in Inkscape

Copyright (C) December 08 2018 George Zhang

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import inkex
import simplestyle
import simpletransform
import sys
import math
import copy
import os
import re
import datetime
import calendar
import logging


class CreateCalendar(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option(
            "--yearNumber", action="store", type="int", dest="yearN", default="1")

        logging.basicConfig(level=logging.DEBUG, filename="logging.txt")

    def effect(self):
        PAGE_W = 36
        PAGE_H = 24

        w = PAGE_W
        h = PAGE_H

        self.change_SVG_size(w, h)

        year = self.options.yearN
        month = 1
        width = 9
        height = 8
        # x = 0
        # y = 0
        # self.draw_month(year, month, width, height, x, y)

        i = j = 0
        for month in range(1, 13):
            i = (month-1) % 4
            j = (month-1) / 4 # python 2 only
            x = i * 9
            y = j * 8
            self.draw_month(year, month, width, height, x, y)



        # bk_layer = self.find_create_layer(self.document.getroot(), 'bk_layer')
        #
        # self.draw_grid(bk_layer, 9, 8, 7, 6, 0, 0)
        # self.draw_grid(bk_layer, 9, 8, 7, 6, 18, 0)
        #
        # text_layer = self.find_create_layer(self.document.getroot(),
        #     'text_layer')
        #
        # self.draw_text(text_layer, 9, 8, 7, 6, 0, 0, "1", 0, 0)
        # self.draw_text(text_layer, 9, 8, 7, 6, 0, 0, "2", 1, 0)

    def change_SVG_size(self, width, height):
        ratio = 25.4
        svg_elem = self.document.getroot()

        page_width = width
        page_height = height

        svg_elem.set('width', str(page_width) + 'in')
        svg_elem.set('height', str(page_height) + 'in')
        svg_elem.set('viewBox', '0 0 ' + str(page_width * ratio) + ' '
                     + str(page_height * ratio))

    def draw_SVG_line(self, (x1, y1), (x2, y2), style, name, parent):
        '''style is a dict'''
        line_attribs = {'style': simplestyle.formatStyle(style),
                        inkex.addNS('label', 'inkscape'): name,
                        'd': 'M ' + str(x1) + ',' + str(y1) + ' L' +
                        str(x2) + ',' + str(y2)}
        elm = inkex.etree.SubElement(
            parent, inkex.addNS('path', 'svg'), line_attribs)
        return elm

    def draw_lines(self, layer, width, height):
        line_style = {'stroke': '#000000',
                      'stroke-width': str(self.unittouu('1px')),
                      'fill': 'none'}

        for i in range(1, 4):
            x1_str = str(9 * i) + 'in'
            y1_str = '0.25in'
            y2_str = str(height - 0.25) + 'in'
            x1, x2, y1, y2 = map(
                self.unittouu, [x1_str, x1_str, y1_str, y2_str])
            self.draw_SVG_line((x1, y1), (x2, y2), line_style, 'line', layer)

        for j in range(1, 3):
            x1_str = '0.25in'
            x2_str = str(width - 0.25) + 'in'
            y1_str = str(8 * j) + 'in'
            x1, x2, y1, y2 = map(
                self.unittouu, [x1_str, x2_str, y1_str, y1_str])
            self.draw_SVG_line((x1, y1), (x2, y2), line_style, 'line', layer)

    def draw_grid(self, layer, width, height, num_col, num_row, x, y):
        '''width and height, in in inches, same for x and y'''
        line_style = {'stroke': '#000000',
                      'stroke-width': str(self.unittouu('1px')),
                      'fill': 'none'}

        for i in range(num_col + 1):
            x1_str = str(x + (float(width)/num_col) * i) + 'in'
            x2_str = x1_str
            y1_str = str(y) + 'in'
            y2_str = str(y + height) + 'in'
            x1, x2, y1, y2 = map(
                self.unittouu, [x1_str, x2_str, y1_str, y2_str])
            self.draw_SVG_line((x1, y1), (x2, y2), line_style, 'line', layer)

        for i in range(num_row + 1):
            x1_str = str(x) + 'in'
            x2_str = str(x + width) + 'in'
            y1_str = str(y + (float(height)/num_row) * i) + 'in'
            y2_str = y1_str
            x1, x2, y1, y2 = map(
                self.unittouu, [x1_str, x2_str, y1_str, y2_str])
            logging.debug("%s %s %s %s" % (x1_str, x2_str, y1_str, y2_str))
            logging.debug("%s %s %s %s" % (x1, x2, y1, y2))
            self.draw_SVG_line((x1, y1), (x2, y2), line_style, 'line', layer)


    def draw_month(self, year, month, width, height, x, y):
        '''height and width in inches int
        x and y in inches from top left corner'''
        # num_col = 7
        # num_row = 5
        cal = calendar.Calendar(6) # set Sunday as first day

        width = width - 0.4
        height = height - 0.4
        x = x + 0.2
        y = y + 0.2

        # assert num_row in (4, 5, 6), "num of row should be 4 5 or 6"
        # width_col = float(width) / num_col
        # height_row = float(height) / num_row

        x_month = x + float(width) / 2
        y_month = y
        ratio = 25.4
        x_month_R, y_month_R = (x_month * ratio, y_month * ratio)

        y_month_R += 9.15 + 7 # 7 from observation
        text_layer = self.find_create_layer(self.document.getroot(),
            'text_layer')
        elem = self.draw_month_text(x_month_R, y_month_R, month, year)
        text_layer.append(elem)

        x_dayofweek = x + float(width) / 7.0 / 2
        y_dayofweek = y + 1.35
        x_dayofweek_R, y_dayofweek_R = (x_dayofweek * ratio,
            y_dayofweek * ratio)

        for i in range(7):
            elem = self.draw_weekday_text(x_dayofweek_R, y_dayofweek_R, i)
            text_layer.append(elem)
            x_dayofweek_R += float(width) / 7.0 * ratio

        bk_layer = self.find_create_layer(self.document.getroot(), 'bk_layer')

        num_col = 7
        num_row = len(cal.monthdayscalendar(year, month))

        self.draw_grid(bk_layer, width, height - 1.5, num_col, num_row,
            x, y+1.5)

        cal_matrix = cal.monthdayscalendar(year, month)

        for i in range(num_row):
            for j in range(num_col):
                day_num = cal_matrix[i][j]
                if day_num != 0:
                    self.draw_text(text_layer, width, height - 1.5,
                        num_col, num_row, x, y+1.5, str(day_num), j, i)


    def draw_text(self, layer, width, height, num_col, num_row, x, y,
        name, i, j):
        '''place day number in a monthly grid'''

        x_loc = x + (float(width)/num_col) * i
        y_loc = y + (float(height)/num_row) * j # top left corner

        ratio = 25.4

        x_loc_R = x_loc * ratio
        y_loc_R = y_loc * ratio

        y_loc_R += 6.097  # vertical adjustement, vertical align baseline

        x_loc_R += 2
        y_loc_R += 2  # second adjustment

        elem = self.create_text(x_loc_R, y_loc_R, name)
        layer.append(elem)

    def create_text(self, x, y, name):

        style_d = {'font-size': '6.34px',  # 18 pt
                   'font-family': 'Roboto',
                   #   'text-align': 'center',
                   'text-anchor': 'start',
                   'fill': '#000000',
                   'stroke': 'none',
                   }
        t = inkex.etree.Element('text')
        t.set(inkex.addNS('space', 'xml'), 'preserve')
        t.set('x', str(x))
        t.set('y', str(y))
        t.set('style', simplestyle.formatStyle(style_d))

        sp = inkex.etree.SubElement(t, 'tspan')
        sp.set(inkex.addNS('role', 'sodipodi'), 'line')
        sp.text = name
        return t

    def draw_month_text(self, x, y, month, year):
        month_name_str = ['0', 'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']

        style_d = {'font-size': '12.69px',  # 24 pt
                   'font-family': 'Roboto',
                   #'text-align': 'center',
                   'text-anchor': 'middle',
                   'fill': '#000000',
                   'stroke': 'none',
                   }
        t = inkex.etree.Element('text')
        t.set(inkex.addNS('space', 'xml'), 'preserve')
        t.set('x', str(x))
        t.set('y', str(y))
        t.set('style', simplestyle.formatStyle(style_d))

        sp = inkex.etree.SubElement(t, 'tspan')
        sp.set(inkex.addNS('role', 'sodipodi'), 'line')
        sp.text = month_name_str[month] + ' ' + str(year)
        return t


    def draw_weekday_text(self, x, y, dayofweek):
        dayofweek_str = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday' ]

        style_d = {'font-size': '8.46px',  # 24 pt
                   'font-family': 'Roboto',
                   #'text-align': 'center',
                   'text-anchor': 'middle',
                   'fill': '#000000',
                   'stroke': 'none',
                   }
        t = inkex.etree.Element('text')
        t.set(inkex.addNS('space', 'xml'), 'preserve')
        t.set('x', str(x))
        t.set('y', str(y))
        t.set('style', simplestyle.formatStyle(style_d))

        sp = inkex.etree.SubElement(t, 'tspan')
        sp.set(inkex.addNS('role', 'sodipodi'), 'line')
        sp.text = dayofweek_str[dayofweek][0:3]
        return t

        # day_of_week_str = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
        #     'Thursday', 'Friday', 'Saturday' ]

    def find_create_layer(self, parent, layer_name):
        # this should not be svg:g
        path = '//g[@inkscape:label="%s"]' % layer_name
        path += '|//svg:g[@inkscape:label="%s"]' % layer_name
        el_list = self.document.xpath(path, namespaces=inkex.NSS)
        # inkex.debug(el_list)
        if el_list:
            layer = el_list[0]
            #inkex.debug('this code never execute, why?')
        else:
            layer = inkex.etree.SubElement(parent, 'g')
            layer.set(inkex.addNS('label', 'inkscape'), layer_name)
            layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        return layer

    def create_group(self, group_name):
        group = inkex.etree.Element('g')
        group.set(inkex.addNS('label', 'inkscape'), group_name)
        group.set('fill', 'none')
        return group


if __name__ == '__main__':
    e = CreateCalendar()
    e.affect()
