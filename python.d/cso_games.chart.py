import json
from third_party.osgi_monitor import OsgiMonitorService

# default module values (can be overridden per job in `config`)
update_every = 15
priority = 60000
retries = 60

# charts order (can be overridden if you want less charts, or different order)
ORDER = ['connections', 'game.participants', 'game.bots']

CHARTS = {
    'connections': {
        'options': [None, 'Connections', 'connections', 'Connections', 'cso.connections', 'area'],
        'lines': [
            ['connection.number.total', 'total'],
            ['auth.user.registry.size', 'authenticated']
        ]},
    'game.participants': {
        'options': [None, 'Participants', 'participants', 'Participants', 'cso.game.participants', 'area'],
        'lines': [
            ['game.service.authz.active', 'active'],
            ['game.service.authz.total', 'total'],
            ['game.service.authz.active.m_5', 'durak'],
            ['game.service.authz.active.m_9', 'gammon'],
            ['game.service.authz.active.m_11', 'poker']
        ]},
    'game.bots': {
        'options': [None, 'Bots', 'bots', 'Bots', 'cso.game.bots', 'area'],
        'lines': [
            ['game.bots.clustered.number', 'total']
        ]},
}

class Service(OsgiMonitorService):
    def __init__(self, configuration=None, name=None):
        OsgiMonitorService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
