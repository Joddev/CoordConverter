from math import tan, cos, sqrt, pi, sin

class LatLng:
	def __init__(self, latitude, longitude):
		# save as radian
		self.latitude = latitude * pi / 180
		self.longitude = longitude * pi / 180

class Coords:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Ellipsoid:
	def __init__(self, a, f, dY, dX):
		#장반경
		self.a = a
		#단반경
		b = a * (1 - f)
		self.b = b
		#편평률
		self.f = f
		#원점 가산값
		self.dY = dY
		self.dX = dX
		#제1이심률
		self.e1sq = (pow(a,2)-pow(b,2)) / pow(a,2)
		#제2이심률
		self.e2sq = (pow(a,2)-pow(b,2)) / pow(b,2)
	
	# 자오 선호장 계산
	def getM(self, target):
		return self.a * (
			(1-self.e1sq/4-3*pow(self.e1sq,2)/64-5*pow(self.e1sq,3)/256)*target.latitude -
			(3*self.e1sq/8 + 3*pow(self.e1sq,2)/32 + 45*pow(self.e1sq,3)/1024)*sin(2*target.latitude) +
			(15*pow(self.e1sq,2)/256 + 45*pow(self.e1sq,3)/1024)*sin(4*target.latitude) -
			35*pow(self.e1sq,3)/3072*sin(6*target.latitude)
		)

#서부원점
westOrigin = LatLng(38.0, 125.0)
#중부원점
midOrigin = LatLng(38.0, 127.0)
#동부원점
eastOrigin = LatLng(38.0, 129.0)
#동해원점
eastSeaOrigin = LatLng(38.0, 131.0)

#GRS80
grs80 = Ellipsoid(6378137.000, 1/298.2572221010, 200000, 600000)
#Bessel
bessel = Ellipsoid(6377397.155, 1/299.1528128000, 200000, 500000)

#원점축척계수
k = 1.0000

# 경위도 -> TM 좌표
def LatLong_to_TM(latitude, longitude, origin=midOrigin, ellipsoid=grs80):
	target = LatLng(latitude, longitude)
	T = pow(tan(target.latitude), 2)
	C = (ellipsoid.e1sq/(1-ellipsoid.e1sq)) * pow(cos(target.latitude), 2)
	A = (target.longitude - origin.longitude) * cos(target.latitude)
	N = ellipsoid.a / sqrt(1 - ellipsoid.e1sq * pow(sin(target.latitude), 2))
	M = ellipsoid.getM(target)
	M0 = ellipsoid.getM(origin)
	
	ret = {}
	ret['X'] = ellipsoid.dX + k*(M - M0 + N*tan(target.latitude)*(pow(A,2)/2 + pow(A,4)/24*(5-T+9*C+4*pow(C,2)) + pow(A,6)/720*(61-58*T+pow(T,2)+600*C-330*ellipsoid.e2sq)))
	ret['Y'] = ellipsoid.dY + k*N*(A + pow(A,3)/6*(1-T+C) + pow(A,5)/120*(5-18*T+pow(T,2)+72*C-58*ellipsoid.e2sq))
	return ret

# TM -> 경위도
def TM_to_LatLong(X, Y, origin=midOrigin, ellipsoid=grs80):
	M = ellipsoid.getM(origin) + (X - ellipsoid.dX)/k
	u1 = M / (ellipsoid.a * (1 - ellipsoid.e1sq/4 - 3*pow(ellipsoid.e1sq,2)/64 - 5*pow(ellipsoid.e1sq,3)/256))
	e1 = (1 - sqrt(1 - ellipsoid.e1sq)) / (1 + sqrt(1 - ellipsoid.e1sq))
	lat1 = u1 + (3*e1/2 - 27*pow(e1,3)/32)*sin(2*u1) + (21*pow(e1,2)/16 - 55*pow(e1,4)/32)*sin(4*u1) + 151*pow(e1,3)/96*sin(6*u1) + 1097*pow(e1,4)/512*sin(8*u1)
	R1 = (ellipsoid.a * (1-ellipsoid.e1sq)) / pow(1-ellipsoid.e1sq*pow(sin(lat1),2),3/2)
	C1 = ellipsoid.e2sq*pow(cos(lat1),2)
	T1 = pow(tan(lat1),2)
	N1 = ellipsoid.a / sqrt(1 - ellipsoid.e1sq*pow(sin(lat1),2))
	D = (Y - ellipsoid.dY) / (N1*k)

	ret = {}
	ret['latitude'] = lat1 - N1*tan(lat1)/R1 * (pow(D,2)/2 - pow(D,4)/24*(5+3*T1+10*C1-4*pow(C1,2)-9*ellipsoid.e2sq) + pow(D,6)/720*(61+90*T1+298*C1+45*pow(T1,2)-252*ellipsoid.e2sq-3*pow(C1,2)))
	ret['longtitude'] = origin.longitude + 1/cos(lat1) * (D - pow(D,3)/6*(1+2*T1+C1) + pow(D,5)/120*(5-2*C1+28*T1-3*pow(C1,2)+8*ellipsoid.e2sq+24*pow(T1,2)))
	ret['latitude'] = ret['latitude'] * 180 / pi
	ret['longtitude']= ret['longtitude'] * 180 / pi
	return ret

if __name__ == "__main__":
	print(LatLong_to_TM(37.373786305555555, 127.23560866666666))
	print(TM_to_LatLong(530522.2352,220868.8326))