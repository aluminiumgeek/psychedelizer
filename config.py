# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# psychedelizer.0x80.ru
# config.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Application config

import motor

SETTINGS = {
    'upload_tmp': 'public/tmp',
    'saved_files': 'public/content',
    'db': motor.MotorClient().open_sync().psychedelizer,
    'debug': True
}
