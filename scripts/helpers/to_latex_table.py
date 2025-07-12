import sys
import os

from params.cells import cell_params
from params.synapses import syn_params
from params.general import latex_dir
from brian2 import nS, mV, ms, pA, pF
from os.path import join

neuron_type_mapping = {
    "Córtex Entorrinal": "pp",
    "Granular madura": "mgc",
    "Granular imatura": "igc",
    "Musgosa": "mc",
    "HIPP": "hipp",
    "Em cesto": "bc",
    "Piramidal do CA3": "pca3",
    "Inibitória do CA3": "ica3",
}

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

def generate_synapse_table():
    neuron_name_map = {
        "pp": "Córtex Entorrinal",
        "mgc": "Granular madura",
        "igc": "Granular imatura",
        "mc": "Musgosa",
        "hipp": "HIPP",
        "bc": "Em cesto",
        "pca3": "Piramidal do CA3",
        "ica3": "Inibitória do CA3",
    }

    neurons_with_images = set(neuron_type_mapping.values())

    # Parameters: (key_in_synapses_py, LaTeX_header_name, unit_string_for_header, brian2_unit_for_conversion)
    parameters_info = [
        ('g', '$g$', '(nS)', nS),
        ('tau_d', '$\\tau_d$', '(ms)', ms),
        ('tau_r', '$\\tau_r$', '(ms)', ms),
        ('tau_f', '$\\tau_f$', '(ms)', ms),
        ('U_se', '$U$', '', 1),
    ]

    header_latex_names = [info[1] for info in parameters_info]
    param_keys = [info[0] for info in parameters_info]
    param_brian2_units = [info[3] for info in parameters_info]

    table_rows_data = []
    for synapse_key, params in syn_params.items():
        pre_name, post_name = synapse_key.split('_')
        
        pre_display_name = neuron_name_map.get(pre_name, pre_name)
        if pre_name in neurons_with_images:
            image_tex = f"$\\vcenter{{\\hbox{{\\includegraphics[height=1.5em]{{figuras/neurônios/{pre_name}.png}}}}}}$"
            pre_display_name = f"{image_tex} {pre_display_name}"

        post_display_name = neuron_name_map.get(post_name, post_name)
        if post_name in neurons_with_images:
            image_tex = f"$\\vcenter{{\\hbox{{\\includegraphics[height=1.5em]{{figuras/neurônios/{post_name}.png}}}}}}$"
            post_display_name = f"{image_tex} {post_display_name}"

        prob = params.get('p', 0) * 100
        prob_val = f"{prob:.0f}" if prob == int(prob) else f"{prob:.1f}"

        conn_type = "Aleatória"
        if 'condition' in params:
            if "==" in params['condition']:
                conn_type = "Lamelar"
            elif "!=" in params['condition'] and "i != j" not in params['condition']:
                conn_type = "Interlamelar"

        current_row_values = [pre_display_name, post_display_name, conn_type, prob_val]

        for p_key, b_unit in zip(param_keys, param_brian2_units):
            if p_key in params:
                raw_value = params[p_key]
                current_row_values.append(format_value(raw_value, b_unit, precision=3))
            else:
                current_row_values.append("-")
        
        table_rows_data.append(current_row_values)

    output_path = join(latex_dir, 'tabelas/sinapses.tex')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        # Print LaTeX table for synapses
        print("% Synapse Parameters Table", file=f)
        print("% Required packages: \\usepackage{amsmath}, \\usepackage{graphicx}, \\usepackage{multirow}", file=f)
        print("\\begin{table}[h!]", file=f)
        print("\\centering", file=f)
        print("\\renewcommand{\\arraystretch}{1.4}", file=f)
        print("\\resizebox{\\textwidth}{!}{%", file=f)
        print(f"\\begin{{tabular}}{{llcc{'c' * len(parameters_info)}}}", file=f)
        print("\\toprule", file=f)

        # Header row
        print("\\multirow{2}{*}{\\textbf{Pré-sináptico}} & \\multirow{2}{*}{\\textbf{Pós-sináptico}} & \\multirow{2}{*}{\\textbf{Conexão}} & $P$ & " +
              " & ".join([f"\\textbf{{{name}}}" for name in header_latex_names]) + " \\\\", file=f)
        print(" & & & (\\%) & " + " & ".join([info[2] for info in parameters_info]) + " \\\\", file=f)
        print("\\midrule", file=f)

        # Data rows
        for row_data_list in table_rows_data:
            print(" & ".join(map(str, row_data_list)) + " \\\\", file=f)

        print("\\bottomrule", file=f)
        print("\\end{tabular}}", file=f)
        # print("\\caption{Parâmetros das sinapses entre as populações neuronais.}", file=f)
        print('''\\caption{Parâmetros das sinapses entre as populações neuronais. Conexões aleatórias ocorrem entre todas as células
              de ambas as populações; conexões lamelares ocorrem entre células da mesma lamela; conexões interlamelares ocorrem
              entre as células de uma lamela com todas as demais. A probabilidade de conexão $P$ diz respeito à porcentagem de
              conexões entre as populações neuronais de acordo com a condição de conexão.}''', file=f)
        print("\\label{tab:synapse_params}", file=f)
        print("\\end{table}", file=f)


