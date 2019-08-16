import parser
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from guizero import App, PushButton, TextBox, ListBox, CheckBox, Text
import matplotlib
import matplotlib.cm as cm
import Golden_search
import random


class AppGui:
    def __init__(self, resolution, black_mode=0):
        self.app = App(title="Gauss-Seidel", bg="#A4DDCA", layout="grid", height=900, width=1200) ##f79be0

        self.list_of_functions = ["(x0^2+x1-11)^2 + (x0+x1^2-7)^2-200", "(x1^2+x0-11)^2 + (x1+x0^2-7)^2-200",
                                  "(x0-2)^2 +(x0-x1^2)^2", "x0^2+x1^2", "x0^4+x1^4-x0^2-x1^2", "x0+x1+x2",
                                  "x0+x1+x2+x3+x4+x5+x6+x7+x8+x9", "x0^2-cos(18*x0)+x1^2-cos(18*x1)",
                                  "x0^2-cos(18*x0)+x1^2-cos(18*x1)+x2^2-cos(18*x2)" ]
        self.list_of_iterations = []
        self.list_of_results = []
        self.list_of_starters = [-3, 4]
        self.listbox = ListBox(self.app, items=self.list_of_functions, grid=[4, 1], command=self.change, scrollbar=True, align="left", width= 300, height=200)
        self.function_plot = PushButton(self.app, command=self.start_plot, grid=[0, 0], text="3D function", width=20)
        self.contour_plot = PushButton(self.app, command=self.start_contour, grid=[1, 0], text="Contours", width=20)
        self.checkbox = CheckBox(self.app, grid=[0, 1], align="left", text="Black mode")
        self.checkbox2 = CheckBox(self.app, grid=[0, 2], align="left", text="dynamically")
        self.text_range_a = Text(self.app, text="Function: ", grid=[3, 0], width=14)
        self.input_box = TextBox(self.app, grid= [4, 0], text= self.list_of_functions[0] , width=60)
        self.append_button = PushButton(self.app, grid=[5,0], text="Add", align="left",
                                        command=self.append_to_list, width=5, height=1)
        self.text_range_a = Text(self.app, text= "Range: ", grid=[0,2])
        self.range_a = TextBox(self.app, grid= [1, 2], align="left", text= -5, width=5)
        self.range_b = TextBox(self.app, grid=[1, 2], align="right", text=5, width=5)
        self.precision_text = Text(self.app, text= "Precision: ", grid=[0,3])
        self.precision_box = TextBox(self.app, grid=[1, 3], align="right", text=0.0001, width=10)
        self.precision = self.precision_box.get()
        self.text_range_a = Text(self.app, text= "Start points: ", grid=[0,4], width=10)
        self.start_points = TextBox(self.app, grid= [1, 4], text= self.list_of_starters, width=20)
        self.start = self.start_points.get()
        self.activate = PushButton(self.app, grid=[0, 5], text="Activate", command=self.activate_params, width=20, height=2)
        self.activate = PushButton(self.app, grid=[1, 5], text="Start", command=self.start_algorithm, width=20, height=2)
        self.iteration_points_text = Text(self.app, text="Iteration points", grid= [0, 6, 2, 6], align="top")
        self.iteration_points_box = ListBox(self.app, items=self.list_of_iterations, grid=[0, 7, 2, 7], command=self.change, scrollbar=True, width=650, height=400)
        self.results_points_box = ListBox(self.app, items=self.list_of_results, grid=[3, 7], scrollbar=True, width=80, height=400)
        self.number_of_iterations = Text(self.app, grid= [4,6], text= "{} iteracji".format(len(self.list_of_iterations)), align="left")
        self.random_button = PushButton(self.app, grid=[2, 4], text= "Random", align="right", command=self.random_start_points, width=5, height=1)
        self.random_button = PushButton(self.app, grid=[1, 4], text="validate", align="right",
                                        command=self.change_starters, width=5, height=1)
        self.iterations = TextBox(self.app, grid=[4, 5], text= "1000", width=6, align="left")
        self.iterations_text = Text(self.app, grid=[3, 5], text="max iterations:", align="left")
        self.resolution = resolution
        self.x_range = int(self.range_a.get())
        self.y_range = int(self.range_b.get())
        self.x = np.linspace(self.x_range, self.y_range, resolution)  # 13
        self.y = np.linspace(self.x_range, self.y_range, resolution)
        self.black_mode = black_mode

        self.points_x = []
        self.points_y = []
        self.points_z = []

        self.start_app()
        self.formula = ""
    def append_to_list(self):
        formula = self.input_box.get()
        self.list_of_functions.append(formula)
        self.listbox.append(formula)

    def change_starters(self):
        temp = self.start_points.get()
        temp = temp[1:-1]
        temp = temp.split(",")
        temp_list = []
        for element in temp:
            temp_list.append(float(element))
        temp = [float(i) for i in temp]
        print(temp)
        self.start_points.set(temp)
        self.list_of_starters = temp

    def count_variables(self):
        formula = self.get_formula_and_refactor()
        print(formula)
        variables = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"]
        for v in variables:
            if v not in formula:
                print(v)
                print(variables.index(v))
                return variables.index(v)
        return 10

    def activate_params(self):
        self.x_range = int(self.range_a.get())
        self.y_range = int(self.range_b.get())
        self.x = np.linspace(self.x_range, self.y_range, self.resolution)  # 13
        self.y = np.linspace(self.x_range, self.y_range, self.resolution)
        self.start = self.start_points.get()

        self.precision = self.precision_box.get()
        self.points_x.clear()
        self.points_y.clear()
        self.points_z.clear()
        self.iteration_points_box.clear()
        self.number_of_iterations.clear()
        self.list_of_iterations.clear()
        self.list_of_results.clear()
        self.results_points_box.clear()
        self.formula = self.input_box.get()

    def start_algorithm(self):
        self.golden_search = Golden_search.GoldenSearch(self.x_range, self.y_range, self.list_of_starters,
                                                        float(self.precision), self.formula)
        self.golden_search.test_search(int(self.iterations.get()), self.count_variables(), self.checkbox2.get_value())
        self.list_of_iterations = self.golden_search.points
        self.list_of_results = self.golden_search.results_of_function
        self.iterations_to_box()
        self.results_to_box()
        self.number_of_iterations.set("{} iteracji".format(len(self.list_of_iterations)))

    def iterations_to_box(self):
        for element in self.list_of_iterations:
            self.iteration_points_box.append(element)

    def results_to_box(self):
        for element in self.list_of_results:
            self.results_points_box.append(str(round(float(element),4)))

    def return_result_of_function(self, x0, x1, f):
        return eval(f)

    def random_start_points(self):
        temp = []
        for _ in range(self.count_variables()):
            temp.append(round(random.uniform(float(self.range_a.get()), float(self.range_b.get())),3))
        self.start_points.set(temp)
        self.list_of_starters = temp

    def replace_power_symbol(self, expression):
        return expression.replace('^','**')

    def add_np_to_functions(self, expression):
        functions = ["log", "sin", "cos", "tan", "exp", "sqrt"]
        for fun in functions:
            expression = expression.replace(fun, "np."+fun)
        return expression

    def compile(self, formula, x0, x1, x2=0): #x0, x1
        return eval(parser.expr(formula).compile())

    def set_xyz_labels(self, ax):
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        return ax

    def create_new_3d_plot(self, formula, x, y):
        fig = plt.figure()
        X, Y = np.meshgrid(x, y)
        Z = self.compile(formula, X, Y)
        ax = plt.axes(projection='3d')
        ax = self.set_xyz_labels(ax)
        if self.checkbox.get_value()==False:
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='black')
        else:
            ax.contour3D(X, Y, Z, 50, cmap='binary')
        plt.show()


    def create_contours(self, formula, x, y, points):
        fig, ax = plt.subplots()
        X, Y = np.meshgrid(x, y)
        Z = self.compile(formula, X, Y)
        CS = ax.contour(X, Y, Z, levels=50)
        ax.clabel(CS, inline=1, fontsize=8)
        points_x = []
        points_y = []
        for dict in points:
            points_x.append(float(dict["x0"]))
            points_y.append(float(dict["x1"]))
        plt.plot(points_x, points_y, linestyle="--", marker="o", color="r")
        # size = max(float(self.range_a.get()), float(self.range_b.get()))
        plt.show()

    def get_formula_and_refactor(self):
        formula = self.input_box.get()
        formula = self.replace_power_symbol(formula)
        formula = self.add_np_to_functions(formula)
        return formula

    def start_plot(self):
        formula = self.get_formula_and_refactor()
        return self.create_new_3d_plot(formula, self.x, self.y)

    def start_contour(self):
        formula = self.get_formula_and_refactor()
        print(self.list_of_iterations)
        return self.create_contours(formula, self.x, self.y, self.list_of_iterations)

    def change(self, value):
        self.input_box.set(value)
        self.function_plot.enabled = self.count_variables() == 2
        self.contour_plot.enabled = self.count_variables()  == 2
        self.checkbox.enabled = self.count_variables()  == 2

    def start_app(self):
        self.app.display()

if __name__ == '__main__':
    a = AppGui(resolution=30, black_mode=1)
