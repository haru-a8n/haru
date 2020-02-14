#Haru Automation#
Windows UI Automation using mostly UIA

##Automate Notepad?
```python
app = haru.App()
app.start('notepad.exe')
notepad = app.Notepad
notepad.edit.type("hello")
notepad.close()
notepad.wait_for(object_type='dialog', caption='Notepad')
notepad.Notepad.DontSave.click()
```


##Installation##
* Download 32-bit version of Python 3.7.4 or newer (tested using Miniconda 3 [Python 3.7.4, 32-bit])  
  * Python 3.8.1 has a bug that prevents using comtypes, see
    * [Cannot Import pywinauto (comtypes passes a union by value)](https://github.com/pywinauto/pywinauto/issues/868)
    * [bpo-16575: Disabled checks for union types being passed by value](https://github.com/python/cpython/pull/17960)
    * Recommend to use Python 3.7.4 
* Create conda environment, open Andaconda prompt and do:
  ```console
    conda create --name haruenv pip python=3.7.4
  ```
  To activate/deactivate do:
  ```console
    conda activate haruenv
    conda deactivate
  ```
* Install comtypes
  * Other Windows OS versions
  ```console
      pip install comtypes
      pip install six
  ```
  * Windows 10 64-bit build 10074 (due to bug, see http://bugs.python.org/issue24127)
  ```console
      python -m pip install comtypes
  ```

##Related projects##
* http://code.google.com/p/swapy/
* http://code.google.com/p/pywinauto/
* http://stackoverflow.com/questions/22198792/create-a-poker-table-scanner
	