def generate_neuron_table():
    # Parameters: (key_in_cells_py, LaTeX_header_name, unit_string_for_header, brian2_unit_for_conversion)
    parameters_info = [
        ('k', '$k$', '(nS/mV)', nS/mV),
        ('a', '$a$', '(ms$^{-1}$)', ms**-1),
        ('b', '$b$', '(nS)', nS),
        ('d', '$d$', '(pA)', pA),
        ('Cm', '$C_m$', '(pF)', pF),
        ('Vr', '$V_r$', '(mV)', mV),
        ('Vt', '$V_t$', '(mV)', mV),
        ('Vmin', '$V_{min}$', '(mV)', mV),
        ('Vpeak', '$V_{peak}$', '(mV)', mV),
    ]

    header_latex_names = [info[1] for info in parameters_info]
    header_units = [info[2] for info in parameters_info]
    param_keys_in_cells = [info[0] for info in parameters_info]
    param_brian2_units = [info[3] for info in parameters_info]

    table_rows_data = []
    for neuron_display_name, cell_data_key in neuron_type_mapping.items():
        image_tex = f"$\\vcenter{{\\hbox{{\\includegraphics[height=1.5em]{{figuras/neurônios/{cell_data_key}.png}}}}}}$"
        cell_name_with_img = f"{image_tex} {neuron_display_name}"

        if cell_data_key in cell_params:
            source_cell_data = cell_params[cell_data_key]
            # Ensure it's an Izhikevich model, which should have these parameters
            if source_cell_data.get("model") == "izhikevich":
                current_row_values = [cell_name_with_img]
                for p_key, b_unit in zip(param_keys_in_cells, param_brian2_units):
                    if p_key in source_cell_data:
                        raw_value = source_cell_data[p_key]
                        current_row_values.append(format_value(raw_value, b_unit, precision=3))
                    else:
                        current_row_values.append("-") # Placeholder if param is unexpectedly missing
                table_rows_data.append(current_row_values)
            else:
                print(f"Skipping '{neuron_display_name}' (mapped to '{cell_data_key}'): Not an Izhikevich model or missing 'model' key.", file=sys.stderr)
                continue
        else:
            print(f"Warning: Cell key '{cell_data_key}' (for '{neuron_display_name}') not found in cell_params.", file=sys.stderr)
            continue

    output_path = join(latex_dir, 'tabelas/izhikevich.tex')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        # Print LaTeX table
        print("% Required packages: \\usepackage{amsmath}, \\usepackage{graphicx}, \\usepackage{multirow}", file=f)
        print("\\begin{table}[h!]", file=f)
        print("\\centering", file=f)
        print("\\renewcommand{\\arraystretch}{1.4}", file=f)
        print("\\resizebox{\\textwidth}{!}{%", file=f)
        # 'l' for neuron name column, 'c' for each parameter column
        print(f"\\begin{{tabular}}{{l{'c' * len(parameters_info)}}}", file=f)
        print("\\toprule", file=f)

        # Parameter names row (LaTeX formatted)
        print("\\multirow{2}{*}{\\textbf{Célula}} & " + " & ".join([f"\\textbf{{{name}}}" for name in header_latex_names]) + " \\\\", file=f)
        # Parameter units row
        print(" & " + " & ".join(header_units) + " \\\\", file=f)
        print("\\midrule", file=f)

        # Data rows
        for row_data_list in table_rows_data:
            print(" & ".join(map(str, row_data_list)) + " \\\\", file=f)

        print("\\bottomrule", file=f)
        print("\\end{tabular}}", file=f)
        print("\\caption{Parâmetros do modelo Izhikevich por tipo de neurônio.}\\label{tab:izhikevich_neuron_params}", file=f)
        print("\\end{table}", file=f)

def generate_neuron_counts_table():
    table_rows_data = []

    for neuron_display_name, cell_data_key in neuron_type_mapping.items():
        if cell_data_key in cell_params:
            count = cell_params[cell_data_key].get('N', '-')
            image_tex = f"$\\vcenter{{\\hbox{{\\includegraphics[height=1.5em]{{figuras/neurônios/{cell_data_key}.png}}}}}}$"
            neuron_name_with_img = f"{image_tex} {neuron_display_name}"
            table_rows_data.append([neuron_name_with_img, str(count)])
        else:
            print(f"Warning: Cell key '{cell_data_key}' (for '{neuron_display_name}') not found in cell_params for counts table.", file=sys.stderr)

    output_path = join(latex_dir, 'tabelas/neuron_counts.tex')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        print("% Neuron Counts Table", file=f)
        print("% Required packages: \\usepackage{amsmath}, \\usepackage{graphicx}", file=f)
        print("\\begin{table}[h!]", file=f)
        print("\\centering", file=f)
        print("\\renewcommand{\\arraystretch}{1.4}", file=f)
        # 'l' for neuron name column, 'c' for count
        print("\\begin{tabular}{lc}", file=f)
        print("\\toprule", file=f)

        # Header row
        print("\\textbf{Célula} & \\textbf{N} \\\\", file=f)
        print("\\midrule", file=f)

        # Data rows
        for row_data in table_rows_data:
            print(" & ".join(row_data) + " \\\\", file=f)

        print("\\bottomrule", file=f)
        print("\\end{tabular}", file=f)
        print("\\caption{Quantidade de neurônios por população (N).}\\label{tab:neuron_counts}", file=f)
        print("\\end{table}", file=f)


if __name__ == "__main__":
    generate_neuron_table()
    generate_synapse_table()
    generate_neuron_counts_table()
    print('feito')
