import sys
import os

# Add the project root to sys.path to allow importing params.cells
# This assumes the script is in neurogenesis/scripts/helpers/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from params.cells import cell_params
from brian2 import nS, mV, ms, pA, pF # For unit conversions

def format_value(value, unit, precision=3):
    """Formats a Brian2 Quantity or a number to a string with specified precision,
       trimming unnecessary trailing zeros and decimal points."""
    if isinstance(value, (float, int)):
        numeric_value = value
    else:
        # Brian2 quantity, convert to float
        try:
            numeric_value = float(value / unit)
        except Exception as e:
            print(f"Error converting value {value} with unit {unit}: {e}", file=sys.stderr)
            return "Error"
            
    # Check if the number is effectively an integer (within a small tolerance for float inaccuracies)
    if abs(numeric_value - round(numeric_value)) < 1e-9: # Check if it's very close to an integer
        return str(int(round(numeric_value)))
    else:
        # Format to the specified precision
        formatted_str = f"{numeric_value:.{precision}f}"
        # Remove trailing zeros
        formatted_str = formatted_str.rstrip('0')
        # Remove trailing decimal point if it exists (e.g., after rstrip('0'), "123." might remain)
        if formatted_str.endswith('.'):
             formatted_str = formatted_str.rstrip('.')
        return formatted_str

def main():
    neuron_type_mapping = {
        "Granular madura": "mgc",
        "Granular imatura": "igc",
        "Musgosa": "mc",
        "HIPP": "hipp",
        "Em cesto": "bc",
        "Piramidal do CA3": "pca3",
        "Inibitória do CA3": "ica3",
    }

    # Parameters: (key_in_cells_py, LaTeX_header_name, unit_string_for_header, brian2_unit_for_conversion)
    parameters_info = [
        ('k', 'k', '(nS/mV)', nS/mV),
        ('a', 'a', '(ms$^{-1}$)', ms**-1),
        ('b', 'b', '(nS)', nS),
        ('d', 'd', '(pA)', pA),
        ('Cm', 'C$_m$', '(pF)', pF),
        ('Vr', 'V$_r$', '(mV)', mV),
        ('Vt', 'V$_t$', '(mV)', mV),
        ('Vmin', 'V$_{min}$', '(mV)', mV),
        ('Vpeak', 'V$_{peak}$', '(mV)', mV),
    ]

    header_latex_names = [info[1] for info in parameters_info]
    header_units = [info[2] for info in parameters_info]
    param_keys_in_cells = [info[0] for info in parameters_info]
    param_brian2_units = [info[3] for info in parameters_info]

    table_rows_data = []
    for neuron_display_name, cell_data_key in neuron_type_mapping.items():
        if cell_data_key in cell_params:
            source_cell_data = cell_params[cell_data_key]
            # Ensure it's an Izhikevich model, which should have these parameters
            if source_cell_data.get("model") == "izhikevich":
                current_row_values = [neuron_display_name]
                for p_key, b_unit in zip(param_keys_in_cells, param_brian2_units):
                    if p_key in source_cell_data:
                        raw_value = source_cell_data[p_key]
                        current_row_values.append(format_value(raw_value, b_unit, precision=3))
                    else:
                        current_row_values.append("-") # Placeholder if param is unexpectedly missing
                table_rows_data.append(current_row_values)
            else:
                print(f"Skipping '{neuron_display_name}' (mapped to '{cell_data_key}'): Not an Izhikevich model or missing 'model' key.", file=sys.stderr)
                placeholder_row = [neuron_display_name] + ["-"] * len(param_keys_in_cells)
                table_rows_data.append(placeholder_row)
        else:
            print(f"Warning: Cell key '{cell_data_key}' (for '{neuron_display_name}') not found in cell_params.", file=sys.stderr)
            placeholder_row = [neuron_display_name] + ["-"] * len(param_keys_in_cells)
            table_rows_data.append(placeholder_row)

    # Print LaTeX table
    print("\\begin{table}[h!]")
    print("\\centering")
    print("\\renewcommand{\\arraystretch}{1.4}")
    # 'l' for neuron name column, 'c' for each parameter column
    print(f"\\begin{{tabular}}{{l{'c' * len(parameters_info)}}}")
    print("\\toprule")

    # Parameter names row (LaTeX formatted)
    print("\\textbf{Célula} & " + " & ".join([f"\\textbf{{{name}}}" for name in header_latex_names]) + " \\\\")
    # Parameter units row
    print(" & " + " & ".join(header_units) + " \\\\")
    print("\\midrule")

    # Data rows
    for row_data_list in table_rows_data:
        print(" & ".join(map(str, row_data_list)) + " \\\\")

    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\caption{Parâmetros do modelo Izhikevich por tipo de neurônio.}") # Added a generic caption
    print("\\label{tab:izhikevich_neuron_params}") # Added a generic label
    print("\\end{table}")

if __name__ == "__main__":
    main()
