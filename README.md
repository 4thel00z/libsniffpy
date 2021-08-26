# libsniffpy

![libsniff.png](https://raw.githubusercontent.com/4thel00z/logos/master/libsniff.png)

## Motivation

I wanted to have a nice cython/python wrapper around [libsniff](https://github.com/4thel00z/libsniff).
This name might confuse you, I just care about sniffing wifi packets from a nic in monitor mode.

## Installation

```
pip install libsniffpy
```

## Usage

### Simple: Low level usage

```python

from sniff import get_socket

# You might have to adjust 
s = get_socket("wlan0mon")
# or whatever big number, forgot how big those frames are lel
raw = s.recv(3000)

```

### Advanced: Iterate over the Radiotap frames

```python
from sniff import get_socket, type_predicate, subtype_predicate, loop
from sys import stderr
from dpkt import ieee80211
from dpkt.radiotap import Radiotap

if __name__ == "__main__":
    mgmt_predicate = type_predicate(ieee80211.MGMT_TYPE)
    probe_request_predicate = subtype_predicate(ieee80211.M_PROBE_REQ)

    mgmt_packets = filter(mgmt_predicate, loop("wlan0mon"))
    probe_requests = filter(probe_request_predicate, mgmt_packets)
    
    for pkg in probe_requests:
        print(pkg)
```

## Guidance for n00bs

This lib opens a raw socket for a monitor mode enabled interface.
It needs privs that your user probably don't have.

Either you run this stuff as `root` or you do sth like this:

```
sudo setcap cap_net_raw,cap_net_admin=eip
```

on a wrapper script that calls your python interpreter.

## License

This project is licensed under the GPL-3 license.
