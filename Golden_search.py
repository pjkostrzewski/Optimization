from math import sqrt
import numpy as np
import random
import parser
from copy import deepcopy

class GoldenSearch:

    def __init__(self, a, b, list_of_starters, absolute_precision, formula):
        self.x = np.linspace(a, b, 13)  # 13
        self.y = np.linspace(a, b, 13)
        self.a = a
        self.b = b
        self.absolute_precision = absolute_precision
        self.digit_of_precision = self.from_precision_to_digit()
        self.phi = (1 + sqrt(5)) / 2
        self.resphi = 2 - self.phi
        self.start_point = random.uniform(a,b)
        self.formula = formula
        self.results = {}
        self.starters_to_dict_results(list_of_starters)
        self.temp_function = ""
        self.points = []
        self.results_of_function = []

    def oblicz_wartosc_funkcji(self, number_of_variables):
        if number_of_variables == 2:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
        if number_of_variables == 3:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
        if number_of_variables == 4:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
            x3 = float(self.points[-1]["x3"])
        if number_of_variables == 5:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
            x3 = float(self.points[-1]["x3"])
            x4 = float(self.points[-1]["x4"])
        if number_of_variables == 6:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
            x3 = float(self.points[-1]["x3"])
            x4 = float(self.points[-1]["x4"])
            x5 = float(self.points[-1]["x5"])
        if number_of_variables == 7:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
            x3 = float(self.points[-1]["x3"])
            x4 = float(self.points[-1]["x4"])
            x5 = float(self.points[-1]["x5"])
            x6 = float(self.points[-1]["x6"])
        if number_of_variables == 8:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
            x3 = float(self.points[-1]["x3"])
            x4 = float(self.points[-1]["x4"])
            x5 = float(self.points[-1]["x5"])
            x6 = float(self.points[-1]["x6"])
            x7 = float(self.points[-1]["x7"])
        if number_of_variables == 9:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
            x3 = float(self.points[-1]["x3"])
            x4 = float(self.points[-1]["x4"])
            x5 = float(self.points[-1]["x5"])
            x6 = float(self.points[-1]["x6"])
            x7 = float(self.points[-1]["x7"])
            x8 = float(self.points[-1]["x8"])
        if number_of_variables == 10:
            x0 = float(self.points[-1]["x0"])
            x1 = float(self.points[-1]["x1"])
            x2 = float(self.points[-1]["x2"])
            x3 = float(self.points[-1]["x3"])
            x4 = float(self.points[-1]["x4"])
            x5 = float(self.points[-1]["x5"])
            x6 = float(self.points[-1]["x6"])
            x7 = float(self.points[-1]["x7"])
            x8 = float(self.points[-1]["x8"])
            x9 = float(self.points[-1]["x9"])
        return eval(self.formula)

    def starters_to_dict_results(self, list_of_starters):
        length = len(list_of_starters)
        for i in range(length):
            self.results.update({"x"+str(i) : str(list_of_starters[i])})

    def from_precision_to_digit(self):
        return len(str(self.absolute_precision))-2


    def goldenSectionSearch(self, f, a, c, b):
        if abs(a - b) < self.absolute_precision:
            return (a + b) / 2
        d = c + self.resphi * (b - c)
        if f(d) < f(c):
            return self.goldenSectionSearch(f, c, d, b)
        else:
            return self.goldenSectionSearch(f, d, c, a)

    def modify_formula(self):
        self.formula = self.replace_power_symbol(self.formula)
        self.formula = self.add_np_to_functions(self.formula)

    def replace_power_symbol(self, expression):
        return expression.replace('^','**')

    def add_np_to_functions(self, expression):
        functions = ["log", "sin", "cos", "tan", "exp", "sqrt"]
        for fun in functions:
            expression = expression.replace(fun, "np."+fun)
        return expression

    def compile(self, x, formula):
        return eval(parser.expr(formula).compile())

    def func(self, x):
        return eval(self.formula)


    def one_variable_function(self, variable, dict):
        self.temp_function = self.formula
        self.formula = self.formula.replace(variable, 'x')
        for key, value in dict.items():
            self.formula =self.formula.replace(key, value)

    def backup_function(self):
        self.formula = self.temp_function
        self.temp_function = ""

    def test_search(self, iterations, number_of_variables, dynamically):
        self.modify_formula()
        flag = True
        temp = deepcopy(self.results)
        self.points.append(temp)
        counter = 0
        self.results_of_function.append(self.oblicz_wartosc_funkcji(number_of_variables))
        valid = 0
        for _ in range(iterations):
            if flag == False:
                break
            for key in self.results.keys():
                counter += 1
                self.one_variable_function(key, self.results)
                piwot = (-1 + self.resphi*2)#(sqrt(5)-1)/2 #0.6180339887498949
                piwot = piwot*(-1) if float(self.points[-1][key]) <= 0 else piwot
                if dynamically == True:
                    result = self.goldenSectionSearch(self.func,
                                                      float(self.points[-1][key])-2 if float(self.points[-1][key])-2 > self.a else self.a,
                                                      float(self.points[-1][key])+piwot,
                                                      float(self.points[-1][key])+2 if float(self.points[-1][key])+2 < self.b else self.b) #self.start_point
                else:
                    result = self.goldenSectionSearch(self.func, self.a ,  piwot, self.b)
                result = round(result, self.digit_of_precision)
                difference = abs(round(float(self.points[-1][key]), self.digit_of_precision) - result) < self.absolute_precision
                if counter >= iterations:
                    flag = False
                    break
                self.results.update({key : str(result)})
                temp = deepcopy(self.results)

                self.points.append(temp)
                self.backup_function()
                self.results_of_function.append(self.oblicz_wartosc_funkcji(number_of_variables))
                if self.results_of_function[-2] == self.results_of_function[-1]:
                    valid += 1
                    del self.points[-1]
                if valid >= 3*number_of_variables+1:
                    print(number_of_variables)
                    print(valid)
                    flag = False
                    break
                # if abs(diff) <= self.absolute_precision:
                #     del self.points[-1]
                #     flag = False
                #     break
