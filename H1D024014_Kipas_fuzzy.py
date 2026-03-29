# import library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ── Antecedent (input) variables ──────────────────────────────────────────────
suhu      = ctrl.Antecedent(np.arange(0, 41, 1),  'suhu')       # 0–40 °C
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan') # 0–100 %

# ── Consequent (output) variable ──────────────────────────────────────────────
kecepatan_kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan_kipas') # 0–100

# ── Fuzzy sets: Suhu ──────────────────────────────────────────────────────────
suhu['rendah']  = fuzz.trapmf(suhu.universe, [0,  0,  10, 20])
suhu['sedang']  = fuzz.trimf(suhu.universe,  [10, 20, 30])
suhu['tinggi']  = fuzz.trapmf(suhu.universe, [20, 30, 40, 40])

# ── Fuzzy sets: Kelembapan ────────────────────────────────────────────────────
kelembapan['rendah']  = fuzz.trapmf(kelembapan.universe, [0,  0,  25, 50])
kelembapan['sedang']  = fuzz.trimf(kelembapan.universe,  [25, 50, 75])
kelembapan['tinggi']  = fuzz.trapmf(kelembapan.universe, [50, 75, 100, 100])

# ── Fuzzy sets: Kecepatan Kipas ───────────────────────────────────────────────
kecepatan_kipas['lambat']  = fuzz.trapmf(kecepatan_kipas.universe, [0,  0,  20, 40])
kecepatan_kipas['sedang']  = fuzz.trimf(kecepatan_kipas.universe,  [30, 50, 70])
kecepatan_kipas['cepat']   = fuzz.trapmf(kecepatan_kipas.universe, [60, 80, 100, 100])

# ── Fuzzy Rules ───────────────────────────────────────────────────────────────
# Rule 1: Jika suhu rendah DAN kelembapan rendah → kipas lambat
rule1 = ctrl.Rule(suhu['rendah'] & kelembapan['rendah'], kecepatan_kipas['lambat'])

# Rule 2: Jika suhu sedang ATAU kelembapan sedang → kipas sedang
rule2 = ctrl.Rule(suhu['sedang'] | kelembapan['sedang'], kecepatan_kipas['sedang'])

# Rule 3: Jika suhu tinggi DAN kelembapan tinggi → kipas cepat
rule3 = ctrl.Rule(suhu['tinggi'] & kelembapan['tinggi'], kecepatan_kipas['cepat'])

# Rule 4: Jika suhu tinggi saja → kipas sedang-cepat
rule4 = ctrl.Rule(suhu['tinggi'] & kelembapan['rendah'], kecepatan_kipas['sedang'])

# Rule 5: Jika kelembapan tinggi saja → kipas sedang-cepat
rule5 = ctrl.Rule(suhu['rendah'] & kelembapan['tinggi'], kecepatan_kipas['sedang'])

# ── Control System ────────────────────────────────────────────────────────────
engine = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
system = ctrl.ControlSystemSimulation(engine)

# ── Simulasi ──────────────────────────────────────────────────────────────────
system.input['suhu']       = 30   # °C
system.input['kelembapan'] = 70   # %

system.compute()

print(f"Kecepatan Kipas: {system.output['kecepatan_kipas']:.2f}")
kecepatan_kipas.view(sim=system)
input("Tekan Enter untuk keluar...")