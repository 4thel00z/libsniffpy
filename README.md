# libsniffpy

## Motivation

I wanted to have a nice cython/python wrapper around [libsniff](https://github.com/4thel00z/libsniff).
This name might confuse you, I just care about sniffing wifi packets from a nic in monitor mode.

## Usage

```python

from sniff import get_socket

# You might have to adjust 
s = get_socket("wlan0mon")
# or whatever big number, forgot how big those frames are lel
pkg = s.recv(3000)
# do some parsing magic, out of scope for this package
```
## License

This project is licensed under the GPL-3 license.
