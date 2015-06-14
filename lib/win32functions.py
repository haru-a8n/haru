# GUI Application automation and testing library
# Copyright (C) 2006 Mark Mc Mahon
# Copyright (C) 2015 Haru A8n
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place,
#    Suite 330,
#    Boston, MA 02111-1307 USA
"""Defines Windows(tm) functions"""

import ctypes

GetSystemMetrics    = ctypes.windll.user32.GetSystemMetrics
MapVirtualKey       = ctypes.windll.user32.MapVirtualKeyW
SendInput           = ctypes.windll.user32.SendInput
SetCursorPos        = ctypes.windll.user32.SetCursorPos
