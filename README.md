# excercise2

The program is intended to run on Ubuntu linux, running it on other OS might cause failures.

# Install dependencies:

pip install matplotlib

pip install numpy

pip install tikzplotlib

# Run the program

Run the python script to run the program.

# Types of plots

The program has two kinds of plots, a static plot and a dynamic plot. They can both be used by creating an instance and then running their respective run() function.
For example:

myPlot = staticPlot(x_min=0, x_max=5,x_label="t", y_label="h(t)", expression=h, res=0.01)

myPlot.run()

or

myPlot = dynamicPlot(x_label="t", y_label="h(t)", expression=h, res=0.01)


myPlot.run()
