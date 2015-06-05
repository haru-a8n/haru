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

import ctypes
from ctypes import c_ushort, c_long, c_ulong, sizeof, alignment, Union
import six


LONG = c_long
WORD = c_ushort
DWORD = c_ulong


class Structure(ctypes.Structure):
    """Override the Structure class from ctypes to add printing and comparison"""
    # ----------------------------------------------------------------
    def __str__(self):
        """Print out the fields of the ctypes Structure
        fields in exceptList will not be printed"""

        lines = []
        for f in self._fields_:
            name = f[0]
            lines.append("%20s\t%s" % (name, getattr(self, name)))

        return "\n".join(lines)

    # ----------------------------------------------------------------
    def __eq__(self, other_struct):
        """return true if the two structures have the same coordinates"""

        if isinstance(other_struct, ctypes.Structure):

            try:
                # pretend they are two structures - check that they both
                # have the same value for all fields
                are_equal = True
                for field in self._fields_:
                    name = field[0]
                    if getattr(self, name) != getattr(other_struct, name):
                        are_equal = False
                        break

                return are_equal

            except AttributeError:
                return False

        if isinstance(other_struct, (list, tuple)):
            # Now try to see if we have been passed in a list or tuple
            # noinspection PyBroadException
            try:
                are_equal = True
                for i, field in enumerate(self._fields_):
                    name = field[0]
                    if getattr(self, name) != other_struct[i]:
                        are_equal = False
                        break
                return are_equal

            except:
                return False

        return False


class HARDWAREINPUT(Structure):
    _pack_ = 2
    _fields_ = [
        # C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4300
        ('uMsg', DWORD),
        ('wParamL', WORD),
        ('wParamH', WORD),
    ]
assert sizeof(HARDWAREINPUT) == 8, sizeof(HARDWAREINPUT)
assert alignment(HARDWAREINPUT) == 2, alignment(HARDWAREINPUT)


