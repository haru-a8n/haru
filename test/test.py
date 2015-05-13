import unittest
import sys
sys.path.append('..')
import haru


class HaruTest(unittest.TestCase):
    def test_cwindow_invoke(self):
        robot = haru.Robot()
        robot.start(['notepad'])
        notepad = robot.Notepad
        notepad.edit.type("hello")
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.invoke()

    def test_cwindow_click(self):
        robot = haru.Robot()
        robot.start(['notepad'])
        notepad = robot.Notepad
        notepad.edit.type("hello")
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

if __name__ == '__main__':
    unittest.main()