## Quiver
A handy wrapper that allows somebody to quickly and easily plot equations, using [Sympy](www.sympy.org) and [Matplotlib](matplotlib.org).

### Motivation
When I was taking a differential equations course, as much time trying to program
decent looking plots as actually working on the problems. I wanted to create a tool
that would allow students and teachers to quickly plot direction fields, such as for a first order differential equation.

###  Example Usage
```python
from quiver.plotter import FieldPlotter

plotter = FieldPlotter()
plotter.set_equation_from_string('x+y')
plotter.make_plot()

with open('plot_file.png', 'w+') as output:
    plotter.write_data(output)
```
