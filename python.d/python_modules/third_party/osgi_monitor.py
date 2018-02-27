import json
from bases.FrameworkServices.UrlService import UrlService

# default module values (can be overridden per job in `config`)
update_every = 10
priority = 60000
retries = 60

# default job configuration (overridden by python.d.plugin)
# config = {'local': {
#             'update_every': update_every,
#             'retries': retries,
#             'priority': priority,
#             'url': 'http://localhost/system/monitor?json&vars'
#          }}

class OsgiMonitorService(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)

    def _get_mon_data(self, raw):
        """
        Get monitorables data from data received from http request to Monitorable Service
        FIXME: this code assumes that all monitorable vars have unique ids
        :return: dict
        """
        try:
            parsed = json.loads(raw)
        except:
            return None

        try:
            data = parsed['data']
        except:
            return None

        mon_data = {}
        for d in data:
            for var in d['vars']:
                if var['datatype'] == 'FLOAT':
                    val = int(float(var['value'])*1000)
                elif var['datatype'] == 'INT':
                    val = int(var['value'])
                else:
                    val = var['value']
                mon_data[var['id']] = val

        if len(mon_data) == 0:
            return None
        return mon_data

    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        self.chart_name = self.name

        raw = self._get_raw_data()

        if not raw:
            return None

        return self._get_mon_data(raw)
