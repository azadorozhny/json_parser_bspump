#!/usr/bin/env python3
import logging
import datetime

import bspump
import bspump.mongodb
import bspump.common
import bspump.file
import bspump.trigger

###

L = logging.getLogger(__name__)


###


class SamplePipeline(bspump.Pipeline):

    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.build(
            bspump.file.FileJSONSource(
                app, self, config={
                    'path': './data/sample-data.json',
                    'post': 'noop',
                }
            ).on(bspump.trigger.RunOnceTrigger(app)),
            ProcessorParse(app, self),
            bspump.common.PPrintProcessor(app, self),

            # MongoDB sink can accept dict or list of dicts
            bspump.mongodb.MongoDBSink(app, self, 'MongoDBConnection', config={'collection': 'lxc_containers'}),
        )


def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
        except TypeError:  # if state: null
            return None
    return dct


class ProcessorParse(bspump.Processor):

    def __init__(self, app, pipeline):
        super().__init__(app, pipeline)

    def process(self, context, event):
        containers_parsed = []
        for item in event:
            res_dict = {}
            res_dict['name'] = item.get('name')
            res_dict['cpu_usage'] = safeget(item, 'state', 'cpu', 'usage')
            res_dict['memory_usage'] = safeget(item, 'state', 'memory', 'usage')
            # "2020-06-09T14:51:42+02:00"
            res_dict['created_at'] = datetime.datetime.strptime(item.get('created_at'), '%Y-%m-%dT%H:%M:%S%z')
            res_dict['status'] = item.get('status')
            ip_addrs = []
            network = safeget(item, 'state', 'network')
            if network:
                for value in safeget(item, 'state', 'network').values():
                    addrs = value.get('addresses')
                    if addrs:
                        for addr in addrs:
                            ip_addrs.append(addr.get('address'))
                res_dict['IP_addresses'] = ip_addrs
            else:
                res_dict['IP_addresses'] = []

            containers_parsed.append(
                res_dict
            )
        return containers_parsed


if __name__ == '__main__':
    app = bspump.BSPumpApplication()

    svc = app.get_service('bspump.PumpService')

    svc.add_connection(
        bspump.mongodb.MongoDBConnection(app, 'MongoDBConnection')
    )

    # Construct and register Pipeline
    pl = SamplePipeline(app, 'SamplePipeline')
    svc.add_pipeline(pl)

    app.run()
