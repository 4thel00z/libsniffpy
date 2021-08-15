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

```python

from sniff import get_socket

# You might have to adjust 
s = get_socket("wlan0mon")
# or whatever big number, forgot how big those frames are lel
pkg = s.recv(3000)
# do some parsing magic, out of scope for this package
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
