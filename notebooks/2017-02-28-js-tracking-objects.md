# Tracking Objects
Tracking will involve batch processing coordinates from multiple frames.

## Methodology
- New bee appears
- Create bee object with coordinates and class if identified
- Look at previous 5 classifications once available:
    - If instance of bee class already exists, merge bees
    - If it does not, make this the bee class instance
- Bee aware of when bee was last seen

## Edge Cases

- Awareness of being near to other bees
- Extinction - last seen
- writing out output
- Conflicts with multiple individuals same type
- List types being tracked

    sum_matrix /= n_frames
img = sum_matrix.astype(np.uint8)
cv2.imwrite('bg.png', img)

clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(9,9))
clahe_img = clahe.apply(img)
cv2.imwrite('nighttime10.png', clahe_img)

if frame_counter % frame_bg_sample_freq:
    if sum_matrix_bg is None:
        grey
        sum_matrix = gray.astype(np.float64)
    else:
         sum_matrix += gray.astype(np.float64)
    num_frames_averaged += 1

if frame_counter % num_frames_predict_tags == 0:


from t cimport Bee, point, class_frame

from libc.math cimport sqrt, pow
import math
from libcpp.vector cimport vector

def t1():
    l = []
    for i in range(900000000):
        if i % 2 == 0:
            n = math.sqrt(121)
            l.append(n)
        else:
            n = math.pow(121, 22)
            l.append(n)
    return 11

cpdef t2():
    cdef int i
    cdef double n
    cdef num = 900000000
    cdef vector[double] l
    for i in range(num):
        if i % 2 == 0:
            n = sqrt(121.0)
            l.push_back(n)
        else:
            n = pow(121.0, 22.0)
            l.push_back(n)
    return 11


cpdef double tb(vector[double] vin):
    cdef point c
    point(x=11, y=12, frame_seen=111) #can't convert double to int
    b = Bee(c)

    b.append_point(c)
    print(b.get_path())
    print(b.get_last_frame_seen())

    print(b.get_class_classified())

    b.update_class_classified(200)

    print(b.get_class_classified())

    cdef point c2
    c2 = point(x=vin[0], y=vin[1], frame_seen=3) #can't convert double to int
    b2 = Bee(c2)
    print(b2.get_path())
    print(b2.get_class_classified())

    b2.update_class_classified(5)

    print(b2.get_class_classified())
    return 55











Z and n are the same

row1 = [(38.2, 11.5), (11.2, 22.1)]
row2 = [(15.2, 7.5), (9.2, 3.1)]

np.array([row1, row2], dtype=np.double)

np.array([38.2, 11.5, 11.2, 22.1], dtype=np.double).reshape(-1, 2)

cpdef double t3d (double [:,:,::1] arr):
    return arr[0,0,0]


cpdef double tax(double amount):
    if amount <= 18200:
        return 0
    elif amount <= 37000:
        return 0.19 * (amount - 18200)
    else:
        return 100000

cpdef double tottax(double[:] incomes):
    cdef int i
    cdef int n = incomes.shape[0]
    cdef double tot = 0

    for i in range(n):
        tot += tax(incomes[i])
    return tot

cpdef int multi(int [:,:,:] arr):
    return arr[0][0][0]

cdef extern from "math.h":
    double cos(double x)
    double sin(double x)
    double tan(double x)

