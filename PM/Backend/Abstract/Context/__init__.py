#!/usr/bin/env python                                   
# -*- coding: utf-8 -*-                                 
# Copyright (C) 2008 Adriano Monteiro Marques           
#                                                       
# Author: Francesco Piccinno <stack.box@gmail.com>      
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

"""
In this module are defined:
    - register_static_context
    - register_timed_context
    - register_send_context
    - register_send_receive_context
    - register_sniff_context

respectively to hook the contexts StaticContext, TimedContext,
SendContext, SendReceiveContext, and SniffContext class creation.

It accepts as argument a BaseContext class objects defined in
Abstact/BaseContext and should return a new class object that
subclass this abstract class passed as argument to be valid.

So in your backend you should override this functions
if you want to customize the base context classes.

See also Scapy directory for reference.
"""

def register_static_context(context_class):
    "Override this to create your own StaticContext"

    print "!! StaticContext not overloaded"
    return context_class

def register_timed_context(context_class):
    "Override this to create your own TimedContext"

    print "!! TimedContext not overloaded"
    return context_class

def register_send_context(context_class):
    "Override this to create your own SendContext"

    print "!! SendContext not overloaded"
    return context_class

def register_send_receive_context(context_class):
    "Override this to create your own SendReceiveContext"

    print "!! SendReceiveContext not overloaded"
    return context_class

def register_sniff_context(context_class):
    "Override this to create your own SniffContext"

    print "!! SniffContext not overloaded"
    return context_class

from PM.Manager.PreferenceManager import Prefs

if Prefs()['backend.system'].value.lower() == 'umpa':
    from PM.Backend.UMPA.Context import *
else:
    from PM.Backend.Scapy.Context import *
