#Set of utilities for weaver. 

class SettingsError(Exception):
    pass

def get_setting(setting_name, setting_mod, transform=lambda x: x):
    setting = getattr(setting_mod, setting_name)
    if type(setting) == str:
        return transform(setting)
    elif type(setting) == tuple:
        setting = dict(
            staging=transform(setting[0]),
            internal=transform(setting[1]),
            production=transform(setting[2]),
        )
        return setting
    else:
        raise SettingsError('Settings must be one of: str, tuple')
