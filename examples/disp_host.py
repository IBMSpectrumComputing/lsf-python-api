from pythonlsf import lsf
import inspect

if __name__ == '__main__':
    if lsf.lsb_init("test") > 0:
        exit - 1;

    for hostInfoEnt in lsf.get_host_info_all():
        attributes = [d for d in dir(hostInfoEnt)
                      if not d.startswith('__')]
        item = {}
        for a in attributes:
            v = getattr(hostInfoEnt, a)
            if not inspect.ismethod(v) and isinstance(v, (int, str, float)):
                item[a] = v
        print(item)