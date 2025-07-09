# fuzzy_controller.py
# Módulo que define la lógica difusa para controlar el tiempo de luz verde en función del tráfico

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definición de variables difusas
ns_density = ctrl.Antecedent(np.arange(0, 21, 1), 'ns_density')  # Cantidad de autos en Norte-Sur
ew_density = ctrl.Antecedent(np.arange(0, 21, 1), 'ew_density')  # Cantidad de autos en Este-Oeste
green_time = ctrl.Consequent(np.arange(5, 61, 1), 'green_time')  # Tiempo de luz verde en segundos

# Funciones de membresía para densidades
ns_density['bajo'] = fuzz.trimf(ns_density.universe, [0, 0, 10])
ns_density['medio'] = fuzz.trimf(ns_density.universe, [5, 10, 15])
ns_density['alto'] = fuzz.trimf(ns_density.universe, [10, 20, 20])

ew_density['bajo'] = fuzz.trimf(ew_density.universe, [0, 0, 10])
ew_density['medio'] = fuzz.trimf(ew_density.universe, [5, 10, 15])
ew_density['alto'] = fuzz.trimf(ew_density.universe, [10, 20, 20])

# Funciones de membresía para tiempo de luz verde
green_time['corto'] = fuzz.trimf(green_time.universe, [5, 10, 20])
green_time['medio'] = fuzz.trimf(green_time.universe, [15, 30, 45])
green_time['largo'] = fuzz.trimf(green_time.universe, [30, 60, 60])

# Reglas difusas
rule1 = ctrl.Rule(ns_density['alto'] & ew_density['bajo'], green_time['largo'])
rule2 = ctrl.Rule(ns_density['medio'] & ew_density['medio'], green_time['medio'])
rule3 = ctrl.Rule(ns_density['bajo'] & ew_density['alto'], green_time['corto'])
rule4 = ctrl.Rule(ns_density['medio'] & ew_density['alto'], green_time['corto'])
rule5 = ctrl.Rule(ns_density['alto'] & ew_density['alto'], green_time['medio'])
rule6 = ctrl.Rule(ns_density['bajo'] & ew_density['bajo'], green_time['medio'])

# Sistema de control difuso
fuzzy_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
fuzzy_simulator = ctrl.ControlSystemSimulation(fuzzy_ctrl)

def get_green_time(ns_count, ew_count):
    fuzzy_simulator.input['ns_density'] = ns_count
    fuzzy_simulator.input['ew_density'] = ew_count
    fuzzy_simulator.compute()
    return int(fuzzy_simulator.output['green_time'])