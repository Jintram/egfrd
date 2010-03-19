#!/usr/bin/python


import math
import numpy
import scipy.special as special

import string



def minz_j(n):
    
    # This is where GSL switches from taylor expansion to
    # continued fraction;
    #return math.sqrt(10. * (n + 0.5) / numpy.e)
    #
    # However...
    # We can start table interpolation from zero because there is
    # no singularity in bessel_j for z>=0.
    return 0

def minz_y(n):

    #return max(3., n)
    return .5


def maxz_j(n):

    z = (n * n + n + 1) / 1.221e-4

    if z >= 1000:
        z = max(1000, n * n)

    return z


def maxz_y(n):

    # from gsl/special/bessel_y.c:
    #  else if(GSL_ROOT3_DBL_EPSILON * x > (l*l + l + 1.0)) {
    #     int status = gsl_sf_bessel_Ynu_asympx_e(l + 0.5, x, result);
    #     ...
    z = (n * n + n + 1) / 6.06e-6

    # ... but this is usually too big.
    if z >= 2000:
        z = max(2000, n * n)

    return z


def jnyn(n, resolution):

    delta = numpy.pi / resolution
    zTable = numpy.mgrid[min(minz_j(n),minz_y(n)):max(maxz_j(n), maxz_y(n)):delta]

    jTable = numpy.zeros((len(zTable), n+1))
    jdotTable = numpy.zeros((len(zTable), n+1))
    yTable = numpy.zeros((len(zTable), n+1))
    ydotTable = numpy.zeros((len(zTable), n+1))

    for i, z in enumerate(zTable):
        jTable[i], jdotTable[i], yTable[i], ydotTable[i] \
            = special.sph_jnyn(n, z)

    jTable = jTable.transpose()
    jdotTable = jdotTable.transpose()
    yTable = yTable.transpose()
    ydotTable = ydotTable.transpose()
    return zTable, jTable, jdotTable, yTable, ydotTable

def make_table(func, n, z0, z1, tol):

    z = z0

    dz = numpy.pi / 100

    j, jp = func(n, z)
    j_prev = j[n]
    jp_prev = jp[n]
    jpp_prev = 0

    zTable = numpy.array([z, ])
    yTable = numpy.array([j[n], ])

    while z < z1:
        j, jp = func(n, z + dz)
        abs_jpp_norm = abs((jp[n] - jp_prev) * dz)

        if abs_jpp_norm > tol:# or abs(j[n] - j_prev) > tol:
            dz *= .5
            continue 

        z += dz

        zTable = numpy.append(zTable, z)
        yTable = numpy.append(yTable, j[n])

        if abs_jpp_norm < tol * .5:
            dz *= 2

        jpp_prev = abs_jpp_norm
        jp_prev = jp[n]
        #j_prev = j[n]

        #print z, yTable[-1]

    assert len(zTable) == len(yTable)

    return zTable, yTable


def writeHeader(file):

    template = '''

/* Auto-generated by a script.  Do not edit. */

namespace sb_table
{

struct Table
{
    const unsigned int N;
    const double x_start;
    const double delta_x;
    const double* const y;
};
'''

    file.write(template)

def writeFooter(file):

    template = '''
}  // namespace sbjy_table
'''

    file.write(template)

def writeTableArray(file, name, minn, maxn):

    file.write('static const unsigned int %s_min(%d);\n' % (name, minn)) 
    file.write('static const unsigned int %s_max(%d);\n' % (name, maxn)) 
    file.write('static const Table* %s[%d + 1] =\n{\n' % (name, maxn)) 
    #file.write('boost::array<const double**, %d + 1>%s =\n{\n' % (N, name)) 

    for n in range(minn):
        file.write('    0,\n')

    for n in range(minn, maxn+1):
        file.write('    &%s%d,\n' % (name, n))

    file.write('};\n\n')


