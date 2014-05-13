cdef extern from "unistd.h":
    unsigned int csleep "sleep" (unsigned int seconds) nogil

cdef extern from "stdlib.h":
    long int crandom "random" () nogil
    void srandom(unsigned int seed) nogil

cpdef do_sum(int bound):
    cdef int sum = 0
    cdef int i
    with nogil:
        for i in xrange(bound):
            sum += i
    return sum


cpdef do_sum_sleep(int bound):
    cdef int sum = 0
    cdef int i
    with nogil:
        for i in xrange(bound):
            sum += i

        csleep(1)

        for i in xrange(bound):
            sum += i

    return sum

#cpdef do_rand_sum(
