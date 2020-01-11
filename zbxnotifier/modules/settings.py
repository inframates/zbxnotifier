import keyring


class Settings:
    main_window_title = "RoboAlert 3000"
    main_window_height = 500
    main_window_width = 600

    zabbix_user = "Admina"
    zabbix_password = keyring.get_password("zabbix", "Admin")
    zabbix_url = "http://192.168.1.160"