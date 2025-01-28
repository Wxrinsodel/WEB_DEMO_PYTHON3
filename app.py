
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid

app = Flask(__name__)


if not os.path.exists('static'):
    os.makedirs('static', mode=0o755)
if not os.path.exists('static/images'):
    os.makedirs('static/images', mode=0o755)

# Available functions for plotting
FUNCTIONS = {
    'sin': np.sin,
    'cos': np.cos,
    'x^2': lambda x: x**2,
    'sqrt(x)': lambda x: np.sqrt(np.abs(x)),  # Using abs to avoid negative sqrt
    'tan': np.tan,
    'exp': np.exp
}

#
COLORS = {
    'blue': '#1f77b4',
    'red': '#d62728',
    'green': '#2ca02c',
    'purple': '#9467bd',
    'orange': '#ff7f0e',
    'pink':'#ffa1e5'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        try:
            print("Form data received:", request.form)
            
            x_from = float(request.form['x_from'])
            x_to = float(request.form['x_to'])
            
            selected_functions = request.form.getlist('functions')
            selected_colors = request.form.getlist('colors')
            
            print("Selected functions:", selected_functions)
            print("Selected colors:", selected_colors)

            # Validate function and color selections
            invalid_functions = [func for func in selected_functions if func not in FUNCTIONS]
            invalid_colors = [color for color in selected_colors if color not in COLORS]

            if invalid_functions:
                return render_template('plotter.html',
                                       error=f"Invalid functions selected: {', '.join(invalid_functions)}",
                                       functions=list(FUNCTIONS.keys()),
                                       colors=list(COLORS.keys()))

            if invalid_colors:
                return render_template('plotter.html',
                                       error=f"Invalid colors selected: {', '.join(invalid_colors)}",
                                       functions=list(FUNCTIONS.keys()),
                                       colors=list(COLORS.keys()))

            if not selected_functions:
                return render_template('plotter.html',
                                       error="Choose at least one function",
                                       functions=list(FUNCTIONS.keys()),
                                       colors=list(COLORS.keys()))

            if len(set(selected_colors)) < len(selected_colors):
                return render_template('plotter.html',
                                       error="Duplicate colors selected. Please use unique colors for each function.",
                                       functions=list(FUNCTIONS.keys()),
                                       colors=list(COLORS.keys()))

            # Set default colors if none are selected
            if not selected_colors:
                selected_colors = ['blue'] * len(selected_functions)

            plot_type = request.form.get('plot_type', 'single')
            plot_filename = f"plot_{uuid.uuid4().hex[:8]}.png"
            plot_path = os.path.join('static/images', plot_filename)
            
            try:
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
            except Exception as e:
                print("Error creating plot:", str(e))
                return render_template('plotter.html',
                                       error=f"Error creating plot: {str(e)}",
                                       functions=list(FUNCTIONS.keys()),
                                       colors=list(COLORS.keys()))

        except ValueError as e:
            print("Value Error:", str(e))
            return render_template('plotter.html',
                                   error=str(e),
                                   functions=list(FUNCTIONS.keys()),
                                   colors=list(COLORS.keys()))
        except Exception as e:
            print("Unexpected error:", str(e))
            return render_template('plotter.html',
                                   error=f"An unexpected error occurred: {str(e)}",
                                   functions=list(FUNCTIONS.keys()),
                                   colors=list(COLORS.keys()))

    return render_template('plotter.html',
                           functions=list(FUNCTIONS.keys()),
                           colors=list(COLORS.keys()))

def create_single_plot(x_from, x_to, selected_functions, selected_colors, plot_path):
    plt.switch_backend('Agg') 
    x = np.linspace(x_from, x_to, 500)
    
    try:
        fig = plt.figure(figsize=(10, 6))
        for i, func_name in enumerate(selected_functions):
            color = COLORS.get(selected_colors[i], 'black') if i < len(selected_colors) else 'black'
            y = FUNCTIONS[func_name](x)
            plt.plot(x, y, color=color, label=func_name)
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Combined Plot of Selected Functions')
        plt.grid(True)
        plt.legend()
        plt.savefig(plot_path)
    finally:
        plt.close('all')  

def create_multiple_plots(x_from, x_to, selected_functions, selected_colors):
    plt.switch_backend('Agg') 
    plot_files = []
    x = np.linspace(x_from, x_to, 500)
    
    try:
        for i, func_name in enumerate(selected_functions):
            plot_filename = f"plot_{uuid.uuid4().hex[:8]}.png"
            plot_path = os.path.join('static/images', plot_filename)
            
            fig = plt.figure(figsize=(8, 5))
            color = COLORS.get(selected_colors[i], 'black') if i < len(selected_colors) else 'black'
            y = FUNCTIONS[func_name](x)
            plt.plot(x, y, color=color, label=func_name)
            
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title(f'Plot of {func_name}')
            plt.grid(True)
            plt.legend()
            plt.savefig(plot_path)
            plt.close(fig) 
            
            plot_files.append(plot_filename)
    finally:
        plt.close('all') 
    
    return plot_files

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)