def writeArray(file, name, table):

    #    head_template = '''
    #static const double %s[2][%d + 1] =
    #{\n'''

    head_template = '''
static const double %s[%d + 1] =
{\n'''

    #array_template = '''{\n%s\n}'''
    number_template = '''    %.18f'''
    foot_template = '''};\n'''

    N = len(table)

    file.write(head_template % (name, N))

    #file.write('    {\n')
    file.write(',\n'.join([number_template % n for n in table]))
    #file.write('    },\n')

    file.write(foot_template)

def writeArrays(file, name, table1, table2):

    #    head_template = '''
    #static const double %s[2][%d + 1] =
    #{\n'''

    head_template = '''
static const double %s[%d + 1] =
{\n'''

    #array_template = '''{\n%s\n}'''
    number_template = '''    %.18e, %.18e'''
    foot_template = '''};\n'''

    # check if len(table1) == len(table2)
    N = len(table1)

    file.write(head_template % (name, N * 2))

    #file.write('    {\n')
    file.write(',\n'.join([number_template % (value, table2[i]) for i, value in enumerate(table1)]))
    #file.write('    },\n')

    file.write(foot_template)


def writeTable(file, name, N, x_start, delta_x):

    struct_template = '''
static const Table %s = { %d, %.18f, %.18f, %s_f };

'''

    file.write(struct_template % (name, N, x_start, delta_x, name))



if __name__ == '__main__':

    import sys

    filename = sys.argv[1]

    file = open(filename, 'w')

    minn_j = 4
    # this should be larger (than maxn_y), but the table bloats.
    maxn_j = 51

    minn_y = 3
    # GSL always uses Olver asymptotic form for n > 40
    maxn_y = 40


    #tolerance = 5e-5
    resolution = 35

    writeHeader(file)

    zTable, jTable, jdotTable, yTable, ydotTable \
        = jnyn(max(maxn_j, maxn_y), resolution)

    delta_z = zTable[1]-zTable[0]

    # j
    for n in range(minn_j, maxn_j + 1):

        #zTable, jTable = make_table(special.sph_jn, n, 
       #                             minz_j(n), maxz_j(n), tolerance)
        #writeArray(file, 'sj_table%d_z' % n, zTable)
        #writeArray(file, 'sj_table%d_f' % n, jTable)
        #writeTable(file, 'sj_table%d' % n, len(zTable))

        start = numpy.searchsorted(zTable, minz_j(n))
        end = numpy.searchsorted(zTable, maxz_j(n))
        z_start = zTable[start]
        j = jTable[n][start:end]
        jdot = jdotTable[n][start:end]
        #writeArray(file, 'sj_table%d_z' % n, z)
        #writeArray(file, 'sj_table%d_f' % n, j)
        writeArrays(file, 'sj_table%d_f' % n, j, jdot)
        writeTable(file, 'sj_table%d' % n, end-start, z_start, delta_z)
        print 'j', n, len(j)

    # y
    for n in range(minn_y, maxn_y + 1):

        #zTable, yTable = make_table(special.sph_yn, n, 
       #                             minz_y(n), maxz_y(n), tolerance)
        #writeArray(file, 'sy_table%d_z' % n, zTable)
        #writeArray(file, 'sy_table%d_f' % n, yTable)
        #writeTable(file, 'sy_table%d' % n, len(zTable))

        start = numpy.searchsorted(zTable, minz_y(n))
        end = numpy.searchsorted(zTable, maxz_y(n))
        #z = zTable[start:end]
        z_start = zTable[start]
        y = yTable[n][start:end]
        ydot = ydotTable[n][start:end]
        #writeArray(file, 'sy_table%d_z' % n, z)
        #writeArray(file, 'sy_table%d_f' % n, y)
        writeArrays(file, 'sy_table%d_f' % n, y, ydot)
        writeTable(file, 'sy_table%d' % n, end-start, z_start, delta_z)

        print 'y', n, len(y)

    writeTableArray(file, 'sj_table', minn_j, maxn_j)
    writeTableArray(file, 'sy_table', minn_y, maxn_y)

    writeFooter(file)

    file.write('\n')

    file.close()

