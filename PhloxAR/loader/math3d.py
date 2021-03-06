#!/usr/bin/env python
#
# Copyright (c) 2006 alex Holkner
# alex.Holkner@mail.google.com
#
# Copyright (c) 2016 Matthias Y. Chen
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTabILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, boston, MA  02110-1301 USA

from __future__ import division, print_function
from __future__ import absolute_import, unicode_literals
import math
import operator
import types


__all__ = [
    'vec2', 'vec3', 'mat4', 'mat3', 'Vector2', 'Vector3', 'Matrix3', 'Matrix4',
    'Point3', 'Point2', 'Ray3', 'Ray2', 'Circle', 'Sphere', 'LineSegment3',
    'LineSegment2', 'Plane'
]


class Vector2(object):
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __repr__(self):
        return '<Vector2(%.2f, %.2f)>'% (self._x, self._y)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self._x == other.x and self._y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self._x != 0 or self._y != 0

    def __len__(self):
        return 2

    def __getitem__(self, key):
        return (self._x, self._y)[key]

    def __setitem__(self, key, value):
        l = [self._x, self._y]
        l[key] = value
        self._x, self._y = l

    def __iter__(self):
        return iter((self._x, self._y))

    def __getattr__(self, key):
        try:
            return tuple([(self._x, self._y)['xy'.index(c)] for c in key])
        except ValueError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if len(key):
            object.__setattr__(self, key, value)
        else:
            try:
                l = [self._x, self._y]
                for k, v in map(None, key, value):
                    l['xy'.index(k)] = v
                self._x, self._y = l
            except ValueError:
                raise AttributeError(key)

    def __add__(self, other):
        if isinstance(other, Vector2):
            if self.__class__ is other.__class__:
                _class = Vector2
            else:
                _class = Point2

            return _class(self._x + other.x, self._y + other.y)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(self._x + other[0], self._y + other[1])

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self._x += other.x
            self._y += other.y
        else:
            self.x += other[0]
            self.y += other[1]

        return self

    def __sub__(self, other):
        if isinstance(object, Vector2):
            if self.__class__ is other.__class__:
                _class = Vector2
            else:
                _class = Point2
            return _class(self._x - other.x, self._y - other.y)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(self._x - other[0], self._y - other[1])

    def __rsub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(other.x - self._x, other.y - self._y)

        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(other.x - self[0], other.y - self[1])

    def __mul__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(self._x * other, self._y * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        assert type(other) in (int, long, float)
        self._x *= other
        self._y *= other

        return self

    def __div__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.div(self._x, other), operator.div(self._y, other))

    def __rdiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.div(other, self._x), operator.div(other, self._y))

    def __floordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.floordiv(self._x, other),
                       operator.floordiv(self._y, other))

    def __rfloordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.floordiv(other, self._x),
                       operator.floordiv(other, self._y))

    def __truediv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.truediv(self._x, other),
                       operator.truediv(self._y, other))

    def __rtruediv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.truediv(other, self._x),
                       operator.truediv(other, self._y))

    def __neg__(self):
        return Vector2(-self._x, -self._y)

    @property
    def copy(self):
        return self.__class__(self._x, self._y)

    @property
    def magnitude(self):
        return math.sqrt(self._x**2 + self._y**2)

    def magnitude_squared(self):
        return self._x**2 + self._y**2

    def normalize(self):
        d = self.magnitude
        if d:
            self._x /= d
            self._y /= d
        return self

    def normalized(self):
        d = self.magnitude
        if d:
            return Vector2(self._x / d, self._y / d)
        return self.copy

    def dot(self, other):
        assert isinstance(other, Vector2)
        return self._x * other.x + self._y * other.y

    # to improve
    def cross(self, other):
        return Vector3(0, 0, self._x * other.y - self._y * other.x)

    def reflect(self, normal):
        # assume normal is normalized
        assert isinstance(normal, Vector2)
        d = 2 * (self.x * normal.x + self.y * normal.y)
        return Vector2(self.x - d * normal.x, self.y - d * normal.y)

    def angle(self, other):
        return math.acos(self.dot(other) / self.magnitude)

    def project(self, other):
        n = other.normalized()
        return self.dot(n) * n

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val


class Vector3(object):
    def __init__(self, x=0, y=0, z=0):
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self):
        return '<Vector3 (%.2f, %.2f, %.2f)>' % (self._x, self._y, self._z)

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return (self._x == other.x and self.y == other.y and
                    self.z == other.z)
        else:
            assert hasattr(other, '__len__') and len(other) == 3
            return (self.x == other[0] and self.y == other[1] and
                   self.z == other[2])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self._x !=0 or self._y != 0 or self._z != 0

    def __len__(self):
        return 3

    def __getitem__(self, key):
        return (self._x, self._y, self._z)[key]

    def __setitem__(self, key, value):
        l = [self._x, self._y, self._z]
        l[key] = value
        self.x, self.y, self.z = l

    def __iter__(self):
        return iter((self._x, self._y, self._z))

    def __getattr__(self, item):
        try:
            return tuple([(self._x, self._y, self._z)['xyz'.index(c)] for c in item])
        except ValueError:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        if len(key) == 1:
            object.__setattr__(self, key, value)
        else:
            try:
                l = [self._x, self._y, self._z]
                for k, v in map(None, key, value):
                    l['xyz'.index(k)] = v
                self._x, self._y, self._z = l
            except ValueError:
                raise AttributeError(key)

    def __add__(self, other):
        if isinstance(other, Vector3):
            if self.__class__ is other.__class__:
                _class = Vector3
            else:
                _class = Point3
            return _class(self._x + other.x, self._y + other.y, self._z + other.z)
        else:
            assert hasattr(other, '__len__') and len(other) == 3
        return Vector3(self._x + other[0], self._y + other[1], self._z + other[2])

    def __iadd__(self, other):
        if isinstance(other, Vector3):
            self._x += other.x
            self._y += other.y
            self._z += other.z
        else:
            self._x += other[0]
            self._y += other[1]
            self._z += other[2]
        return self

    def __sub__(self, other):
        if isinstance(other, Vector3):
            if self.__class__ is other.__class__:
                _class = Vector3
            else:
                _class = Point3
            return Vector3(self._x - other.x, self._y - other.y, self._z - other.z)
        else:
            assert hasattr(other, '__len__') and len(other) == 3
            return Vector3(self._x - other[0], self._y - other[1], self._z - other[2])

    def __rsub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(other.x - self._x, other.y - self._y, other.z - self._z)
        else:
            assert hasattr(other, '__len__') and len(other) == 3
            return Vector3(other._x - self[0], other._y - self[1], other._z - self[2])

    def __mul__(self, other):
        if isinstance(other, Vector3):
            # TODO component-wise mul/div in-place and on Vector2; docs.
            if self.__class__ is Point3 or other.__class__ is Point3:
                _class = Point3
            else:
                _class = Vector3
            return _class(self._x * other.x, self._y * other.y, self._z * other.z)
        else:
            assert type(other) in (int, long, float)
            return Vector3(self._x * other,
                           self._y * other,
                           self._z * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        assert type(other) in (int, long, float)
        self._x *= other
        self._y *= other
        self._z *= other
        return self

    def __div__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(operator.div(self._x, other), operator.div(self._y, other),
                       operator.div(self._z, other))

    def __rdiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(operator.div(other, self._x), operator.div(other, self._y),
                       operator.div(other, self._z))

    def __floordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(operator.floordiv(self._x, other),
                       operator.floordiv(self._y, other),
                       operator.floordiv(self._z, other))

    def __rfloordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(operator.floordiv(other, self._x),
                       operator.floordiv(other, self._y),
                       operator.floordiv(other, self._z))

    def __truediv__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(operator.truediv(self._x, other),
                       operator.truediv(self._y, other),
                       operator.truediv(self._z, other))

    def __rtruediv__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(operator.truediv(other, self._x),
                       operator.truediv(other, self._y),
                       operator.truediv(other, self._z))

    def __neg__(self):
        return Vector3(-self._x, -self._y, -self._z)

    @property
    def copy(self):
        return self.__class__(self._x, self._y, self._z)

    @property
    def magnitude(self):
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @property
    def magnitude_squared(self):
        return self._x ** 2 + self._y ** 2 + self._z ** 2

    def normalize(self):
        d = self.magnitude
        if d:
            self._x /= d
            self._y /= d
            self._z /=d
        return self

    def normalized(self):
        d = self.magnitude
        if d:
            Vector3(self._x / d, self._y / d, self._z / d)
        return self.copy

    def dot(self, other):
        assert isinstance(other, Vector3)
        return self._x * other.x + self._y * other.y + self._z * other.z

    def cross(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self._y * other.z - self._z * other.y,
                       self._z * other.x - self._x * other.z,
                       self._x * other.y - self._y * other.x)

    def reflect(self, normal):
        # assume normal is normalized
        assert isinstance(normal, Vector3)
        d = 2 * (self.x * normal.x + self.y * normal.y + self.z * normal.z)
        return Vector3(self.x - d * normal.x,
                       self.y - d * normal.y,
                       self.z - d * normal.z)

    def rotate_around(self, axis, theta):
        """
        Return the vector rotated around axis through angle theta. Right hand rule applies"""

        # adapted from equations published by Glenn Murray.
        # http://inside.mines.edu/~gmurray/ArbitraryAxisRotation/ArbitraryAxisRotation.html
        x, y, z = self._x, self._y, self._z
        u, v, w = axis.x, axis.y, axis.z

        # Extracted common factors for simplicity and efficiency
        r2 = u ** 2 + v ** 2 + w ** 2
        r = math.sqrt(r2)
        ct = math.cos(theta)
        st = math.sin(theta) / r
        dt = (u * x + v * y + w * z) * (1 - ct) / r2
        return Vector3((u * dt + x * ct + (-w * y + v * z) * st),
                       (v * dt + y * ct + (w * x - u * z) * st),
                       (w * dt + z * ct + (-v * x + u * y) * st))

    def angle(self, other):
        return math.acos(self.dot(other) / (self.magnitude * other.magnitude))

    def project(self, other):
        n = other.normalized()
        return self.dot(n) * n

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, val):
        self._z = val


