#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009 Adriano Monteiro Marques
#
# Author: Abhiram Kasina <abhiram.casina@gmail.com>
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import sys, os, os.path

import gtk
import gobject
import cairo
import pango
import gobject
import pangocairo


from umit.pm import backend
from umit.pm.gui.widgets.interfaces import InterfacesCombo


import scapy.all
from datetime import datetime

"""
This module contains common classes for the chart drawing
"""

class Chart(gtk.DrawingArea):
    """
    Creates the Message Sequence Chart
    """
    __gtype_name__ = "Chart"
    

    def __init__(self):
        self.IPs = []
        self.start_time = datetime.now()
        self.sniffing_frozen = False
        #add host IP
        #TODO: Need to find a way of finding the IP without using scapy
        for x in scapy.all.conf.route.routes:
            if x[2] != '0.0.0.0':
                self.IPs.append(x[4])
        self.Packets = []
        super(Chart, self).__init__()
        self.connect('expose_event', self.do_expose_event)
   
    def do_expose_event(self, widget, evt):
        self.cr = self.window.cairo_create()
        self.__cairo_draw()
        return gtk.DrawingArea.do_expose_event

    def __cairo_draw(self):
        self.cr.save()
        
        #set background
        self.cr.set_source_rgb(1, 1, 1)
        self.cr.rectangle(0, 0, *self.window.get_size())
        self.cr.fill()
        
        #draw IPs
        self.cr.select_font_face("Georgia",
                cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        self.cr.set_font_size(14)
        i=0
        margin=100
        self.cr.set_source_rgb(0.5, 0.5, 0.5)
        self.cr.move_to(margin-10, 100)
        self.cr.line_to(margin-10, self.window.get_size()[1]-50)
        self.cr.stroke()
        for ip in self.IPs:
            self.cr.set_source_rgb(0.0, 0.0, 0.0)
            x_bearing, y_bearing, width, height = self.cr.text_extents(ip)[:4]
            self.cr.move_to(margin, 100)
            self.cr.show_text(ip)
            self.cr.move_to(margin+width/2, 100+height)
            self.cr.line_to(margin+width/2, self.window.get_size()[1]-50)
            self.cr.stroke()
            margin = margin+width+20
            i=i+1
        self.cr.restore()



    def redraw(self, iface):
        self.__init__()
        self.sniff_context = backend.SniffContext(iface, None, 0, 0, None, 0, 0, 0, \
                                      True, True, True, False, True, True, \
                                      False, 0, True, self.update_drawing_clbk, None)
        self.timeout = gobject.timeout_add(300, self.__check_for_packets)
        self.sniff_context._start()
        
    def stop_sniffing(self):
        self.sniffing_frozen = True
    
    def update_drawing_clbk(self, packet, udata):
        self.__add_packet_to_list(packet.get_source())
        self.__add_packet_to_list(packet.get_dest())   
        if(self.IPs.count(packet.get_source()) >=1 and self.IPs.count(packet.get_dest()) >=1):
            self.Packets.append(packet)
            print str(self.__get_time_passed(packet.get_datetime())) + "ms :: "  + \
                packet.get_source() + "-->" + packet.get_dest()
        
    def __add_packet_to_list(self, address):
        #Add only IP addresses
        if(address == "N/A" or address.find(":") != -1 or len(self.IPs) >= 5):
            return None
        try:
            x = self.IPs.index(address)
        except ValueError:
            self.IPs.append(address)   
            print "(NEW): " + address


    def __check_for_packets(self):
        self.sniff_context.check_finished()
        self.queue_draw()
        if self.sniffing_frozen :
            print "Sniffing Stopped"
            return False
        return True


    def __get_time_passed(self, this_time):
        #print (str((this_time.microsecond - self.start_time.microsecond)) + ":" +str((this_time.second-self.start_time.second)*1000000)  +":" +str((this_time.minute-self.start_time.minute)*60*1000000))
        return (float((this_time.microsecond - self.start_time.microsecond)) + \
                (this_time.second - self.start_time.second)*1000000 + \
                (this_time.minute - self.start_time.minute)*60*1000000)/1000