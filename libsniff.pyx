cdef extern from "deps/libsniff/libsniff.h":
    cpdef int libsniff_open_raw(char *iface)

def open_raw(iface:str) -> int:
    cdef int fd = libsniff_open_raw(iface.encode("UTF-8"))
    if fd == -1:
        raise ValueError("Could not open the socket")
    return fd