# C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4292
class KEYBDINPUT(Structure):
    _pack_ = 2
    _fields_ = [
        # C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4292
        ('wVk', WORD),
        ('wScan', WORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', DWORD),
    ]
assert sizeof(KEYBDINPUT) == 16, sizeof(KEYBDINPUT)
assert alignment(KEYBDINPUT) == 2, alignment(KEYBDINPUT)


# C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4283
class MOUSEINPUT(Structure):
    _pack_ = 2
    _fields_ = [
        # C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4283
        ('dx', LONG),
        ('dy', LONG),
        ('mouseData', DWORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', DWORD),
    ]
assert sizeof(MOUSEINPUT) == 24, sizeof(MOUSEINPUT)
assert alignment(MOUSEINPUT) == 2, alignment(MOUSEINPUT)


# C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4314
# noinspection PyPep8Naming
class UNION_INPUT_STRUCTS(Union):
    _fields_ = [
        # C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4314
        ('mi', MOUSEINPUT),
        ('ki', KEYBDINPUT),
        ('hi', HARDWAREINPUT),
    ]
assert sizeof(UNION_INPUT_STRUCTS) == 24, sizeof(UNION_INPUT_STRUCTS)
assert alignment(UNION_INPUT_STRUCTS) == 2, alignment(UNION_INPUT_STRUCTS)


# C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4310
class INPUT(Structure):
    _pack_ = 2
    _fields_ = [
        # C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4310
        ('type', DWORD),
        # Unnamed field renamed to '_'
        ('_', UNION_INPUT_STRUCTS),
    ]
assert sizeof(INPUT) == 28, sizeof(INPUT)
assert alignment(INPUT) == 2, alignment(INPUT)


# C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4314
# noinspection PyPep8Naming
class UNION_INPUT_STRUCTS(Union):
    _fields_ = [
        # C:/PROGRA~1/MICROS~4/VC98/Include/winuser.h 4314
        ('mi', MOUSEINPUT),
        ('ki', KEYBDINPUT),
        ('hi', HARDWAREINPUT),
    ]
assert sizeof(UNION_INPUT_STRUCTS) == 24, sizeof(UNION_INPUT_STRUCTS)
assert alignment(UNION_INPUT_STRUCTS) == 2, alignment(UNION_INPUT_STRUCTS)


class POINT(Structure):
    _fields_ = [
        # C:/PROGRA~1/MIAF9D~1/VC98/Include/windef.h 307
        ('x', LONG),
        ('y', LONG),
    ]
assert sizeof(POINT) == 8, sizeof(POINT)
assert alignment(POINT) == 4, alignment(POINT)


class RECT(Structure):
    """Wrap the RECT structure and add extra functionality"""
    _fields_ = [
        # C:/PROGRA~1/MIAF9D~1/VC98/Include/windef.h 287
        ('left', LONG),
        ('top', LONG),
        ('right', LONG),
        ('bottom', LONG),
    ]

    def __init__(self, other_rect_or_left=0, top=0, right=0, bottom=0):
        """Provide a constructor for RECT structures
        A RECT can be constructed by:
        - Another RECT (each value will be copied)
        - Values for left, top, right and bottom
        e.g. my_rect = RECT(otherRect)
        or   my_rect = RECT(10, 20, 34, 100)
        """

        super(RECT, self).__init__()
        if isinstance(other_rect_or_left, RECT):
            self.left = other_rect_or_left.left
            self.right = other_rect_or_left.right
            self.top = other_rect_or_left.top
            self.bottom = other_rect_or_left.bottom
        else:
            if six.PY3:
                self.left = other_rect_or_left
                self.right = right
                self.top = top
                self.bottom = bottom
            else:
                self.left = long(other_rect_or_left)
                self.right = long(right)
                self.top = long(top)
                self.bottom = long(bottom)


#    #----------------------------------------------------------------
#    def __eq__(self, otherRect):
#        "return true if the two rectangles have the same coordinates"
#
#        try:
#            return \
#                self.left == otherRect.left and \
#                self.top == otherRect.top and \
#                self.right == otherRect.right and \
#                self.bottom == otherRect.bottom
#        except AttributeError:
#            return False

    # ----------------------------------------------------------------
    def __str__(self):
        """Return a string representation of the RECT"""
        return "(L%d, T%d, R%d, B%d)" % (
            self.left, self.top, self.right, self.bottom)

    # ----------------------------------------------------------------
    def __repr__(self):
        """Return some representation of the RECT"""
        return "<RECT L%d, T%d, R%d, B%d>" % (
            self.left, self.top, self.right, self.bottom)

    # ----------------------------------------------------------------
    def __sub__(self, other):
        """Return a new rectangle which is offset from the one passed in"""
        new_rect = RECT()

        new_rect.left = self.left - other.left
        new_rect.right = self.right - other.left

        new_rect.top = self.top - other.top
        new_rect.bottom = self.bottom - other.top

        return new_rect

    # ----------------------------------------------------------------
    def __add__(self, other):
        """Allow two rects to be added using +"""
        new_rect = RECT()

        new_rect.left = self.left + other.left
        new_rect.right = self.right + other.left

        new_rect.top = self.top + other.top
        new_rect.bottom = self.bottom + other.top

        return new_rect

    # ----------------------------------------------------------------
    def width(self):
        """Return the width of the  rect"""
        return self.right - self.left

    # ----------------------------------------------------------------
    def height(self):
        """Return the height of the rect"""
        return self.bottom - self.top

    # ----------------------------------------------------------------
    def mid_point(self):
        """Return a POINT structure representing the mid point"""
        pt = POINT()
        pt.x = self.left + int(float(self.width()) / 2.)
        pt.y = self.top + int(float(self.height()) / 2.)
        return pt

    # def __hash__(self):
    # 	return hash (self.left, self.top, self.right, self.bottom)

# allow ctypes structures to be pickled
# set struct.__reduce__ = _reduce
# e.g. RECT.__reduce__ = _reduce


def _construct(typ, buf):
    obj = typ.__new__(typ)
    ctypes.memmove(ctypes.addressof(obj), buf, len(buf))
    return obj


def _reduce(self):
    return _construct, (self.__class__, str(buffer(self)))

RECT.__reduce__ = _reduce

assert sizeof(RECT) == 16, sizeof(RECT)
assert alignment(RECT) == 4, alignment(RECT)
