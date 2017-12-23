# -*- coding: utf-8 -*-
# @Date    : 2017-12-22 16:30:40
# @Author  : J. W. Huang (huangjasper@126.com)

import numpy as np
import sys
import logging
import LUT

logging.basicConfig(level = logging.INFO)

class LatticeParameter(object):
	"""include lattice parameters"""

	def __init__(self, arr):
		super(LatticeParameter, self).__init__()
		if len(arr) == 6:
			self.a, self.b, self.c, self.alpha, self.beta, self.gamma = arr[0], arr[1], arr[2], np.deg2rad(arr[3]), np.deg2rad(arr[4]), np.deg2rad(arr[5])
		elif arr.shape == (3,3):
			va, vb, vc = arr
			self.a, self.b, self.c = Length(va), Length(vb), Length(vc)
			self.alpha = Angle_between_2vector(vb, vc)
			self.beta = Angle_between_2vector(vc, va)
			self.gamma = Angle_between_2vector(va, vb)

		logging.info('lattice parameters = (%f %f %f %f %f %f)'%(self.a, self.b, self.c, np.rad2deg(self.alpha), np.rad2deg(self.beta), np.rad2deg(self.gamma)))
		if not self.isvalid():
			logging.error('lattice parameter is invalid!')

	def isvalid(self):
		if self.a <= 0 or self.b <= 0 or self.c <= 0:
			return False

		for angle in (self.alpha, self.beta, self.gamma):
			if angle >= np.pi or angle <= 0:
				return False
		return True

	@property
	def direct_matrix(self):
		v1 = self.a*np.array((1,0,0))
		v2 = self.b*np.array((np.cos(self.gamma),np.sin(self.gamma),0))
		v3 = self.c*Norm_vector((np.cos(self.beta),(np.cos(self.alpha)-np.cos(self.beta)*np.cos(self.gamma))/np.sin(self.gamma)))
		m = np.vstack((v1,v2,v3))

		logging.info('Direct matrix is\t, (%s)'%(','.jion(m.flatten.tolist())))
		return m

	@property
	def reciprocal_matrix(self):
		def Calc_reciprocal_vectors(v):
			return np.vstack((np.cross(v[1],v[2]),np.cross(v[2],v[0]),np.cross(v[0],v[1])))/linalg.det(v)
		m = Calc_reciprocal_vectors(self.direct_matrix)

		logging.info('Reciprocal matrix is\t, (%s)'%(','.jion(m.flatten.tolist())))
		return m

	def report(self, fout = None):
		if fout != None:
			printfile = functools.partial(print, file = fout)
		else:
			printfile = print

		printfile('\ta = ', self.a, '\n\tb = ', self.b, '\n\tc = ',self.c)
		printfile('\talpha = ', np.rad2deg(self.alpha), '\n\tbeta = ', np.rad2deg(self.beta), '\n\tgamma = ', np.rad2deg(self.gamma))


class Atom(object):
	def __init__(self, element, atomcoor):
		super(Atom, self).__init__()

		if type(element) is str:
			self.element = Element(element)
		else:
			self.element = element
		if type(atomcoor) is FracCoor:
			self.coor = atomcoor
		else:
			self.coor = FracCoor(atomcoor)

class FracCoor(object):
	def __init__(self, coors):
		super(FracCoor, self).__init__()

		if len(coors) == 3:
			pass
		else:
			logging.error('Coordinates are not 3-dimensional')
		
		for coor in coors:
			if coor < 0 or coor >1:
				logging.error('Fractional coordinates exceeds 0 ~ 1!')

		self.iter = np.array(coors)

	@property
	def x(self):
		return self.iter[0]

	@property
	def y(self):
		return self.iter[1]

	@property
	def z(self):
		return self.iter[2]

class Element(object):
	def __init__(self, name):
		super(Element, self).__init__()

		self.name, self.mass, self.scatter_factor = LUT.dict_element[name]

class Lattice(object):
	def __init__(self):
		super(Lattice, self).__init__()

		self.LP = NULL
		self.atoms = []

	def addLatticeParameter(self, latticeprameter):
		if not type(latticeprameter) is LatticeParameter:
			logging.error('argument should be type \'LatticeParameter\'')

		self.LP = latticeprameter

	def addAtoms(self, atom):
		if not type(atom) is Atom:
			logging.error('argument shoulde be type \'Atom\'')

		self.atoms.append(atom)

	def 

class Fcc(Lattice):
	def __init__(self, element, a):
		super(Fcc, self).__init__()

		self.addLatticeParameter(LatticeParameter(a,a,a,90,90,90))
		coors = ((0,0,0),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5))
		for coor in coors:
			self.addAtoms(Atom(element,coor))

		logging.info('init of fcc is done')

class SimpleCubic(Lattice):
	def __init__(self, element, a):
		super(SimpleCubic, self).__init__()

		self.addLatticeParameter(LatticeParameter(a,a,a,90,90,90))
		coors = ((0,0,0))
		for coor in coors:
			self.addAtoms(Atom(element,coor))

		logging.info('init of simplecubic is done')

class Bcc(Lattice):
	def __init__(self, element, a):
		super(Bcc, self).__init__()

		self.addLatticeParameter(LatticeParameter(a,a,a,90,90,90))
		coors = ((0,0,0),(0.5,0.5,0.5))
		for coor in coors:
			self.addAtoms(Atom(element,coor))

		logging.info('init of bcc is done')

