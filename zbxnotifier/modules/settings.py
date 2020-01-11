from zbxnotifier.modules.zabbix.zabbix import Zabbix


class Settings:
    main_window_title = "RoboAlert 3000"
    main_window_height = 500
    main_window_width = 600
    zbx_api = Zabbix('http://192.168.1.160/', 'Admin', 'zabbix')

