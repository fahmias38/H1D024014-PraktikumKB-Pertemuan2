# import library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# preparing fuzzy variables
cost = ctrl.Antecedent(np.arange(0,1001), 'cost')
request = ctrl.Antecedent(np.arange(0,60), 'request')
production = ctrl.Consequent(np.arange(0,100), 'production')

# production cost
cost['low'] = fuzz.zmf(cost.universe, 0, 500)
cost['medium'] = fuzz.pimf(cost.universe, 0, 500, 500, 1000)
cost['high'] = fuzz.smf(cost.universe, 500, 1000)

# production request
request['decrease'] = fuzz.trapmf(request.universe, [0,0,10,30])
request['stable'] = fuzz.trimf(request.universe, [10,30,50])
request['increase'] = fuzz.trapmf(request.universe, [30,50,60,60])

# production total
production['reduce'] = fuzz.trapmf(production.universe, [0,0,10,50])
production['normal'] = fuzz.trimf(production.universe, [30,50,70])
production['grow'] = fuzz.trapmf(production.universe, [50,90,100,100])

rule1 = ctrl.Rule(cost['low'] & request['increase'], production['grow'])
rule2 = ctrl.Rule(cost['medium'], production['normal'])
rule3 = ctrl.Rule(cost['high'] & request['decrease'], production['reduce'])

engine = ctrl.ControlSystem([rule1, rule2, rule3])
system = ctrl.ControlSystemSimulation(engine)

system.input['cost'] = 500
system.input['request'] = 30
system.compute()
print(system.output['production'])
production.view()
input("enter to continue")