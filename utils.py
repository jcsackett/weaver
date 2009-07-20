#Set of utilities for weaver. 

class SettingsError(Exception):
    pass

def get_setting(setting_mod, setting_name, transform=lambda x: x):
    setting = getattr(setting_mod, setting_name)
    #if the setting is just a string, we know it stays the same across servers
    if type(setting) == str:
        return transform(setting)
    #tuples, however, mean the setting changes from server to server
    elif type(setting) == tuple:
        setting = dict(
            staging=transform(setting[0]),
            internal=transform(setting[1]),
            production=transform(setting[2]),
        )
        return setting
    else:
        raise SettingsError('Settings must be one of: str, tuple')
