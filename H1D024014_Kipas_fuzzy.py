import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

suhu      = ctrl.Antecedent(np.arange(0, 41, 1),  'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')

kecepatan_kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan_kipas')

suhu['rendah']  = fuzz.trapmf(suhu.universe, [0,  0,  10, 20])
suhu['sedang']  = fuzz.trimf(suhu.universe,  [10, 20, 30])
suhu['tinggi']  = fuzz.trapmf(suhu.universe, [20, 30, 40, 40])

kelembapan['rendah']  = fuzz.trapmf(kelembapan.universe, [0,  0,  25, 50])
kelembapan['sedang']  = fuzz.trimf(kelembapan.universe,  [25, 50, 75])
kelembapan['tinggi']  = fuzz.trapmf(kelembapan.universe, [50, 75, 100, 100])

kecepatan_kipas['lambat']  = fuzz.trapmf(kecepatan_kipas.universe, [0,  0,  20, 40])
kecepatan_kipas['sedang']  = fuzz.trimf(kecepatan_kipas.universe,  [30, 50, 70])
kecepatan_kipas['cepat']   = fuzz.trapmf(kecepatan_kipas.universe, [60, 80, 100, 100])

rule1 = ctrl.Rule(suhu['rendah'] & kelembapan['rendah'], kecepatan_kipas['lambat'])
rule2 = ctrl.Rule(suhu['sedang'] | kelembapan['sedang'], kecepatan_kipas['sedang'])
rule3 = ctrl.Rule(suhu['tinggi'] & kelembapan['tinggi'], kecepatan_kipas['cepat'])
rule4 = ctrl.Rule(suhu['tinggi'] & kelembapan['rendah'], kecepatan_kipas['sedang'])
rule5 = ctrl.Rule(suhu['rendah'] & kelembapan['tinggi'], kecepatan_kipas['sedang'])

engine = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
system = ctrl.ControlSystemSimulation(engine)

system.input['suhu']       = 30
system.input['kelembapan'] = 70

system.compute()

print(f"Kecepatan Kipas: {system.output['kecepatan_kipas']:.2f}")
kecepatan_kipas.view(sim=system)
input("Tekan Enter untuk keluar...")