class Matrix3(object):
    """
    a b c
    e f g
    i j k
    """
    a = b = c = e = f = g = i = j = k = 0

    def __init__(self):
        self.a = self.f = self.k = 1
        self.b = self.c = self.e = self.g = self.i = self.j = 0

    def __repr__(self):
        return ('<Matrix3>\n[% 8.2f % 8.2f % 8.2f\n % 8.2f % 8.2f % 8.2f\n'
                ' % 8.2f % 8.2f % 8.2f]') % (self.a, self.b, self.c, self.e,
                                             self.f, self.g, self.i, self.j,
                                             self.k)

    def __getitem__(self, key):
        return [self.a, self.e, self.i,
                self.b, self.f, self.j,
                self.c, self.g, self.k][key]

    def __setitem__(self, key, value):
        l = self[:]
        l[key] = value
        (self.a, self.e, self.i, self.b, self.f, self.j,
         self.c, self.g, self.k) = l

    def __mul__(self, other):
        if isinstance(other, Matrix3):
            # Caching repeatedly accessed attributes in local variables
            # apparently increases performance by 20%.  Attrib: Will McGugan.
            aa = self.a
            ab = self.b
            ac = self.c
            ae = self.e
            af = self.f
            ag = self.g
            ai = self.i
            aj = self.j
            ak = self.k
            ba = other.a
            bb = other.b
            bc = other.c
            be = other.e
            bf = other.f
            bg = other.g
            bi = other.i
            bj = other.j
            bk = other.k
            c = Matrix3()
            c.a = aa * ba + ab * be + ac * bi
            c.b = aa * bb + ab * bf + ac * bj
            c.c = aa * bc + ab * bg + ac * bk
            c.e = ae * ba + af * be + ag * bi
            c.f = ae * bb + af * bf + ag * bj
            c.g = ae * bc + af * bg + ag * bk
            c.i = ai * ba + aj * be + ak * bi
            c.j = ai * bb + aj * bf + ak * bj
            c.k = ai * bc + aj * bg + ak * bk
            return c
        elif isinstance(other, Point2):
            a = self
            b = other
            p = Point2(0, 0)
            p.x = a.a * b.x + a.b * b.y + a.c
            p.y = a.e * b.x + a.f * b.y + a.g
            return p
        elif isinstance(other, Vector2):
            a = self
            b = other
            v = Vector2(0, 0)
            v.x = a.a * b.x + a.b * b.y
            v.y = a.e * b.x + a.f * b.y
            return v
        else:
            other = other.copy()
            other._apply_transform(self)
            return other

    def __imul__(self, other):
        assert isinstance(other, Matrix3)
        # Cache attributes in local vars (see Matrix3.__mul__).
        aa = self.a
        ab = self.b
        ac = self.c
        ae = self.e
        af = self.f
        ag = self.g
        ai = self.i
        aj = self.j
        ak = self.k
        ba = other.a
        bb = other.b
        bc = other.c
        be = other.e
        bf = other.f
        bg = other.g
        bi = other.i
        bj = other.j
        bk = other.k
        self.a = aa * ba + ab * be + ac * bi
        self.b = aa * bb + ab * bf + ac * bj
        self.c = aa * bc + ab * bg + ac * bk
        self.e = ae * ba + af * be + ag * bi
        self.f = ae * bb + af * bf + ag * bj
        self.g = ae * bc + af * bg + ag * bk
        self.i = ai * ba + aj * be + ak * bi
        self.j = ai * bb + aj * bf + ak * bj
        self.k = ai * bc + aj * bg + ak * bk
        return self

    @property
    def copy(self):
        m = Matrix3()
        m.a = self.a
        m.b = self.b
        m.c = self.c
        m.e = self.e
        m.f = self.f
        m.g = self.g
        m.i = self.i
        m.j = self.j
        m.k = self.k

        return m

    def identity(self):
        self.a = self.f = self.k = 1
        self.b = self.c = self.e = self.g = self.i = self.j = 0
        return self

    def scale(self, x, y):
        self *= Matrix3.new_scale(x, y)
        return self

    def translate(self, x, y):
        self *= Matrix3.new_translate(x, y)
        return self

    def rotate(self, angle):
        self *= Matrix3.new_rotate(angle)
        return self

    @classmethod
    def new_identity(cls):
        return cls()

    @classmethod
    def new_scale(cls, x, y):
        c = cls()
        c.a = x
        c.f = y
        return c

    @classmethod
    def new_translate(cls, x, y):
        c = cls()
        c.c = x
        c.g = y
        return c

    @classmethod
    def new_rotate(cls, angle):
        cl = cls()
        s = math.sin(angle)
        c = math.cos(angle)

        cl.a = cl.f = c
        cl.b = -s
        cl.e = s

        return cl

    @property
    def determinant(self):
        return (self.a * self.f * self.k + self.b * self.g * self.i +
                self.c * self.e * self.j - self.a * self.g * self.j -
                self.b * self.e * self.k - self.c * self.f * self.i)

    @property
    def inverse(self):
        tmp = Matrix3()
        d = self.determinant

        if abs(d) < 0.001:
            # No inverse, return identity
            return tmp
        else:
            d = 1.0 / d

            tmp.a = d * (self.f * self.k - self.g * self.j)
            tmp.b = d * (self.c * self.j - self.b * self.k)
            tmp.c = d * (self.b * self.g - self.c * self.f)
            tmp.e = d * (self.g * self.i - self.e * self.k)
            tmp.f = d * (self.a * self.k - self.c * self.i)
            tmp.g = d * (self.c * self.e - self.a * self.g)
            tmp.i = d * (self.e * self.j - self.f * self.i)
            tmp.j = d * (self.b * self.i - self.a * self.j)
            tmp.k = d * (self.a * self.f - self.b * self.e)

            return tmp


