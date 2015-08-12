A handy wrapper that allows somebody to quickly and easily plot equations, using [Sympy](www.sympy.org) and [Matplotlib](matplotlib.org)

## Example Usage
```python
from quiver.plotter import FieldPlotter

plotter = FieldPlotter()
plotter.set_equation_from_string('x+y')
plotter.make_plot()

with open('plot_file.png', 'w+') as output:
    plotter.write_data(output)
```
