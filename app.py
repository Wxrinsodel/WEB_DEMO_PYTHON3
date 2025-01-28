
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid

app = Flask(__name__)

# Ensure the static/images directory exists
if not os.path.exists('static/images'):
    os.makedirs('static/images')

# Available functions for plotting
FUNCTIONS = {
    'sin': np.sin,
    'cos': np.cos,
    'x^2': lambda x: x**2,
    'sqrt(x)': lambda x: np.sqrt(np.abs(x)),  # Using abs to avoid negative sqrt
    'tan': np.tan,
    'exp': np.exp
}

# Available colors for plotting
COLORS = {
    'blue': '#1f77b4',
    'red': '#d62728',
    'green': '#2ca02c',
    'purple': '#9467bd',
    'orange': '#ff7f0e'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        try:
            x_from = float(request.form['x_from'])
            x_to = float(request.form['x_to'])
            
            
            selected_functions = request.form.getlist('functions')
            selected_colors = request.form.getlist('colors')
            plot_type = request.form.get('plot_type', 'single')
            
            if not selected_functions:
                raise ValueError("Please select at least one function")
            
            
            plot_filename = f"plot_{uuid.uuid4().hex[:8]}.png"
            plot_path = os.path.join('static/images', plot_filename)
            
            if plot_type == 'single':
                
                create_single_plot(x_from, x_to, selected_functions, selected_colors, plot_path)
                plots = [plot_filename]
            else:
                
                plots = create_multiple_plots(x_from, x_to, selected_functions, selected_colors)
            
            return render_template('plotter.html',
                                plots=plots,
                                functions=list(FUNCTIONS.keys()),
                                colors=list(COLORS.keys()),
                                show_plot=True,
                                x_from=x_from,
                                x_to=x_to)

        except ValueError as e:
            return render_template('plotter.html',
                                error=str(e),
                                functions=list(FUNCTIONS.keys()),
                                colors=list(COLORS.keys()))

    # GET request - show empty form
    return render_template('plotter.html',
                         functions=list(FUNCTIONS.keys()),
                         colors=list(COLORS.keys()))

def create_single_plot(x_from, x_to, selected_functions, selected_colors, plot_path):
    x = np.linspace(x_from, x_to, 500)
    plt.figure(figsize=(10, 6))
    
    for i, func_name in enumerate(selected_functions):
        color = COLORS[selected_colors[i]] if i < len(selected_colors) else None
        y = FUNCTIONS[func_name](x)
        plt.plot(x, y, color=color, label=func_name)
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Combined Plot of Selected Functions')
    plt.grid(True)
    plt.legend()
    plt.savefig(plot_path)
    plt.close()

def create_multiple_plots(x_from, x_to, selected_functions, selected_colors):
    plot_files = []
    x = np.linspace(x_from, x_to, 500)
    
    for i, func_name in enumerate(selected_functions):
        plot_filename = f"plot_{uuid.uuid4().hex[:8]}.png"
        plot_path = os.path.join('static/images', plot_filename)
        
        plt.figure(figsize=(8, 5))
        color = COLORS[selected_colors[i]] if i < len(selected_colors) else None
        y = FUNCTIONS[func_name](x)
        plt.plot(x, y, color=color, label=func_name)
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Plot of {func_name}')
        plt.grid(True)
        plt.legend()
        plt.savefig(plot_path)
        plt.close()
        
        plot_files.append(plot_filename)
    
    return plot_files

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)