class Matrix4(object):
    """
    a b c d
    e f g h
    i j k l
    m n o p
    """
    a = b = c = d = 0
    e = f = g = h = 0
    i = j = k = l = 0
    m = n = o = p = 0

    def __init__(self):
        self.a = self.f = self.k = self.p = 1.
        self.b = self.c = self.d = self.e = 0
        self.g = self.h = self.i = self.j = 0
        self.l = self.m = self.n = self.o = 0

    def __repr__(self):
        return ('<Matrix4>\n'
                '% 8.2f % 8.2f % 8.2f % 8.2f\n'
                '% 8.2f % 8.2f % 8.2f % 8.2f\n'
                '% 8.2f % 8.2f % 8.2f % 8.2f\n'
                '% 8.2f % 8.2f % 8.2f % 8.2f]') % (self.a, self.b, self.c, self.d,
                                                   self.e, self.f, self.g, self.h,
                                                   self.i, self.j, self.k, self.l,
                                                   self.m, self.n, self.o, self.p)

    def __getitem__(self, key):
        return [self.a, self.e, self.i, self.m,
                self.b, self.f, self.j, self.n,
                self.c, self.g, self.k, self.o,
                self.d, self.h, self.l, self.p][key]

    def __setitem__(self, key, value):
        l = self[:]
        l[key] = value
        (self.a, self.e, self.i, self.m,
         self.b, self.f, self.j, self.n,
         self.c, self.g, self.k, self.o,
         self.d, self.h, self.l, self.p) = l

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            # Cache attributes in local vars (see Matrix3.__mul__).
            aa = self.a
            ab = self.b
            ac = self.c
            ad = self.d
            ae = self.e
            af = self.f
            ag = self.g
            ah = self.h
            ai = self.i
            aj = self.j
            ak = self.k
            al = self.l
            am = self.m
            an = self.n
            ao = self.o
            ap = self.p
            ba = other.a
            bb = other.b
            bc = other.c
            bd = other.d
            be = other.e
            bf = other.f
            bg = other.g
            bh = other.h
            bi = other.i
            bj = other.j
            bk = other.k
            bl = other.l
            bm = other.m
            bn = other.n
            bo = other.o
            bp = other.p
            c = Matrix4()
            c.a = aa * ba + ab * be + ac * bi + ad * bm
            c.b = aa * bb + ab * bf + ac * bj + ad * bn
            c.c = aa * bc + ab * bg + ac * bk + ad * bo
            c.d = aa * bd + ab * bh + ac * bl + ad * bp
            c.e = ae * ba + af * be + ag * bi + ah * bm
            c.f = ae * bb + af * bf + ag * bj + ah * bn
            c.g = ae * bc + af * bg + ag * bk + ah * bo
            c.h = ae * bd + af * bh + ag * bl + ah * bp
            c.i = ai * ba + aj * be + ak * bi + al * bm
            c.j = ai * bb + aj * bf + ak * bj + al * bn
            c.k = ai * bc + aj * bg + ak * bk + al * bo
            c.l = ai * bd + aj * bh + ak * bl + al * bp
            c.m = am * ba + an * be + ao * bi + ap * bm
            c.n = am * bb + an * bf + ao * bj + ap * bn
            c.o = am * bc + an * bg + ao * bk + ap * bo
            c.p = am * bd + an * bh + ao * bl + ap * bp
            return c
        elif isinstance(other, Point3):
            a = self
            b = other
            p = Point3(0, 0, 0)
            p.x = a.a * b.x + a.b * b.y + a.c * b.z + a.d
            p.y = a.e * b.x + a.f * b.y + a.g * b.z + a.h
            p.z = a.i * b.x + a.j * b.y + a.k * b.z + a.l
            return p
        elif isinstance(other, Vector3):
            a = self
            b = other
            v = Vector3(0, 0, 0)
            v.x = a.a * b.x + a.b * b.y + a.c * b.z
            v.y = a.e * b.x + a.f * b.y + a.g * b.z
            v.z = a.i * b.x + a.j * b.y + a.k * b.z
            return v
        else:
            other = other.copy()
            other._apply_transform(self)
            return other

    def __imul__(self, other):
        aa = self.a
        ab = self.b
        ac = self.c
        ad = self.d
        ae = self.e
        af = self.f
        ag = self.g
        ah = self.h
        ai = self.i
        aj = self.j
        ak = self.k
        al = self.l
        am = self.m
        an = self.n
        ao = self.o
        ap = self.p
        ba = other.a
        bb = other.b
        bc = other.c
        bd = other.d
        be = other.e
        bf = other.f
        bg = other.g
        bh = other.h
        bi = other.i
        bj = other.j
        bk = other.k
        bl = other.l
        bm = other.m
        bn = other.n
        bo = other.o
        bp = other.p
        self.a = aa * ba + ab * be + ac * bi + ad * bm
        self.b = aa * bb + ab * bf + ac * bj + ad * bn
        self.c = aa * bc + ab * bg + ac * bk + ad * bo
        self.d = aa * bd + ab * bh + ac * bl + ad * bp
        self.e = ae * ba + af * be + ag * bi + ah * bm
        self.f = ae * bb + af * bf + ag * bj + ah * bn
        self.g = ae * bc + af * bg + ag * bk + ah * bo
        self.h = ae * bd + af * bh + ag * bl + ah * bp
        self.i = ai * ba + aj * be + ak * bi + al * bm
        self.j = ai * bb + aj * bf + ak * bj + al * bn
        self.k = ai * bc + aj * bg + ak * bk + al * bo
        self.l = ai * bd + aj * bh + ak * bl + al * bp
        self.m = am * ba + an * be + ao * bi + ap * bm
        self.n = am * bb + an * bf + ao * bj + ap * bn
        self.o = am * bc + an * bg + ao * bk + ap * bo
        self.p = am * bd + an * bh + ao * bl + ap * bp

    @property
    def copy(self):
        m = Matrix4()
        m.a = self.a
        m.b = self.b
        m.c = self.c
        m.d = self.d
        m.e = self.e
        m.f = self.f
        m.g = self.g
        m.h = self.h
        m.i = self.i
        m.j = self.j
        m.k = self.k
        m.l = self.l
        m.m = self.m
        m.n = self.n
        m.o = self.o
        m.p = self.p
        return m

    def transform(self, other):
        a = self
        b = other
        p = Point3(0, 0, 0)
        p.x = a.a * b.x + a.b * b.y + a.c * b.z + a.d
        p.y = a.e * b.x + a.f * b.y + a.g * b.z + a.h
        p.z = a.i * b.x + a.j * b.y + a.k * b.z + a.l
        w = a.m * b.x + a.n * b.y + a.o * b.z + a.p
        if w != 0:
            p.x /= w
            p.y /= w
            p.z /= w
        return p

    def identity(self):
        self.a = self.f = self.k = self.p = 1.
        self.b = self.c = self.d = self.e = 0
        self.g = self.h = self.i = self.j = 0
        self.l = self.m = self.n = self.o = 0

        return self

    def scale(self, x, y, z):
        self *= Matrix4.new_scale(x, y, z)
        return self

    def translate(self, x, y, z):
        self *= Matrix4.new_translate(x, y, z)
        return self

    def rotate_x(self, angle):
        self *= Matrix4.new_rotate_x(angle)
        return self

    def rotate_y(self, angle):
        self *= Matrix4.new_rotate_y(angle)
        return self

    def rotate_z(self, angle):
        self *= Matrix4.new_rotate_z(angle)
        return self

    def rotate_axis(self, angle, axis):
        self *= Matrix4.new_rotate_axis(angle, axis)
        return self

    def rotate_euler(self, heading, attitude, bank):
        self *= Matrix4.new_rotate_euler(heading, attitude, bank)
        return self

    def rotate_triple_axis(self, x, y, z):
        self *= Matrix4.new_rotate_triple_axis(x, y, z)
        return self

    def transpose(self):
        (self.a, self.e, self.i, self.m,
         self.b, self.f, self.j, self.n,
         self.c, self.g, self.k, self.o,
         self.d, self.h, self.l, self.p) = \
            (self.a, self.b, self.c, self.d,
             self.e, self.f, self.g, self.h,
             self.i, self.j, self.k, self.l,
             self.m, self.n, self.o, self.p)

    def transposed(self):
        m = self.copy
        m.transpose()
        return m

    @classmethod
    def new(cls, *vals):
        m = cls()
        m[:] = vals
        return m

    @classmethod
    def new_identity(cls):
        c = cls()
        return c

    @classmethod
    def new_scale(cls, x, y, z):
        c = cls()
        c.a = x
        c.f = y
        c.k = z
        return c

    @classmethod
    def new_translate(cls, x, y, z):
        c = cls()
        c.d = x
        c.h = y
        c.l = z
        return c

    @classmethod
    def new_rotate_x(cls, angle):
        cl = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        cl.f = cl.k = c
        cl.g = -s
        cl.j = s
        return cl

    @classmethod
    def new_rotate_y(cls, angle):
        cl = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        cl.a = cl.k = c
        cl.c = s
        cl.i = -s
        return cl

    @classmethod
    def new_rotate_z(cls, angle):
        cl = cls()

        s = math.sin(angle)
        c = math.cos(angle)
        cl.a = cl.f = c
        cl.b = -s
        cl.e = s

        return cl

    @classmethod
    def new_rotate_axis(cls, angle, axis):
        assert (isinstance(axis, Vector3))
        vector = axis.normalized()
        x = vector.x
        y = vector.y
        z = vector.z

        cl = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        c1 = 1. - c

        # from the glRotate man page
        cl.a = x * x * c1 + c
        cl.b = x * y * c1 - z * s
        cl.c = x * z * c1 + y * s
        cl.e = y * x * c1 + z * s
        cl.f = y * y * c1 + c
        cl.g = y * z * c1 - x * s
        cl.i = x * z * c1 - y * s
        cl.j = y * z * c1 + x * s
        cl.k = z * z * c1 + c
        return cl

    @classmethod
    def new_rotate_euler(cls, heading, attitude, bank):
        # from http://www.euclideanspace.com/
        ch = math.cos(heading)
        sh = math.sin(heading)
        ca = math.cos(attitude)
        sa = math.sin(attitude)
        cb = math.cos(bank)
        sb = math.sin(bank)

        cl = cls()
        cl.a = ch * ca
        cl.b = sh * sb - ch * sa * cb
        cl.c = ch * sa * sb + sh * cb
        cl.e = sa
        cl.f = ca * cb
        cl.g = -ca * sb
        cl.i = -sh * ca
        cl.j = sh * sa * cb + ch * sb
        cl.k = -sh * sa * sb + ch * cb
        return cl

    @classmethod
    def new_rotate_triple_axis(cls, x, y, z):
        m = cls()

        m.a, m.b, m.c = x.x, y.x, z.x
        m.e, m.f, m.g = x.y, y.y, z.y
        m.i, m.j, m.k = x.z, y.z, z.z

        return m

    @classmethod
    def new_look_at(cls, eye, at, up):
        z = (eye - at).normalized()
        x = up.cross(z).normalized()
        y = z.cross(x)

        m = cls.new_rotate_triple_axis(x, y, z)
        m.d, m.h, m.l = eye.x, eye.y, eye.z
        return m

    @classmethod
    def new_perspective(cls, fov_y, aspect, near, far):
        # from the gluPerspective man page
        f = 1 / math.tan(fov_y / 2)
        m = cls()
        assert near != 0.0 and near != far
        m.a = f / aspect
        m.f = f
        m.k = (far + near) / (near - far)
        m.l = 2 * far * near / (near - far)
        m.o = -1
        m.p = 0
        return m

    @property
    def determinant(self):
        return ((self.a * self.f - self.e * self.b)
                * (self.k * self.p - self.o * self.l)
                - (self.a * self.j - self.i * self.b)
                * (self.g * self.p - self.o * self.h)
                + (self.a * self.n - self.m * self.b)
                * (self.g * self.l - self.k * self.h)
                + (self.e * self.j - self.i * self.f)
                * (self.c * self.p - self.o * self.d)
                - (self.e * self.n - self.m * self.f)
                * (self.c * self.l - self.k * self.d)
                + (self.i * self.n - self.m * self.j)
                * (self.c * self.h - self.g * self.d))

    @property
    def inverse(self):
        tmp = Matrix4()
        d = self.determinant

        if abs(d) < 0.001:
            # No inverse, return identity
            return tmp
        else:
            d = 1.0 / d

            tmp.a = d * (self.f * (self.k * self.p - self.o * self.l) +
                         self.j * (self.o * self.h - self.g * self.p) +
                         self.n * (self.g * self.l - self.k * self.h))
            tmp.e = d * (self.g * (self.i * self.p - self.m * self.l) +
                         self.k * (self.m * self.h - self.e * self.p) +
                         self.o * (self.e * self.l - self.i * self.h))
            tmp.i = d * (self.h * (self.i * self.n - self.m * self.j) +
                         self.l * (self.m * self.f - self.e * self.n) +
                         self.p * (self.e * self.j - self.i * self.f))
            tmp.m = d * (self.e * (self.n * self.k - self.j * self.o) +
                         self.i * (self.f * self.o - self.n * self.g) +
                         self.m * (self.j * self.g - self.f * self.k))

            tmp.b = d * (self.j * (self.c * self.p - self.o * self.d) +
                         self.n * (self.k * self.d - self.c * self.l) +
                         self.b * (self.o * self.l - self.k * self.p))
            tmp.f = d * (self.k * (self.a * self.p - self.m * self.d) +
                         self.o * (self.i * self.d - self.a * self.l) +
                         self.c * (self.m * self.l - self.i * self.p))
            tmp.j = d * (self.l * (self.a * self.n - self.m * self.b) +
                         self.p * (self.i * self.b - self.a * self.j) +
                         self.d * (self.m * self.j - self.i * self.n))
            tmp.n = d * (self.i * (self.n * self.c - self.b * self.o) +
                         self.m * (self.b * self.k - self.j * self.c) +
                         self.a * (self.j * self.o - self.n * self.k))

            tmp.c = d * (self.n * (self.c * self.h - self.g * self.d) +
                         self.b * (self.g * self.p - self.o * self.h) +
                         self.f * (self.o * self.d - self.c * self.p))
            tmp.g = d * (self.o * (self.a * self.h - self.e * self.d) +
                         self.c * (self.e * self.p - self.m * self.h) +
                         self.g * (self.m * self.d - self.a * self.p))
            tmp.k = d * (self.p * (self.a * self.f - self.e * self.b) +
                         self.d * (self.e * self.n - self.m * self.f) +
                         self.h * (self.m * self.b - self.a * self.n))
            tmp.o = d * (self.m * (self.f * self.c - self.b * self.g) +
                         self.a * (self.n * self.g - self.f * self.o) +
                         self.e * (self.b * self.o - self.n * self.c))

            tmp.d = d * (self.b * (self.k * self.h - self.g * self.l) +
                         self.f * (self.c * self.l - self.k * self.d) +
                         self.j * (self.g * self.d - self.c * self.h))
            tmp.h = d * (self.c * (self.i * self.h - self.e * self.l) +
                         self.g * (self.a * self.l - self.i * self.d) +
                         self.k * (self.e * self.d - self.a * self.h))
            tmp.l = d * (self.d * (self.i * self.f - self.e * self.j) +
                         self.h * (self.a * self.j - self.i * self.b) +
                         self.l * (self.e * self.b - self.a * self.f))
            tmp.p = d * (self.a * (self.f * self.k - self.j * self.g) +
                         self.e * (self.j * self.c - self.b * self.k) +
                         self.i * (self.b * self.g - self.f * self.c))

        return tmp


