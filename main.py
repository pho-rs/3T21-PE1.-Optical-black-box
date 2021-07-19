from math import *

R_0 = 300.0
N_x = 5
N_y_end = 1
N_y_start = 1
R_1 = 50.0
x_1 = 80.0
y_1 = 110.0
n_gl = 1.5
n_air = 1.0
v_0 = 0.01


class Ray:
    def __init__(self, X, Y, ANGLE):
        self.in_big = False
        self.in_small = False
        self.x = X
        self.y = Y
        self.angle = ANGLE

    def update(self):
        # преломление
        if (self.is_in_big() != self.in_big):
            # преломление на границе большого цилиндра
            delta_x = (self.x) / R_0
            if abs(delta_x) > 1:
                delta_x = delta_x / abs(delta_x)

            if (self.y>R_0):
                alpha = acos(delta_x)
            else:
                alpha = 2*pi - acos(delta_x)
            while self.angle > 2 * pi:
                self.angle = self.angle - 2 * pi
            phi = self.angle - alpha

            if ( (abs(phi) > pi/2) and (abs(phi) < (3*pi)/2) ):
                # вход луча
                if phi < 0:
                    phi += 2*pi
                if(abs(sin(pi - phi)*(n_air/n_gl))>1):
                    phi_1 = pi - phi
                else:
                    phi_1 = pi - asin( sin(pi - phi)*(n_air/n_gl) )
                self.angle = alpha + phi_1
            elif ( (abs(phi) == pi/2) or (abs(phi) == (3*pi)/2) ):
                # касание лучом
                pass
            else:
                # выход луча
                if (abs(sin(phi) * (n_gl / n_air)) > 1):
                    phi_1 = pi - phi
                else:
                    phi_1 = asin(sin(phi) * (n_gl / n_air))
                self.angle = alpha + phi_1
            self.in_big = self.is_in_big()
        elif (self.is_in_small() != self.in_small):
            # преломление на границе маленького цилиндра
            delta_x = (self.x - x_1) / R_1
            if abs(delta_x) > 1:
                delta_x = delta_x / abs(delta_x)
            if (self.y > R_0 + y_1):
                alpha = acos(delta_x)
            else:
                alpha = 2 * pi - acos(delta_x)
            while self.angle > 2 * pi:
                self.angle = self.angle - 2 * pi
            phi = self.angle - alpha

            if ((abs(phi) > pi / 2) and (abs(phi) < (3 * pi) / 2)):
                # вход луча
                if phi < 0:
                    phi += 2 * pi

                if (abs(sin(pi - phi) * (n_gl / n_air)) > 1):
                    phi_1 = pi - phi
                else:
                    phi_1 = pi - asin(sin(pi - phi) * (n_gl / n_air))

                self.angle = alpha + phi_1
            elif ((abs(phi) == pi / 2) or (abs(phi) == (3 * pi) / 2)):
                # касание лучом
                pass
            else:
                # выход луча
                if (abs(sin(phi) * (n_air / n_gl)) > 1):
                    phi_1 = pi - phi
                else:
                    phi_1 = asin(sin(phi) * (n_air / n_gl))
                self.angle = alpha + phi_1

            self.in_small = self.is_in_small()

        # перемещение
        self.x += v_0*cos(self.angle)
        self.y += v_0*sin(self.angle)

        # нормировка угла
        while (self.angle > 2*pi):
            self.angle -= 2*pi
        while (self.angle < -2*pi):
            self.angle += 2*pi

        # возвращаем координаты
        return (R_0*N_x + self.x, (2+N_y_end)*R_0 - self.y)

    def is_in_big(self):
        """
        Проверяет находится ли луч в большшом цилиндре
        :return: True/False
        """
        R = sqrt((self.x) ** 2 + (self.y - R_0) ** 2)
        if R < R_0:
            return True
        else:
            return False

    def is_in_small(self):
        """
        Проверяет находится ли луч в маленьком цилиндре
        :return: True/False
        """
        R = sqrt((self.x-x_1) ** 2 + (self.y - R_0-y_1) ** 2)
        if R < R_1:
            return True
        else:
            return False



def measuring(X_0, Y_0, angle):
    if X_0 > N_x * R_0:
        X_0 = N_x * R_0
    elif X_0 < -N_x * R_0:
        X_0 = -N_x * R_0
    while angle > pi:
        angle = angle - 2*pi
    while angle <-pi:
        angle = angle + 2*pi
    ray = Ray(X_0, -Y_0, pi/2 - angle)

    while (abs(ray.x) < R_0 * N_x) and ray.y < R_0 * (2 + N_y_end) and ray.y > -N_y_start*R_0:
        ray.update()
    if abs(ray.x) >= R_0 * N_x:
        return False
    elif ray.y <= -N_y_start*R_0:
        return False
    else:
        return ray.x


cont = True
while cont:
    tried = True
    while(tried):
        tried = False
        print("Введите координату Х: ")
        try:

            X_0 = float(input())
        except ValueError:
            tried = True
            print("Неправильный ввод")
    tried = True
    while (tried):
        tried = False
        print("Введите координату Y: ")
        try:
            Y_0 = float(input())
        except ValueError:
            tried = True
            print("Неправильный ввод")
    tried = True
    while (tried):
        tried = False
        print("Введите угол в радианах: ")
        try:
            angle = float(input())
        except ValueError:
            tried = True
            print("Неправильный ввод")
    ans = measuring(X_0, Y_0, angle)
    if not ans:
        print("Нет сигнала")
    else:
        print("Сигнал по координате: " + str(round(ans, 4)))
