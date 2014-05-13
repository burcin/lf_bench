import time

from lazyflow.request import Request

def lf_req(fn):
    r = Request(fn)
    r.submit()
    return r

def r_bench_factory(fn):
    def time_fn(num_tasks):
        reqs = [lf_req(fn) for i in xrange(num_tasks)]
        for r in reqs:
            r.wait()
    time_fn.__name__ = 'rdo_' + fn.__name__
    return time_fn

def r_bench_factory_latency(fn):
    def time_fn(num_tasks):
        for i in xrange(num_tasks):
            r = Request(fn)
            r.wait()
    time_fn.__name__ = 'rdo_lat_' + fn.__name__
    return time_fn


def g_bench_factory(fn, pool):
    def time_fn(num_tasks):
        reqs = [pool.spawn(fn) for i in xrange(num_tasks)]
        gevent.wait()
    time_fn.__name__ = 'gdo_' + fn.__name__
    return time_fn

def g_bench_factory_latency(fn, pool):
    def time_fn(num_tasks):
        for i in xrange(num_tasks):
            r = pool.spawn(fn)
            r.wait()
    time_fn.__name__ = 'gdo_lat_' + fn.__name__
    return time_fn

        
def bench_factory(fn, pool):
    return r_bench_factory(fn), g_bench_factory(fn, pool)

def bench_factory_latency(fn, pool):
    return r_bench_factory(fn), g_bench_factory(fn, pool)

import multiprocessing
import gevent.threadpool

pool = gevent.threadpool.ThreadPool(multiprocessing.cpu_count())

rdo_nothing, gdo_nothing = bench_factory(lambda : 5, pool)
rdo_sleep, gdo_sleep = bench_factory(lambda : time.sleep(1), pool)
_, gdo_greensleep = bench_factory(lambda : gevent.sleep(1), pool)
rdo_sum, gdo_sum = bench_factory(lambda : sum(xrange(10**7)), pool)

rdo_lat_nothing, gdo_lat_nothing = bench_factory_latency(lambda : 5, pool)
rdo_lat_sleep, gdo_lat_sleep = bench_factory_latency(lambda : time.sleep(1), pool)
_, gdo_lat_greensleep = bench_factory_latency(lambda : gevent.sleep(1), pool)
rdo_lat_sum, gdo_lat_sum = bench_factory_latency(lambda : sum(xrange(10**7)), pool)

from cy_fn import do_sum as cy_do_sum, do_sum_sleep as cy_do_sum_sleep
rdo_nogilsum, gdo_nogilsum = bench_factory(lambda : cy_do_sum(10**8), pool)
rdo_lat_nogilsum, gdo_lat_nogilsum = bench_factory_latency(lambda : cy_do_sum(10**8), pool)
rdo_nogilsumsleep, gdo_nogilsumsleep = \
        bench_factory(lambda : cy_do_sum_sleep(10**8), pool)


def spawn_new_reqs():
    pass