class Quaternion(object):
    # All methods and naming conventions based off
    # http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions
    # w is the real part, (x, y, z) are the imaginary parts
    def __init__(self, w=1, x=0, y=0, z=0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '<Quaternion(real=%.2f, imagine=<%.2f, %.2f, %.2f>)>' % \
               (self.w, self.x, self.y, self.z)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            ax = self.x
            ay = self.y
            az = self.z
            aw = self.w
            bx = other.x
            by = other.y
            bz = other.z
            bw = other.w
            q = Quaternion()
            q.x = ax * bw + ay * bz - az * by + aw * bx
            q.y = -ax * bz + ay * bw + az * bx + aw * by
            q.z = ax * by - ay * bx + az * bw + aw * bz
            q.w = -ax * bx - ay * by - az * bz + aw * bw
            return q
        elif isinstance(other, Vector3):
            w = self.w
            x = self.x
            y = self.y
            z = self.z
            vx = other.x
            vy = other.y
            vz = other.z
            ww = w * w
            w2 = w * 2
            wx2 = w2 * x
            wy2 = w2 * y
            wz2 = w2 * z
            xx = x * x
            x2 = x * 2
            xy2 = x2 * y
            xz2 = x2 * z
            yy = y * y
            yz2 = 2 * y * z
            zz = z * z
            return other.__class__(ww * vx + wy2 * vz - wz2 * vy +
                                   xx * vx + xy2 * vy + xz2 * vz -
                                   zz * vx - yy * vx,
                                   xy2 * vx + yy * vy + yz2 * vz +
                                   wz2 * vx - zz * vy + ww * vy -
                                   wx2 * vz - xx * vy,
                                   xz2 * vx + yz2 * vy +
                                   zz * vz - wy2 * vx - yy * vz +
                                   wx2 * vy - xx * vz + ww * vz)

        else:
            other = other.copy()
            other._apply_transform(self)
            return other

    def __imul__(self, other):
        ax = self.x
        ay = self.y
        az = self.z
        aw = self.w
        bx = other.x
        by = other.y
        bz = other.z
        bw = other.w

        self.x = ax * bw + ay * bz - az * by + aw * bx
        self.y = -ax * bz + ay * bw + az * bx + aw * by
        self.z = ax * by - ay * bx + az * bw + aw * bz
        self.w = -ax * bx - ay * by - az * bz + aw * bw

        return self

    @property
    def copy(self):
        q = Quaternion()
        q.w = self.w
        q.x = self.x
        q.y = self.y
        q.z = self.z
        return q

    @property
    def magnitude(self):
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def magnitude_squared(self):
        return self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2

    def identity(self):
        self.w = 1
        self.x = 0
        self.y = 0
        self.z = 0
        return self

    def rotate_axis(self, angle, axis):
        self *= Quaternion.new_rotate_axis(angle, axis)
        return self

    def rotate_euler(self, heading, attitude, bank):
        self *= Quaternion.new_rotate_euler(heading, attitude, bank)
        return self

    def rotate_matrix(self, mat):
        self *= Quaternion.new_rotate_matrix(m)
        return self

    def conjugated(self):
        q = Quaternion()
        q.w = self.w
        q.x = -self.x
        q.y = -self.y
        q.z = -self.z
        return q

    def normalize(self):
        d = self.magnitude
        if d != 0:
            self.w /= d
            self.x /= d
            self.y /= d
            self.z /= d
        return self

    def normalized(self):
        d = self.magnitude
        if d != 0:
            Q = Quaternion()
            Q.w = self.w / d
            Q.x = self.x / d
            Q.y = self.y / d
            Q.z = self.z / d
            return Q
        else:
            return self.copy

    @property
    def angel_axis(self):
        if self.w > 1:
            self = self.normalized()
        angle = 2 * math.acos(self.w)
        s = math.sqrt(1 - self.w ** 2)
        if s < 0.001:
            return angle, Vector3(1, 0, 0)
        else:
            return angle, Vector3(self.x / s, self.y / s, self.z / s)

    @property
    def euler(self):
        t = self.x * self.y + self.z * self.w
        if t > 0.4999:
            heading = 2 * math.atan2(self.x, self.w)
            attitude = math.pi / 2
            bank = 0
        elif t < -0.4999:
            heading = -2 * math.atan2(self.x, self.w)
            attitude = -math.pi / 2
            bank = 0
        else:
            sqx = self.x ** 2
            sqy = self.y ** 2
            sqz = self.z ** 2
            heading = math.atan2(2 * self.y * self.w - 2 * self.x * self.z,
                                 1 - 2 * sqy - 2 * sqz)
            attitude = math.asin(2 * t)
            bank = math.atan2(2 * self.x * self.w - 2 * self.y * self.z,
                              1 - 2 * sqx - 2 * sqz)
        return heading, attitude, bank

    @property
    def matrix(self):
        xx = self.x ** 2
        xy = self.x * self.y
        xz = self.x * self.z
        xw = self.x * self.w
        yy = self.y ** 2
        yz = self.y * self.z
        yw = self.y * self.w
        zz = self.z ** 2
        zw = self.z * self.w
        m = Matrix4()
        m.a = 1 - 2 * (yy + zz)
        m.b = 2 * (xy - zw)
        m.c = 2 * (xz + yw)
        m.e = 2 * (xy + zw)
        m.f = 1 - 2 * (xx + zz)
        m.g = 2 * (yz - xw)
        m.i = 2 * (xz - yw)
        m.j = 2 * (yz + xw)
        m.k = 1 - 2 * (xx + yy)
        return m

    @classmethod
    def new_identity(cls):
        return cls()

    @classmethod
    def new_rotate_axis(cls, angle, axis):
        assert (isinstance(axis, Vector3))
        axis = axis.normalized()
        s = math.sin(angle / 2)
        q = cls()
        q.w = math.cos(angle / 2)
        q.x = axis.x * s
        q.y = axis.y * s
        q.z = axis.z * s
        return q

    @classmethod
    def new_rotate_euler(cls, heading, attitude, bank):
        q = cls()
        c1 = math.cos(heading / 2)
        s1 = math.sin(heading / 2)
        c2 = math.cos(attitude / 2)
        s2 = math.sin(attitude / 2)
        c3 = math.cos(bank / 2)
        s3 = math.sin(bank / 2)

        q.w = c1 * c2 * c3 - s1 * s2 * s3
        q.x = s1 * s2 * c3 + c1 * c2 * s3
        q.y = s1 * c2 * c3 + c1 * s2 * s3
        q.z = c1 * s2 * c3 - s1 * c2 * s3
        return q

    @classmethod
    def new_rotate_matrix(cls, mat):
        if mat[0 * 4 + 0] + mat[1 * 4 + 1] + mat[2 * 4 + 2] > 0.00000001:
            t = mat[0 * 4 + 0] + mat[1 * 4 + 1] + mat[2 * 4 + 2] + 1.0
            s = 0.5 / math.sqrt(t)

            return cls(
                    s * t,
                    (mat[1 * 4 + 2] - mat[2 * 4 + 1]) * s,
                    (mat[2 * 4 + 0] - mat[0 * 4 + 2]) * s,
                    (mat[0 * 4 + 1] - mat[1 * 4 + 0]) * s
            )

        elif mat[0 * 4 + 0] > mat[1 * 4 + 1] and mat[0 * 4 + 0] > mat[2 * 4 + 2]:
            t = mat[0 * 4 + 0] - mat[1 * 4 + 1] - mat[2 * 4 + 2] + 1.0
            s = 0.5 / math.sqrt(t)

            return cls(
                    (mat[1 * 4 + 2] - mat[2 * 4 + 1]) * s,
                    s * t,
                    (mat[0 * 4 + 1] + mat[1 * 4 + 0]) * s,
                    (mat[2 * 4 + 0] + mat[0 * 4 + 2]) * s
            )

        elif mat[1 * 4 + 1] > mat[2 * 4 + 2]:
            t = -mat[0 * 4 + 0] + mat[1 * 4 + 1] - mat[2 * 4 + 2] + 1.0
            s = 0.5 / math.sqrt(t)

            return cls(
                    (mat[2 * 4 + 0] - mat[0 * 4 + 2]) * s,
                    (mat[0 * 4 + 1] + mat[1 * 4 + 0]) * s,
                    s * t,
                    (mat[1 * 4 + 2] + mat[2 * 4 + 1]) * s
            )

        else:
            t = -mat[0 * 4 + 0] - mat[1 * 4 + 1] + mat[2 * 4 + 2] + 1.0
            s = 0.5 / math.sqrt(t)

            return cls(
                    (mat[0 * 4 + 1] - mat[1 * 4 + 0]) * s,
                    (mat[2 * 4 + 0] + mat[0 * 4 + 2]) * s,
                    (mat[1 * 4 + 2] + mat[2 * 4 + 1]) * s,
                    s * t
            )

    @classmethod
    def new_interpolate(cls, q1, q2, t):
        assert isinstance(q1, Quaternion) and isinstance(q2, Quaternion)
        q = cls()

        costheta = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z
        if costheta < 0.:
            costheta = -costheta
            q1 = q1.conjugated()
        elif costheta > 1:
            costheta = 1

        theta = math.acos(costheta)
        if abs(theta) < 0.01:
            q.w = q2.w
            q.x = q2.x
            q.y = q2.y
            q.z = q2.z
            return q

        sintheta = math.sqrt(1.0 - costheta * costheta)
        if abs(sintheta) < 0.01:
            q.w = (q1.w + q2.w) * 0.5
            q.x = (q1.x + q2.x) * 0.5
            q.y = (q1.y + q2.y) * 0.5
            q.z = (q1.z + q2.z) * 0.5
            return q

        ratio1 = math.sin((1 - t) * theta) / sintheta
        ratio2 = math.sin(t * theta) / sintheta

        q.w = q1.w * ratio1 + q2.w * ratio2
        q.x = q1.x * ratio1 + q2.x * ratio2
        q.y = q1.y * ratio1 + q2.y * ratio2
        q.z = q1.z * ratio1 + q2.z * ratio2
        return q


class Geometry(object):
    def _connect_unimplemented(self, other):
        raise AttributeError('Cannot connect {} {} %s'.format(self.__class__,
                                                              other.__class__))

    def _intersect_unimplemented(self, other):
        raise AttributeError('Cannot intersect %s and %s'.format(self.__class__,
                                                                 other.__class__))

    _intersect_point2 = _intersect_unimplemented
    _intersect_line2 = _intersect_unimplemented
    _intersect_circle = _intersect_unimplemented
    _connect_point2 = _connect_unimplemented
    _connect_line2 = _connect_unimplemented
    _connect_circle = _connect_unimplemented

    _intersect_point3 = _intersect_unimplemented
    _intersect_line3 = _intersect_unimplemented
    _intersect_sphere = _intersect_unimplemented
    _intersect_plane = _intersect_unimplemented
    _connect_point3 = _connect_unimplemented
    _connect_line3 = _connect_unimplemented
    _connect_sphere = _connect_unimplemented
    _connect_plane = _connect_unimplemented

    def intersect(self, other):
        raise NotImplementedError

    def connect(self, other):
        raise NotImplementedError

    def distance(self, other):
        c = self.connect(other)
        if c:
            return c.length
        return 0.0


def _intersect_point2_circle(P, C):
    return abs(P - C.c) <= C.r


def _intersect_line2_line2(A, B):
    d = B.v.y * A.v.x - B.v.x * A.v.y
    if d == 0:
        return None

    dy = A.p.y - B.p.y
    dx = A.p.x - B.p.x
    ua = (B.v.x * dy - B.v.y * dx) / d
    if not A._u_in(ua):
        return None
    ub = (A.v.x * dy - A.v.y * dx) / d
    if not B._u_in(ub):
        return None

    return Point2(A.p.x + ua * A.v.x,
                  A.p.y + ua * A.v.y)


def _intersect_line2_circle(L, C):
    a = L.v.magnitude_squared()
    b = 2 * (L.v.x * (L.p.x - C.c.x) + L.v.y * (L.p.y - C.c.y))
    c = C.c.magnitude_squared() + \
        L.p.magnitude_squared() - \
        2 * C.c.dot(L.p) - \
        C.r ** 2
    det = b ** 2 - 4 * a * c
    if det < 0:
        return None
    sq = math.sqrt(det)
    u1 = (-b + sq) / (2 * a)
    u2 = (-b - sq) / (2 * a)
    if not L._u_in(u1):
        u1 = max(min(u1, 1.0), 0.0)
    if not L._u_in(u2):
        u2 = max(min(u2, 1.0), 0.0)

    # Tangent
    if u1 == u2:
        return Point2(L.p.x + u1 * L.v.x,
                      L.p.y + u1 * L.v.y)

    return LineSegment2(Point2(L.p.x + u1 * L.v.x, L.p.y + u1 * L.v.y),
                        Point2(L.p.x + u2 * L.v.x, L.p.y + u2 * L.v.y))


def _connect_point2_line2(P, L):
    d = L.v.magnitude_squared()
    assert d != 0
    u = ((P.x - L.p.x) * L.v.x + (P.y - L.p.y) * L.v.y) / d
    if not L._u_in(u):
        u = max(min(u, 1.0), 0.0)
    return LineSegment2(P, Point2(L.p.x + u * L.v.x, L.p.y + u * L.v.y))


def _connect_point2_circle(P, C):
    v = P - C.c
    v.normalize()
    v *= C.r
    return LineSegment2(P, Point2(C.c.x + v.x, C.c.y + v.y))


def _connect_line2_line2(A, B):
    d = B.v.y * A.v.x - B.v.x * A.v.y
    if d == 0:
        # Parallel, connect an endpoint with a line
        if isinstance(B, Ray2) or isinstance(B, LineSegment2):
            p1, p2 = _connect_point2_line2(B.p, A)
            return p2, p1
        # No endpoint (or endpoint is on A), possibly choose arbitrary point
        # on line.
        return _connect_point2_line2(A.p, B)

    dy = A.p.y - B.p.y
    dx = A.p.x - B.p.x
    ua = (B.v.x * dy - B.v.y * dx) / d
    if not A._u_in(ua):
        ua = max(min(ua, 1.0), 0.0)
    ub = (A.v.x * dy - A.v.y * dx) / d
    if not B._u_in(ub):
        ub = max(min(ub, 1.0), 0.0)

    return LineSegment2(Point2(A.p.x + ua * A.v.x, A.p.y + ua * A.v.y),
                        Point2(B.p.x + ub * B.v.x, B.p.y + ub * B.v.y))


def _connect_circle_line2(C, L):
    d = L.v.magnitude_squared()
    assert d != 0
    u = ((C.c.x - L.p.x) * L.v.x + (C.c.y - L.p.y) * L.v.y) / d
    if not L._u_in(u):
        u = max(min(u, 1.0), 0.0)
    point = Point2(L.p.x + u * L.v.x, L.p.y + u * L.v.y)
    v = (point - C.c)
    v.normalize()
    v *= C.r
    return LineSegment2(Point2(C.c.x + v.x, C.c.y + v.y), point)


def _connect_circle_circle(A, B):
    v = B.c - A.c
    d = v.magnitude()
    if A.r >= B.r and d < A.r:
        # centre B inside A
        s1, s2 = +1, +1
    elif B.r > A.r and d < B.r:
        # centre A inside B
        s1, s2 = -1, -1
    elif d >= A.r and d >= B.r:
        s1, s2 = +1, -1
    v.normalize()
    return LineSegment2(Point2(A.c.x + s1 * v.x * A.r, A.c.y + s1 * v.y * A.r),
                        Point2(B.c.x + s2 * v.x * B.r, B.c.y + s2 * v.y * B.r))


# 3D Geometry
def _connect_point3_line3(P, L):
    d = L.v.magnitude_squared()
    assert d != 0
    u = ((P.x - L.p.x) * L.v.x + (P.y - L.p.y) * L.v.y + (P.z - L.p.z) * L.v.z) / d
    if not L._u_in(u):
        u = max(min(u, 1.0), 0.0)
    return LineSegment3(P, Point3(L.p.x + u * L.v.x, L.p.y + u * L.v.y,
                                  L.p.z + u * L.v.z))


def _connect_point3_sphere(P, S):
    v = P - S.c
    v.normalize()
    v *= S.r
    return LineSegment3(P, Point3(S.c.x + v.x, S.c.y + v.y, S.c.z + v.z))


def _connect_point3_plane(p, plane):
    n = plane.n.normalized()
    d = p.dot(plane.n) - plane.k
    return LineSegment3(p, Point3(p.x - n.x * d, p.y - n.y * d, p.z - n.z * d))


def _connect_line3_line3(A, B):
    assert A.v and B.v
    p13 = A.p - B.p
    d1343 = p13.dot(B.v)
    d4321 = B.v.dot(A.v)
    d1321 = p13.dot(A.v)
    d4343 = B.v.magnitude_squared()
    denom = A.v.magnitude_squared() * d4343 - d4321 ** 2
    if denom == 0:
        # Parallel, connect an endpoint with a line
        if isinstance(B, Ray3) or isinstance(B, LineSegment3):
            return _connect_point3_line3(B.p, A)._swap()
        # No endpoint (or endpoint is on A), possibly choose arbitrary
        # point on line.
        return _connect_point3_line3(A.p, B)

    ua = (d1343 * d4321 - d1321 * d4343) / denom
    if not A._u_in(ua):
        ua = max(min(ua, 1.0), 0.0)
    ub = (d1343 + d4321 * ua) / d4343
    if not B._u_in(ub):
        ub = max(min(ub, 1.0), 0.0)
    return LineSegment3(Point3(A.p.x + ua * A.v.x,
                               A.p.y + ua * A.v.y,
                               A.p.z + ua * A.v.z),
                        Point3(B.p.x + ub * B.v.x,
                               B.p.y + ub * B.v.y,
                               B.p.z + ub * B.v.z))


def _connect_line3_plane(L, P):
    d = P.n.dot(L.v)
    if not d:
        # Parallel, choose an endpoint
        return _connect_point3_plane(L.p, P)
    u = (P.k - P.n.dot(L.p)) / d
    if not L._u_in(u):
        # intersects out of range, choose nearest endpoint
        u = max(min(u, 1.0), 0.0)
        return _connect_point3_plane(Point3(L.p.x + u * L.v.x,
                                            L.p.y + u * L.v.y,
                                            L.p.z + u * L.v.z), P)
    # Intersection
    return None


def _connect_sphere_line3(S, L):
    d = L.v.magnitude_squared()
    assert d != 0
    u = ((S.c.x - L.p.x) * L.v.x + (S.c.y - L.p.y) * L.v.y + (S.c.z - L.p.z) * L.v.z) / d
    if not L._u_in(u):
        u = max(min(u, 1.0), 0.0)
    point = Point3(L.p.x + u * L.v.x, L.p.y + u * L.v.y, L.p.z + u * L.v.z)
    v = (point - S.c)
    v.normalize()
    v *= S.r
    return LineSegment3(Point3(S.c.x + v.x, S.c.y + v.y, S.c.z + v.z), point)


def _connect_sphere_sphere(A, B):
    v = B.c - A.c
    d = v.magnitude()
    if A.r >= B.r and d < A.r:
        # centre B inside A
        s1, s2 = +1, +1
    elif B.r > A.r and d < B.r:
        # centre A inside B
        s1, s2 = -1, -1
    elif d >= A.r and d >= B.r:
        s1, s2 = +1, -1

    v.normalize()
    return LineSegment3(Point3(A.c.x + s1* v.x * A.r,
                               A.c.y + s1* v.y * A.r,
                               A.c.z + s1* v.z * A.r),
                        Point3(B.c.x + s2* v.x * B.r,
                               B.c.y + s2* v.y * B.r,
                               B.c.z + s2* v.z * B.r))


def _connect_sphere_plane(S, P):
    c = _connect_point3_plane(S.c, P)
    if not c:
        return None
    p2 = c.p2
    v = p2 - S.c
    v.normalize()
    v *= S.r
    return LineSegment3(Point3(S.c.x + v.x, S.c.y + v.y, S.c.z + v.z),
                        p2)


def _connect_plane_plane(A, B):
    if A.n.cross(B.n):
        # Planes intersect
        return None
    else:
        # Planes are parallel, connect to arbitrary point
        return _connect_point3_plane(A._get_point(), B)


def _intersect_point3_sphere(P, S):
    return abs(P - S.c) <= S.r


def _intersect_line3_sphere(L, S):
    a = L.v.magnitude_squared()
    b = 2 * (L.v.x * (L.p.x - S.c.x) + L.v.y * (L.p.y - S.c.y) + L.v.z * (L.p.z - S.c.z))
    c = S.c.magnitude_squared() + L.p.magnitude_squared() - 2 * S.c.dot(L.p) - S.r ** 2
    det = b ** 2 - 4 * a * c
    if det < 0:
        return None
    sq = math.sqrt(det)
    u1 = (-b + sq) / (2 * a)
    u2 = (-b - sq) / (2 * a)
    if not L._u_in(u1):
        u1 = max(min(u1, 1.0), 0.0)
    if not L._u_in(u2):
        u2 = max(min(u2, 1.0), 0.0)
    return LineSegment3(Point3(L.p.x + u1 * L.v.x,
                               L.p.y + u1 * L.v.y,
                               L.p.z + u1 * L.v.z),
                        Point3(L.p.x + u2 * L.v.x,
                               L.p.y + u2 * L.v.y,
                               L.p.z + u2 * L.v.z))


def _intersect_line3_plane(L, P):
    d = P.n.dot(L.v)
    if not d:
        # Parallel
        return None
    u = (P.k - P.n.dot(L.p)) / d
    if not L._u_in(u):
        return None
    return Point3(L.p.x + u * L.v.x,
                  L.p.y + u * L.v.y,
                  L.p.z + u * L.v.z)


def _intersect_plane_plane(A, B):
    n1_m = A.n.magnitude_squared()
    n2_m = B.n.magnitude_squared()
    n1d2 = A.n.dot(B.n)
    det = n1_m * n2_m - n1d2 ** 2
    if det == 0:
        # Parallel
        return None
    c1 = (A.k * n2_m - B.k * n1d2) / det
    c2 = (B.k * n1_m - A.k * n1d2) / det
    return Line3(Point3(c1 * A.n.x + c2 * B.n.x, c1 * A.n.y + c2 * B.n.y,
                        c1 * A.n.z + c2 * B.n.z),
                 A.n.cross(B.n))


class Point2(Vector2, Geometry):
    def __repr__(self):
        return 'Point2(%.2f, %.2f)' % (self.x, self.y)

    def intersect(self, other):
        return other._intersect_point2(self)

    def _intersect_circle(self, other):
        return _intersect_point2_circle(self, other)

    def connect(self, other):
        return other._connect_point2(self)

    def _connect_point2(self, other):
        return LineSegment2(other, self)

    def _connect_line2(self, other):
        c = _connect_point2_line2(self, other)
        if c:
            return c._swap()

    def _connect_circle(self, other):
        c = _connect_point2_circle(self, other)
        if c:
            return c._swap()


class Point3(Vector3, Geometry):
    def __repr__(self):
        return 'Point3(%.2f, %.2f, %.2f)' % (self.x, self.y, self.z)

    def intersect(self, other):
        return other._intersect_point3(self)

    def _intersect_sphere(self, other):
        return _intersect_point3_sphere(self, other)

    def connect(self, other):
        return other._connect_point3(self)

    def _connect_point3(self, other):
        if self != other:
            return LineSegment3(other, self)
        return None

    def _connect_line3(self, other):
        c = _connect_point3_line3(self, other)
        if c:
            return c._swap()

    def _connect_sphere(self, other):
        c = _connect_point3_sphere(self, other)
        if c:
            return c._swap()

    def _connect_plane(self, other):
        c = _connect_point3_plane(self, other)
        if c:
            return c._swap()


class Line2(Geometry):
    def __init__(self, *args):
        if len(args) == 3:
            assert (isinstance(args[0], Point2) and
                    isinstance(args[1], Vector2) and
                    type(args[2]) == float)
            self.p = args[0].copy()
            self.v = args[1] * args[2] / abs(args[1])
        elif len(args) == 2:
            if isinstance(args[0], Point2) and isinstance(args[1], Point2):
                self.p = args[0].copy()
                self.v = args[1] - args[0]
            elif isinstance(args[0], Point2) and isinstance(args[1], Vector2):
                self.p = args[0].copy()
                self.v = args[1].copy()
            else:
                raise AttributeError('%r' % (args,))
        elif len(args) == 1:
            if isinstance(args[0], Line2):
                self.p = args[0].p.copy()
                self.v = args[0].v.copy()
            else:
                raise AttributeError('%r' % (args,))
        else:
            raise AttributeError('%r' % (args,))

        if not self.v:
            raise AttributeError('Line has zero-length vector')

    @property
    def copy(self):
        return self.__class__(self.p, self.v)

    def __repr__(self):
        return 'Line2(<%.2f, %.2f> + u<%.2f, %.2f>)' % \
               (self.p.x, self.p.y, self.v.x, self.v.y)

    p1 = property(lambda self: self.p)
    p2 = property(lambda self: Point2(self.p.x + self.v.x,
                                      self.p.y + self.v.y))

    def _apply_transform(self, t):
        self.p *= t
        self.v *= t

    def _u_in(self, u):
        return True

    def intersect(self, other):
        return other._intersect_line2(self)

    def _intersect_line2(self, other):
        return _intersect_line2_line2(self, other)

    def _intersect_circle(self, other):
        return _intersect_line2_circle(self, other)

    def connect(self, other):
        return other._connect_line2(self)

    def _connect_point2(self, other):
        return _connect_point2_line2(other, self)

    def _connect_line2(self, other):
        return _connect_line2_line2(other, self)

    def _connect_circle(self, other):
        return _connect_circle_line2(other, self)


class Line3(object):
    def __init__(self, *args):
        if len(args) == 3:
            assert isinstance(args[0], Point3) and \
                   isinstance(args[1], Vector3) and \
                   type(args[2]) == float
            self.p = args[0].copy()
            self.v = args[1] * args[2] / abs(args[1])
        elif len(args) == 2:
            if isinstance(args[0], Point3) and isinstance(args[1], Point3):
                self.p = args[0].copy()
                self.v = args[1] - args[0]
            elif isinstance(args[0], Point3) and isinstance(args[1], Vector3):
                self.p = args[0].copy()
                self.v = args[1].copy()
            else:
                raise AttributeError, '%r' % (args,)
        elif len(args) == 1:
            if isinstance(args[0], Line3):
                self.p = args[0].p.copy()
                self.v = args[0].v.copy()
            else:
                raise AttributeError, '%r' % (args,)
        else:
            raise AttributeError, '%r' % (args,)

            # XXX This is annoying.
            # if not self.v:
            #    raise AttributeError, 'Line has zero-length vector'

    @property
    def copy(self):
        return self.__class__(self.p, self.v)

    def __repr__(self):
        return 'Line3(<%.2f, %.2f, %.2f> + u<%.2f, %.2f, %.2f>)' % \
               (self.p.x, self.p.y, self.p.z, self.v.x, self.v.y, self.v.z)

    p1 = property(lambda self: self.p)
    p2 = property(lambda self: Point3(self.p.x + self.v.x,
                                      self.p.y + self.v.y,
                                      self.p.z + self.v.z))

    def _apply_transform(self, t):
        self.p = t * self.p
        self.v = t * self.v

    def _u_in(self, u):
        return True

    def intersect(self, other):
        return other._intersect_line3(self)

    def _intersect_sphere(self, other):
        return _intersect_line3_sphere(self, other)

    def _intersect_plane(self, other):
        return _intersect_line3_plane(self, other)

    def connect(self, other):
        return other._connect_line3(self)

    def _connect_point3(self, other):
        return _connect_point3_line3(other, self)

    def _connect_line3(self, other):
        return _connect_line3_line3(other, self)

    def _connect_sphere(self, other):
        return _connect_sphere_line3(other, self)

    def _connect_plane(self, other):
        c = _connect_line3_plane(self, other)
        if c:
            return c


class Ray2(Line2):
    def __repr__(self):
        return 'Ray2(<%.2f, %.2f> + u<%.2f, %.2f>)' % \
               (self.p.x, self.p.y, self.v.x, self.v.y)

    def _u_in(self, u):
        return u >= 0.0


class Ray3(Line3):
    def __repr__(self):
        return 'Ray3(<%.2f, %.2f, %.2f> + u<%.2f, %.2f, %.2f>)' % \
               (self.p.x, self.p.y, self.p.z, self.v.x, self.v.y, self.v.z)

    def _u_in(self, u):
        return u >= 0.0


class LineSegment2(Line2):
    def __repr__(self):
        return '<LineSegment2(<%.2f, %.2f> to <%.2f, %.2f>)>' % \
               (self.p.x, self.p.y, self.p.x + self.v.x, self.p.y + self.v.y)

    def _u_in(self, u):
        return 0.0 <= u <= 1.0

    def __abs__(self):
        return abs(self.v)

    def magnitude_squared(self):
        return self.v.magnitude_squared()

    def _swap(self):
        # used by connect methods to switch order of points
        self.p = self.p2
        self.v *= -1
        return self

    length = property(lambda self: abs(self.v))


class LineSegment3(Line3):
    def __repr__(self):
        return 'LineSegment3(<%.2f, %.2f, %.2f> to <%.2f, %.2f, %.2f>)' % \
               (self.p.x, self.p.y, self.p.z,
                self.p.x + self.v.x, self.p.y + self.v.y, self.p.z + self.v.z)

    def _u_in(self, u):
        return u >= 0.0 and u <= 1.0

    def __abs__(self):
        return abs(self.v)

    def magnitude_squared(self):
        return self.v.magnitude_squared()

    def _swap(self):
        # used by connect methods to switch order of points
        self.p = self.p2
        self.v *= -1
        return self

    length = property(lambda self: abs(self.v))


class Circle(Geometry):
    def __init__(self, center, radius):
        assert isinstance(center, Vector2) and type(radius) == float
        self.c = center.copy()
        self.r = radius

    def __copy__(self):
        return self.__class__(self.c, self.r)

    copy = __copy__

    def __repr__(self):
        return 'Circle(<%.2f, %.2f>, radius=%.2f)' % \
               (self.c.x, self.c.y, self.r)

    def _apply_transform(self, t):
        self.c = t * self.c

    def intersect(self, other):
        return other._intersect_circle(self)

    def _intersect_point2(self, other):
        return _intersect_point2_circle(other, self)

    def _intersect_line2(self, other):
        return _intersect_line2_circle(other, self)

    def connect(self, other):
        return other._connect_circle(self)

    def _connect_point2(self, other):
        return _connect_point2_circle(other, self)

    def _connect_line2(self, other):
        c = _connect_circle_line2(self, other)
        if c:
            return c._swap()

    def _connect_circle(self, other):
        return _connect_circle_circle(other, self)


class Sphere(object):
    def __init__(self, center, radius):
        assert isinstance(center, Vector3) and type(radius) == float
        self.c = center.copy
        self.r = radius

    @property
    def copy(self):
        return self.__class__(self.c, self.r)

    def __repr__(self):
        return 'Sphere(<%.2f, %.2f, %.2f>, radius=%.2f)' % \
               (self.c.x, self.c.y, self.c.z, self.r)

    def _apply_transform(self, t):
        self.c = t * self.c

    def intersect(self, other):
        return other._intersect_sphere(self)

    def _intersect_point3(self, other):
        return _intersect_point3_sphere(other, self)

    def _intersect_line3(self, other):
        return _intersect_line3_sphere(other, self)

    def connect(self, other):
        return other._connect_sphere(self)

    def _connect_point3(self, other):
        return _connect_point3_sphere(other, self)

    def _connect_line3(self, other):
        c = _connect_sphere_line3(self, other)
        if c:
            return c._swap()

    def _connect_sphere(self, other):
        return _connect_sphere_sphere(other, self)

    def _connect_plane(self, other):
        c = _connect_sphere_plane(self, other)
        if c:
            return c


class Plane(object):
    # n.p = k, where n is normal, p is point on plane, k is constant scalar

    def __init__(self, *args):
        if len(args) == 3:
            assert isinstance(args[0], Point3) and \
                   isinstance(args[1], Point3) and \
                   isinstance(args[2], Point3)
            self.n = (args[1] - args[0]).cross(args[2] - args[0])
            self.n.normalize()
            self.k = self.n.dot(args[0])
        elif len(args) == 2:
            if isinstance(args[0], Point3) and isinstance(args[1], Vector3):
                self.n = args[1].normalized()
                self.k = self.n.dot(args[0])
            elif isinstance(args[0], Vector3) and type(args[1]) == float:
                self.n = args[0].normalized()
                self.k = args[1]
            else:
                raise AttributeError('%r' % (args,))

        else:
            raise AttributeError('%r' % (args,))

        if not self.n:
            raise AttributeError('Points on plane are colinear')

    @property
    def copy(self):
        return self.__class__(self.n, self.k)

    def __repr__(self):
        return 'Plane(<%.2f, %.2f, %.2f>.p = %.2f)' % \
               (self.n.x, self.n.y, self.n.z, self.k)

    def _get_point(self):
        # Return an arbitrary point on the plane
        if self.n.z:
            return Point3(0., 0., self.k / self.n.z)
        elif self.n.y:
            return Point3(0., self.k / self.n.y, 0.)
        else:
            return Point3(self.k / self.n.x, 0., 0.)

    def _apply_transform(self, t):
        p = t * self._get_point()
        self.n *= t
        self.k = self.n.dot(p)

    def intersect(self, other):
        return other._intersect_plane(self)

    def _intersect_line3(self, other):
        return _intersect_line3_plane(other, self)

    def _intersect_plane(self, other):
        return _intersect_plane_plane(self, other)

    def connect(self, other):
        return other._connect_plane(self)

    def _connect_point3(self, other):
        return _connect_point3_plane(other, self)

    def _connect_line3(self, other):
        return _connect_line3_plane(other, self)

    def _connect_sphere(self, other):
        return _connect_sphere_plane(other, self)

    def _connect_plane(self, other):
        return _connect_plane_plane(other, self)


vec2 = Vector2
vec3 = Vector3
mat3 = Matrix3
mat4 = Matrix4
