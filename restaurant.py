#import library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#preparing fuzzy variables
food = ctrl.Antecedent(np.arange(0,11), 'food')
service = ctrl.Antecedent(np.arange(0,11), 'service')
tip = ctrl.Consequent(np.arange(0,11), 'tip')

# food taste
food['bad'] = fuzz.trimf(food.universe, [0, 2, 4])
food['decent'] = fuzz.trimf(food.universe, [3, 5, 7])
food['delicious'] = fuzz.trimf(food.universe, [6, 8, 10])

# service quality
service['rude'] = fuzz.trimf(service.universe, [0, 2, 4])
service['ok'] = fuzz.trimf(service.universe, [3, 5, 7])
service['excellent'] = fuzz.trimf(service.universe, [6, 8, 10])

# restaurant tip
tip['low'] = fuzz.trimf(tip.universe, [0, 2, 4])
tip['medium'] = fuzz.trimf(tip.universe, [3, 5, 7])
tip['high'] = fuzz.trimf(tip.universe, [6, 8, 10])



# rules
rule1 = ctrl.Rule(food['bad'] & service['rude'],
tip['low'])
rule2 = ctrl.Rule(food['decent'] | service['ok'],
tip['medium'])
rule3 = ctrl.Rule(food['delicious'] | service['excellent'],
tip['high'])

engine = ctrl.ControlSystem([rule1, rule2, rule3])
system = ctrl.ControlSystemSimulation(engine)

# input
system.input['food'] = 5.5
system.input['service'] = 7
system.compute()
print(system.output['tip'])
 
# output
tip.view(sim=system)
food.view(sim=system)
service.view(sim=system)
input("enter to exit..")