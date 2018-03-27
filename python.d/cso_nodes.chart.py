import json
from third_party.osgi_monitor import OsgiMonitorService

# default module values (can be overridden per job in `config`)
update_every = 10
priority = 60000
retries = 60

# charts order (can be overridden if you want less charts, or different order)
ORDER = ['datasource.pool', 'datasource.perf', 'conn.service', 'conn.auth',
         'conn.service.messages', 'auth.service', 'game.tables',
         'game.authz', 'game.pool', 'game.perf', 'game.bots.num',
         'game.bots.pool', 'tournament.pool', 'tournament.perf',
         'scheduler.pools', 'system.heap', 'system.threads']

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
    'conn.service.messages': {
        'options': [None, 'Connections (messages by service)', 'messages/s', 'Connections (messages)', 'cso.conn.service.msg', 'line'],
        'lines': [
            # created dynamically
        ]},
    'conn.auth': {
        'options': [None, 'Connections', 'connections', 'Connections (auth)', 'cso.conn.auth', 'area'],
        'lines': [
            ['offline.user.registry.size', 'offline'],
            ['auth.user.registry.size', 'total'],
            ['local.auth.user.registry.size', 'local']
        ]},
    'auth.service': {
        'options': [None, 'Authenticated', 'authenticated', 'Authentication', 'cso.auth.service', 'area'],
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
            ['game.service.authz.active.m_5', 'durak'],
            ['game.service.authz.active.m_9', 'gammon'],
            ['game.service.authz.active.m_11', 'poker']
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
        'options': [None, 'Bots', 'bots', 'Game Bots (num)', 'cso.game.bots.num', 'area'],
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
    'tournament.pool': {
        'options': [None, 'Threads', 'threads', 'Tournament (pool)', 'cso.tournament.pool', 'area'],
        'lines': [
            ['tournaments.pool.size', 'size'],
            ['tournaments.pool.load.avg5min', 'avg5min', 'absolute', 1, 1000]
        ]},
    'tournament.perf': {
        'options': [None, 'Tasks/s', 'tasks/s', 'Tournament (perf)', 'cso.tournament.perf', 'area'],
        'lines': [
            ['tournaments.pool.tasks.complete', 'tasks/s', 'incremental']
        ]},
    'scheduler.pools': {
        'options': [None, 'Active tasks (5 min average)', 'active tasks 5 min avg', 'Scheduler (pools)', 'cso.scheduler.pools', 'line'],
        'lines': [
            # created dynamically
        ]},
}

SERVICES = {
    '1': 'connection', '2': 'game', '3': 'user auth', '4': 'user profile', '5': 'instant messaging',
    '6': 'app update', '8': 'money', '12': 'advertisement', '13': 'photo', '15': 'friends',
    '16': 'tournament', '17': 'payment', '18': 'player stats', '25': 'action', '26': 'user career',
}

class Service(OsgiMonitorService):
    def __init__(self, configuration=None, name=None):
        OsgiMonitorService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.created_dims = []
        self.started = False

    def _create_charts(self, data):
        for d in sorted([d for d in data if d.startswith('scheduler.pool.load.avg')]):
            self.definitions['scheduler.pools']['lines'].append([d, d.rsplit('.', 1)[-1], 'absolute', 1, 1000])

    def _update_charts(self, data):
        chart_id = 'conn.service.messages'
        dim_prefix = 'connection.msg.rcvd.svc'
        new_dims = [d for d in data if d.startswith(dim_prefix) and d not in self.created_dims]
        if new_dims:
            if self.started:
                self._line("CHART " + self.chart_name + "." + chart_id)
            for dim in new_dims:
                dim_id = dim.rsplit('.', 1)[-1]
                dim_name = SERVICES[dim_id] if dim_id in SERVICES else dim_id
                dim_params = [dim, dim_name, 'incremental']
                self.definitions[chart_id]['lines'].append(dim_params)
                if self.started:
                    self.dimension(*dim_params)
                self.created_dims.append(dim)

    def _get_data(self):
        data = OsgiMonitorService._get_data(self)
        if data is not None:
            self._update_charts(data)
        return data

    def check(self):
        """
        Check configuration and dynamically create chart lines data
        :return: boolean
        """
        if not OsgiMonitorService.check(self):
            return False

        data = self._get_data()
        if data is None:
            return False

        self._create_charts(data)

        self.started = True

        return True
