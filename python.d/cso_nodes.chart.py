import json
from cso_base import CsoService

# default module values (can be overridden per job in `config`)
update_every = 10
priority = 60000
retries = 60

# charts order (can be overridden if you want less charts, or different order)
ORDER = ['datasource.pool', 'datasource.perf', 'conn.service', 'conn.auth', 'auth.service', \
        'game.tables', 'game.authz', 'game.pool', 'game.perf', \
        'game.bots.num', 'game.bots.pool', 'scheduler.pools', \
        'system.heap', 'system.threads']

CHARTS = {
    'system.heap': {
        'options': [None, 'Heap', 'MiB', 'System (heap)', 'cso.sys.heap', 'area'],
        'lines': [
            ['heap.used', 'used'],
            ['heap.max', 'max'],
            ['heap.total', 'total']
        ]},
    'system.threads': {
        'options': [None, 'Threads', 'number', 'System (threads)', 'cso.sys.threads', 'area'],
        'lines': [
            ['thread.count', 'total'],
            ['thread.count.daemon', 'daemon'],
            ['thread.count.peak', 'peak'],
            ['thread.count.started', 'started', 'incremental']
        ]},
    'datasource.pool': {
        'options': [None, 'Connections', 'connections', 'DataSource (pool)', 'cso.datasource.pool', 'area'],
        'lines': [
            ['datasource.pool.busy', 'busy'],
            ['datasource.pool.size', 'size'],
            ['datasource.pool.total', 'pooled']
        ]},
    'datasource.perf': {
        'options': [None, 'Connections/s', 'connections/s', 'DataSource (perf)', 'cso.datasource.perf', 'area'],
        'lines': [
            ['datasource.pool.picked', 'conn/s', 'incremental']
        ]}, 
    'conn.service': {
        'options': [None, 'Connections', 'connections', 'Connections (all)', 'cso.conn.service', 'area'],
        'lines': [
            ['connection.number.total', 'total'],
            ['connection.number.local', 'local']
        ]},
    'conn.auth': {
        'options': [None, 'Connections', 'connections', 'Connections (auth)', 'cso.conn.auth', 'area'],
        'lines': [
            ['offline.user.registry.size', 'offline'],
            ['auth.user.registry.size', 'total'],
            ['local.auth.user.registry.size', 'local']
        ]},
    'auth.service': {
        'options': [None, 'Number', 'number', 'Authentication', 'cso.auth.service', 'area'],
        'lines': [
            ['auth.session.number', 'sessions'],
            ['auth.user.number', 'users']
        ]},
    'game.tables': {
        'options': [None, 'Tables', 'tables', 'Game (tables)', 'cso.game.tables', 'area'],
        'lines': [
            ['game.service.tables.local.active', 'active'],
            ['game.service.tables.total', 'total'],
            ['game.service.tables.local.total', 'local']
        ]},
    'game.authz': {
        'options': [None, 'Participants', 'participants', 'Game (authz)', 'cso.game.authz', 'area'],
        'lines': [
            ['game.service.authz.active', 'active'],
            ['game.service.authz.total', 'total'],
            ['game.service.authz.active.m_5', 'durak']
        ]},
    'game.pool': {
        'options': [None, 'Threads', 'threads', 'Game (pool)', 'cso.game.pool', 'area'],
        'lines': [
            ['game.service.pool.size', 'size'],
            ['game.service.pool.load.avg5min', 'avg5min', 'absolute', 1, 1000]
        ]},
    'game.perf': {
        'options': [None, 'Tasks/s', 'tasks/s', 'Game (perf)', 'cso.game.perf', 'area'],
        'lines': [
            ['game.service.pool.tasks.complete', 'tasks/s', 'incremental']
        ]},
    'game.bots.num': {
        'options': [None, 'Number', 'number', 'Game Bots (num)', 'cso.game.bots.num', 'area'],
        'lines': [
            ['game.bots.local.number', 'local'],
            ['game.bots.clustered.number', 'total']
        ]},
    'game.bots.pool': {
        'options': [None, 'Threads', 'threads', 'Game Bots (pool)', 'cso.game.bots.pool', 'area'],
        'lines': [
            ['game.bots.pool.size', 'size'],
            ['game.bots.pool.load.avg5min', 'avg5min', 'absolute', 1, 1000]
        ]},
    'scheduler.pools': {
        'options': [None, 'Active tasks (5 min average)', 'active tasks 5 min avg', 'Scheduler (pools)', 'cso.scheduler.pools', 'line'],
        'lines': [
            # created dynamically
        ]},
}


class Service(CsoService):
    def __init__(self, configuration=None, name=None):
        CsoService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS

    def check(self):
        """
        Check configuration and dynamically create chart lines data
        :return: boolean
        """
        if not CsoService.check(self):
            return False

        data = self._get_data()
        if data is None:
            return False

        names = []
        for name in data:
            if name.startswith('scheduler.pool.load.avg'):
                names.append(name)
        for name in sorted(names):
            self.definitions['scheduler.pools']['lines'].append([name, name.rsplit('.', 1)[-1], 'absolute', 1, 1000])

        return True
