# Pizza.py toolkit, www.cs.sandia.gov/~sjplimp/pizza.html
# Steve Plimpton, sjplimp@sandia.gov, Sandia National Laboratories
#
# Copyright (2005) Sandia Corporation.  Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
# certain rights in this software.  This software is distributed under
# the GNU General Public License.

# vtk tool

import sys

oneline = "Convert LAMMPS snapshots to VTK format"

docstr = """
v = vtk(d)	        d = object containing atom coords (dump, data)

v.one()                 write all snapshots to tmp.vtk
v.one("new")            write all snapshots to new.vtk
v.many()                write snapshots to tmp0000.vtk, tmp0001.vtk, etc
v.many("new")           write snapshots to new0000.vtk, new0001.vtk, etc
v.single(N)             write snapshot for timestep N to tmp.vtk
v.single(N,"file")      write snapshot for timestep N to file.vtk

  surfaces in snapshot will be written to SURF1.vtk, SURF2.vtk, etc
    where each surface (triangle type) is in a different file
"""

# History
#   8/05, Steve Plimpton (SNL): original version

# ToDo list

# Variables
#   data = data file to read from

# Imports and external programs


# Class definition


class vtk:

    # --------------------------------------------------------------------

    def __init__(self, data):
        self.data = data

    # --------------------------------------------------------------------

    def one(self, *args):
        if len(args) == 0:
            file = "tmp.vtk"
        elif args[0][-4:] == ".vtk":
            file = args[0]
        else:
            file = args[0] + ".vtk"

        n = flag = 0
        which, time, flag = self.data.iterator(flag)
        time, box, atoms, bonds, tris, lines = self.data.viz(which)
        print(time, end=" ")
        sys.stdout.flush()

        if len(tris):
            surface(tris)

        allatoms = []
        for atom in atoms:
            allatoms.append(atom)

        while 1:
            which, time, flag = self.data.iterator(flag)
            if flag == -1:
                break
            time, box, atoms, bonds, tris, lines = self.data.viz(which)

            for atom in atoms:
                allatoms.append(atom)
            print(time, end=" ")
            sys.stdout.flush()
            n += 1

        particle(file, allatoms)
        print("\nwrote %d snapshots to %s in VTK format" % (n, file))

    # --------------------------------------------------------------------

    def many(self, *args):
        if len(args) == 0:
            root = "tmp"
        else:
            root = args[0]

        surfflag = 0
        n = flag = 0
        while 1:
            which, time, flag = self.data.iterator(flag)
            if flag == -1:
                break
            time, box, atoms, bonds, tris, lines = self.data.viz(which)

            if surfflag == 0 and len(tris):
                surfflag = 1
                surface(tris)

            if n < 10:
                file = root + "000" + str(n) + ".vtk"
            elif n < 100:
                file = root + "00" + str(n) + ".vtk"
            elif n < 1000:
                file = root + "0" + str(n) + ".vtk"
            else:
                file = root + str(n) + ".vtk"

            particle(file, atoms)

            print(time, end=" ")
            sys.stdout.flush()
            n += 1

        print("\nwrote %s snapshots in VTK format" % n)

    # --------------------------------------------------------------------

    def single(self, time, *args):
        if len(args) == 0:
            file = "tmp.vtk"
        elif args[0][-4:] == ".vtk":
            file = args[0]
        else:
            file = args[0] + ".vtk"

        which = self.data.findtime(time)
        time, box, atoms, bonds, tris, lines = self.data.viz(which)
        if len(tris):
            surface(tris)
        particle(file, atoms)


# --------------------------------------------------------------------
# write list of triangles into VTK surface files: SURF1.vtk, SURF2.vtk, ...
# all triangles of one type constitute 1 surface = 1 file
# create list of unique vertices (via dictionary) from triangle list


def surface(tris):
    ntypes = tris[-1][1]

    for i in range(ntypes):
        itype = i + 1
        v = {}
        nvert = ntri = 0
        for tri in tris:
            if tri[1] == itype:
                ntri += 1
                vert = (tri[2], tri[3], tri[4])
                if vert not in v:
                    v[vert] = nvert
                    nvert += 1
                vert = (tri[5], tri[6], tri[7])
                if vert not in v:
                    v[vert] = nvert
                    nvert += 1
                vert = (tri[8], tri[9], tri[10])
                if vert not in v:
                    v[vert] = nvert
                    nvert += 1

        keys = list(v.keys())
        vinverse = {}
        for key in keys:
            vinverse[v[key]] = key

        filename = "SURF" + str(itype) + ".vtk"
        f = open(filename, "w")

        print("# vtk DataFile Version 3.0", file=f)
        print("Generated by pizza.py", file=f)
        print("ASCII", file=f)
        print("DATASET POLYDATA", file=f)
        print("POINTS %d float" % nvert, file=f)
        for i in range(nvert):
            tuple = vinverse[i]
            print(tuple[0], tuple[1], tuple[2], file=f)
        print("POLYGONS", ntri, 4 * ntri, file=f)
        for tri in tris:
            if tri[1] == itype:
                vert = (tri[2], tri[3], tri[4])
                ivert1 = v[vert]
                vert = (tri[5], tri[6], tri[7])
                ivert2 = v[vert]
                vert = (tri[8], tri[9], tri[10])
                ivert3 = v[vert]
                print(3, ivert1, ivert2, ivert3, file=f)
        print(file=f)
        print("CELL_DATA", ntri, file=f)
        print("POINT_DATA", nvert, file=f)

        f.close()


# --------------------------------------------------------------------
# write atoms from one snapshot into file in VTK format


def particle(file, atoms):
    f = open(file, "w")

    print("# vtk DataFile Version 2.0", file=f)
    print("Generated by pizza.py", file=f)
    print("ASCII", file=f)
    print("DATASET POLYDATA", file=f)
    print("POINTS %d float" % len(atoms), file=f)
    for atom in atoms:
        print(atom[2], atom[3], atom[4], file=f)
    print("VERTICES", len(atoms), 2 * len(atoms), file=f)
    for i in range(len(atoms)):
        print(1, i, file=f)
    print("POINT_DATA", len(atoms), file=f)
    print("SCALARS atom_type int 1", file=f)
    print("LOOKUP_TABLE default", file=f)
    for atom in atoms:
        itype = int(atom[1])
        print(itype, end=" ", file=f)
    print(file=f)

    f.close()
