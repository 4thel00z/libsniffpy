from libsniff import open_raw
import ctypes
import os
import socket
from sys import stderr
from ctypes.util import find_library
from dpkt import ieee80211
from dpkt.radiotap import Radiotap

__all__ = ("fromfd",)

SO_DOMAIN = getattr(socket, "SO_DOMAIN", 39)
SO_TYPE = getattr(socket, "SO_TYPE", 3)
SO_PROTOCOL = getattr(socket, "SO_PROTOCOL", 38)


_libc_name = find_library("c")
if _libc_name is not None:
    libc = ctypes.CDLL(_libc_name, use_errno=True)
else:
    raise OSError("libc not found")


def _errcheck_errno(result, func, arguments):
    """Raise OSError by errno for -1"""
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return arguments


_libc_getsockopt = libc.getsockopt
_libc_getsockopt.argtypes = [
    ctypes.c_int,  # int sockfd
    ctypes.c_int,  # int level
    ctypes.c_int,  # int optname
    ctypes.c_void_p,  # void *optval
    ctypes.POINTER(ctypes.c_uint32),  # socklen_t *optlen
]
_libc_getsockopt.restype = ctypes.c_int  # 0: ok, -1: err
_libc_getsockopt.errcheck = _errcheck_errno


def _raw_getsockopt(fd, level, optname):
    """Make raw getsockopt() call for int32 optval
    :param fd: socket fd
    :param level: SOL_*
    :param optname: SO_*
    :return: value as int
    """
    optval = ctypes.c_int(0)
    optlen = ctypes.c_uint32(4)
    _libc_getsockopt(fd, level, optname, ctypes.byref(optval), ctypes.byref(optlen))
    return optval.value


def _from_fd(fd, keep_fd=True):
    family = _raw_getsockopt(fd, socket.SOL_SOCKET, SO_DOMAIN)
    typ = _raw_getsockopt(fd, socket.SOL_SOCKET, SO_TYPE)
    proto = _raw_getsockopt(fd, socket.SOL_SOCKET, SO_PROTOCOL)
    if sys.version_info.major == 2:
        # Python 2 has no fileno argument and always duplicates the fd
        sockobj = socket.fromfd(fd, family, typ, proto)
        sock = socket.socket(None, None, None, _sock=sockobj)
        if not keep_fd:
            os.close(fd)
        return sock
    else:
        if keep_fd:
            return socket.fromfd(fd, family, typ, proto)
        else:
            return socket.socket(family, typ, proto, fileno=fd)


def get_socket(iface: str = "wlan0man") -> socket.socket:
    fd = open_raw(iface)
    return _from_fd(fd)


subtypes_management = {
    0: "association-request",
    1: "association-response",
    2: "reassociation-request",
    3: "reassociation-response",
    4: "probe-request",
    5: "probe-response",
    8: "beacon",
    9: "announcement-traffic-indication-message",
    10: "disassociation",
    11: "authentication",
    12: "deauthentication",
    13: "action",
}

subtypes_control = {
    8: "block-acknowledgement-request",
    9: "block-acknowledgement",
    10: "power-save-poll",
    11: "request-to-send",
    12: "clear-to-send",
    13: "acknowledgement",
    14: "contention-free-end",
    15: "contention-free-end-plus-acknowledgement",
}

subtypes_data = {
    0: "data",
    1: "data-and-contention-free-acknowledgement",
    2: "data-and-contention-free-poll",
    3: "data-and-contention-free-acknowledgement-plus-poll",
    4: "null",
    5: "contention-free-acknowledgement",
    6: "contention-free-poll",
    7: "contention-free-acknowledgement-plus-poll",
    8: "qos-data",
    9: "qos-data-plus-contention-free-acknowledgement",
    10: "qos-data-plus-contention-free-poll",
    11: "qos-data-plus-contention-free-acknowledgement-plus-poll",
    12: "qos-null",
    14: "qos-contention-free-poll-empty",
}


def type_predicate(type_id: int):
    def predicate(pkg: Radiotap) -> bool:
        return pkg.data.type == type_id

    return predicate


def subtype_predicate(type_id: int):
    def predicate(pkg: Radiotap) -> bool:
        return pkg.data.subtype == type_id

    return predicate


def loop(iface: str = "wlan0man", size: int = 2034):
    s = get_socket(iface)
    try:
        while True:
            try:
                yield Radiotap(s.recv(size))
            except Exception as err:
                print("[*] Could not decode a packet", err, file=stderr)
    except KeyboardInterrupt:
        print("[*] Closed the loop, through SIGINT", file=stderr)
