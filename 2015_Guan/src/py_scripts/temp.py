import math

c = 299792458
eV_to_J = 1.60218 * 10 ** -19
u_to_kg = 1.66054 * 10 ** -27
proton_mass = 1.00727647


def beta(E, m):
    E_eV = E * eV_to_J
    m_u = m * u_to_kg
    beta2 = 1 - 1 / ((E_eV / (m_u * (c ** 2)) + 1) ** 2)
    return math.sqrt(beta2)


def zeff(z, E, m):
    b = beta(E, m)
    return z * (1 - math.exp(-130.2 * b / (z ** (2 / 3))))


def zeff2beta2(z, E, m):
    return zeff(z, E, m) ** 2 / (beta(E, m) ** 2)


print(beta(10 ** 6, 1))

print(zeff2beta2(1, 10 ** 7, 1))