def test_trig():
    print(cos(0))



    Cython -a t.pyx

    # cython:profile=True

        pip install Cython
        Pip install easycython

        pyximport

        cython -a hello.pyx

        #import numpy as np
        #x = np.array([100,100,100000]).astype(np.double)

        #double[:,:,:] arr

        #y=np.array([[[1,2],[3,4],[5,6]],[[7,8], [9,10]]])

        with nogil:
            for i in prange(rows_A):
                for j in range(cols_B):
                s = 0
                for k in range(cols_A):
                    s = s + a[i, k] * B[k, j]

                out[i, j] = s

        Cdef int i,b,c



    double[::1] - this is a contiguous 1d buffer of doubles - no steps, next to each other
    cdef int i, n = a.shape[0]
    cdef double s = 0.0
    for i in range(n):
        s+= a[i]

    cdef int[:,:,:] mv # 3d typed memory view
        cdef int a[3][3][3] #c arrays
        a = np.zeros((10,20,30), dtype=np.int32)

        indexing like numpy but faster
        mv[1,2,0]

        slicing like numpy but faster
        mv[10] == mv[10,:,:] == mv[10,...]

        arr[:, :, ::1] # only works with continuous buffers
        c_contig = np.zeros((10, 20,30), dtype=int)





        cdef class Particicle(object):
        	cdef float pan[3], vel[3]
        	cdef int id

        Cdef list names: python knows its a statically typed list - more efficient
        names.append - cython knows

        Cdef dict name_to_id = {}

        Cdef object o





    def: available to python + cython
    cdef: fast, local to current file
    cpdef: locally c, externally python

    def distance(x, y):
        return np.sum((x-y)**2)

    cdef float distance(float *x, float *y, int n):
        cdef:
            int i
            float d = 0.0
        for i in range(n):
            d += (x[i] - y[i])**2
        return d

    cpdef float distance([:] x, float[:] y):
        cdef int i
        cdef int n = x.shape[0]
        cdef float d = 0.0
        for i in range(n):
            d += (x[i] - y[i])**2
        return d

        import numpy as np
        c_contig = np.zeros((10, 20,30), dtype=np.double)
        c_contig[0,0,0]=55.2
        import hello
        hello.t3d(c_contig)


    typed memoryviews allos efficient arrays

    pass a = arange(1e6)

    double[::1] - this is a contiguous 1d buffer of doubles - no steps, next to each other
    cdef int i, n = a.shape[0]
    cdef double s = 0.0
    for i in range(n):
        s+= a[i]

    cdef int[:,:,:] mv # 3d typed memory view
        cdef int a[3][3][3] #c arrays
        a = np.zeros((10,20,30), dtype=np.int32)

        indexing like numpy but faster
        mv[1,2,0]

        slicing like numpy but faster
        mv[10] == mv[10,:,:] == mv[10,...]

        arr[:, :, ::1] # only works with continuous buffers
        c_contig = np.zeros((10, 20,30), dtype=int)


        



from libcpp.vector cimport vector
from libc.math cimport sqrt, pow
import math

DEF PI = 3.14159265

ctypedef struct pointf:
    float x
    float y
    int frame_seen

ctypedef struct classified_frame:
    int classified
    int frame_classified


cdef pointf zz = pointf(1.1, 2.2, 11)
cdef pointf zz = pointf(x=1.1, y=2.2, frame_seen=11)
structs can also be assigned from a python dictionary

cdef unsigned int i, n = 200


cdef class Bee:
    cdef:
        vector[point] path
        vector[class_frame] classifications
        int class_classified

    def __cinit__(self, point p):
        self.class_classified = 0
        self.path.push_back(p)

    cdef void append_point(self, point p):
        self.path.push_back(p)

    cdef vector[point] get_path(self):
        return self.path

    cdef point get_last_frame_seen(self):
        return self.path.back()

    cdef int get_last_frame_classified(self):
        return self.classifications.back().frame_classified

    cdef int get_class_classified(self):
        return self.class_classified

    cdef void update_class_classified(self, int new_class):
        self.class_classified = new_class



def t1():
    l = []
    for i in range(900000000):
        if i % 2 == 0:
            n = math.sqrt(121)
            l.append(n)
        else:
            n = math.pow(121, 22)
            l.append(n)
    return 11

cpdef t2():
    cdef int i
    cdef double n
    cdef num = 900000000
    cdef vector[double] l
    for i in range(num):
        if i % 2 == 0:
            n = sqrt(121.0)
            l.push_back(n)
        else:
            n = pow(121.0, 22.0)
            l.push_back(n)
    return 11


cpdef double tb(vector[double] vin):
    cdef point c
    c.x = 11
    c.y = 12
    c.frame_seen = 111
    b = Bee(c)

    b.append_point(c)
    print(b.get_path())
    print(b.get_last_frame_seen())

    print(b.get_class_classified())

    b.update_class_classified(200)

    print(b.get_class_classified())

    cdef point c2
    c2.x = vin[0]
    c2.y = vin[1]
    c2.frame_seen = 3 #can't convert double to int
    b2 = Bee(c2)
    print(b2.get_path())
    print(b2.get_class_classified())

    b2.update_class_classified(5)

    print(b2.get_class_classified())
    return 55


#cpdef vector[double] tt (vector[vector[double]] vect):



'''
cpdef vector[double] tt (vector[vector[double]] vect):
    #vect.push_back(i)
    return vect[0];


cdef vector[int] vect
cdef int i
for i in range(10):
    vect.push_back(i)
for i in range(10):
    print vect[i]
'''

#ctypedef pointf point
#ctypedef classified_frame class_frame

python setup.py build_ext --inplace


cdef unsigned int i, n = 200



cdef pointf zz = pointf(1.1, 2.2, 11)
cdef pointf zz = pointf(x=1.1, y=2.2, frame_seen=11)
structs can also be assigned from a python dictionary



