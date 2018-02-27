import json
from third_party.osgi_monitor import OsgiMonitorService

# default module values (can be overridden per job in `config`)
update_every = 10
priority = 60000
retries = 60

ORDER = ['datasource.pool', 'datasource.perf', 'conn.service', 'conn.auth', 'auth.service', \
        'game.tables', 'game.authz', 'game.pool', 'game.perf', \
        'tournament.pool', 'tournament.perf']

CHARTS = {
    'datasource.pool': {
        'options': [None, 'Connections', 'connections', 'DataSource (pool)', 'ssg.datasource.pool', 'area'],
        'lines': [
            ['datasource.pool.busy', 'busy'],
            ['datasource.pool.size', 'size'],
            ['datasource.pool.total', 'pooled']
        ]},
    'datasource.perf': {
        'options': [None, 'Connections/s', 'connections/s', 'DataSource (perf)', 'ssg.datasource.perf', 'area'],
        'lines': [
            ['datasource.pool.picked', 'conn/s', 'incremental']
        ]}, 
    'conn.service': {
        'options': [None, 'Connections', 'connections', 'Connections (all)', 'ssg.conn.service', 'area'],
        'lines': [
            ['connection.number.total', 'total'],
            ['connection.number.local', 'local']
        ]},
    'conn.auth': {
        'options': [None, 'Connections', 'connections', 'Connections (auth)', 'ssg.conn.auth', 'area'],
        'lines': [
            ['offline.user.registry.size', 'offline'],
            ['auth.user.registry.size', 'total'],
            ['local.auth.user.registry.size', 'local']
        ]},
    'auth.service': {
        'options': [None, 'Authenticated', 'authenticated', 'Authentication', 'ssg.auth.service', 'area'],
        'lines': [
            ['auth.session.number', 'sessions'],
            ['auth.user.number', 'users']
        ]},
    'game.tables': {
        'options': [None, 'Tables', 'tables', 'Game (tables)', 'ssg.game.tables', 'area'],
        'lines': [
            ['game.service.tables.local.active', 'active'],
            ['game.service.tables.total', 'total'],
            ['game.service.tables.local.total', 'local']
        ]},
    'game.authz': {
        'options': [None, 'Participants', 'participants', 'Game (authz)', 'ssg.game.authz', 'area'],
        'lines': [
            ['game.service.authz.active', 'active'],
            ['game.service.authz.total', 'total'],
            ['game.service.authz.active.m_1', 'battleship'],
            ['game.service.authz.active.m_2', 'checkers'],
            ['game.service.authz.active.m_5', 'durak'],
            ['game.service.authz.active.m_6', 'chess'],
            ['game.service.authz.active.m_9', 'gammon'],
            ['game.service.authz.active.m_11', 'poker'],
            ['game.service.authz.active.m_14', 'thousand'],
            ['game.service.authz.active.m_15', 'burkozel']
        ]},
    'game.pool': {
        'options': [None, 'Threads', 'threads', 'Game (pool)', 'ssg.game.pool', 'area'],
        'lines': [
            ['game.service.pool.size', 'size'],
            ['game.service.pool.load.avg5min', 'avg5min', 'absolute', 1, 1000]
        ]},
    'game.perf': {
        'options': [None, 'Tasks/s', 'tasks/s', 'Game (perf)', 'ssg.game.perf', 'area'],
        'lines': [
            ['game.service.pool.tasks.complete', 'tasks/s', 'incremental']
        ]},
    'tournament.pool': {
        'options': [None, 'Threads', 'threads', 'Tournament (pool)', 'ssg.tournament.pool', 'area'],
        'lines': [
            ['tournaments.pool.size', 'size'],
            ['tournaments.pool.load.avg5min', 'avg5min', 'absolute', 1, 1000]
        ]},
    'tournament.perf': {
        'options': [None, 'Tasks/s', 'tasks/s', 'Tournament (perf)', 'ssg.tournament.perf', 'area'],
        'lines': [
            ['tournaments.pool.tasks.complete', 'tasks/s', 'incremental']
        ]},
}


class Service(OsgiMonitorService):
    def __init__(self, configuration=None, name=None):
        OsgiMonitorService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS

