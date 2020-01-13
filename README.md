ZBXNotifier
============

ZBXNotifier is a simple Desktop GUI application for Engineers, who are working with Zabbix and don't have huge fancy
TVs/Monitors to show them what's going on all the time. Sure, they could use email alerting but WTF, it's 2020.

So this small application would solve this issue by monitoring the problems via the Zabbix API, if a new alert is 
created, it will notify the user somehow.

It's written in Python3 and with PyQt5.

Supported platforms and notification methods as of now:
* Windows 10
  * Toast


Some images
===========

![Main](https://github.com/inframates/zbxnotifier/documentation/image1.png)

![Main](https://github.com/inframates/zbxnotifier/documentation/settings.png)

Installation
============
Windows

```
pip install zbxnotifier
```

You can run int from command line, or you can create a shortcut.
Command line: ZBXNotifier.pyw
Shortcut: Create a new shortcut, and add ZBXNotifier.pyw to it.

You might need to set up windows to open .pyw files with Python by default!


