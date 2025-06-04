import csv
from os.path import join
from params import base_dir

def parse_hippocampome_params(csv_filepath):
    """
    Parses a CSV file with synaptic parameters from Hippocampome.org and
    returns a string representation of a Python dictionary.

    Args:
        csv_filepath (str): The path to the CSV file.

    Returns:
        str: A string representing the Python dictionary of synaptic parameters.
    """
    neuron_type_mapping = {
        "DG Granule": "mgc",
        "DG Mossy": "mc",
        "DG HIPP": "hipp",
        "DG Basket": "bc",
        "CA3 Pyramidal": "pca3",
        "CA3 Basket": "ica3",
        "MEC LII Stellate": "pp",
    }

    order = ['pp', 'mgc', 'mc', 'hipp', 'bc', 'pca3', 'ica3']
    syn_type_mapping = {
        'pp'   : 'exc',
        'mgc'  : 'exc',
        'mc'   : 'exc',
        'hipp' : 'inh',
        'bc'   : 'inh',
        'pca3' : 'exc',
        'ica3' : 'inh',
    }

    output_dict_str = "syn_params = {\n"
    parsed_connections = []
    post_syn_var_counters = {} # Initialize counter for syn_var

    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    pre_neuron_full = row["Presynaptic Neuron Type"]
                    post_neuron_full = row["Postsynaptic Neuron Type"]

                    # Skip if neuron type is not in our mapping (e.g. from a different region if the CSV is mixed)
                    if pre_neuron_full not in neuron_type_mapping or post_neuron_full not in neuron_type_mapping:
                        # Fallback: if the exact name is not found, try matching parts for broader compatibility
                        pre_key_part = next((k for k in neuron_type_mapping if k.split(" ")[-1] == pre_neuron_full.split(" ")[-1]), None)
                        post_key_part = next((k for k in neuron_type_mapping if k.split(" ")[-1] == post_neuron_full.split(" ")[-1]), None)

                        if pre_key_part and post_key_part:
                            pre_neuron = neuron_type_mapping[pre_key_part]
                            post_neuron = neuron_type_mapping[post_key_part]
                        elif pre_neuron_full in neuron_type_mapping: # one is mapped, the other is not fully qualified
                             pre_neuron = neuron_type_mapping[pre_neuron_full]
                             # try to find a partial match for post_neuron if pre_neuron was found
                             post_key_partial_match = next((k for k in neuron_type_mapping if k.endswith(post_neuron_full)), None)
                             if post_key_partial_match:
                                 post_neuron = neuron_type_mapping[post_key_partial_match]
                             else:
                                print(f"Skipping row due to unmapped postsynaptic neuron type: {post_neuron_full} (Presynaptic: {pre_neuron_full})")
                                continue
                        elif post_neuron_full in neuron_type_mapping: # one is mapped, the other is not fully qualified
                            post_neuron = neuron_type_mapping[post_neuron_full]
                            # try to find a partial match for pre_neuron if post_neuron was found
                            pre_key_partial_match = next((k for k in neuron_type_mapping if k.endswith(pre_neuron_full)), None)
                            if pre_key_partial_match:
                                pre_neuron = neuron_type_mapping[pre_key_partial_match]
                            else:
                                print(f"Skipping row due to unmapped presynaptic neuron type: {pre_neuron_full} (Postsynaptic: {post_neuron_full})")
                                continue
                        else:
                            print(f"Skipping row due to unmapped neuron types: {pre_neuron_full} -> {post_neuron_full}")
                            continue
                    else:
                        pre_neuron = neuron_type_mapping[pre_neuron_full]
                        post_neuron = neuron_type_mapping[post_neuron_full]

                    # Increment syn_var for the current post_neuron
                    current_syn_var = post_syn_var_counters.get(post_neuron, 0) + 1
                    post_syn_var_counters[post_neuron] = current_syn_var

                    key_name = f"{pre_neuron}_{post_neuron}"
                    syn_type_val = syn_type_mapping[pre_neuron]

                    # Parameter extraction - ensure correct types and units
                    # Using get with default to handle potentially missing columns gracefully, though schema implies they exist
                    g = float(row.get("g", 0))
                    tau_d = float(row.get("tau_d", 0))
                    tau_r = float(row.get("tau_r", 0))
                    tau_f = float(row.get("tau_f", 0))
                    u_val = float(row.get("u", 0))
                    prob = float(row.get("Connection Probability", 0))
                    delay = float(row.get("Synaptic Delay", 0))

                    connection_details_str = '{\n'
                    connection_details_str += f'        "syn_type" : "{syn_type_val}",\n'
                    connection_details_str += f'        "syn_var"  : {current_syn_var},\n'
                    connection_details_str += f'        "p"        : {prob:.4f},\n'
                    connection_details_str += f'        "g"        : {g:.4f} * nS,\n'
                    connection_details_str += f'        "tau_r"    : {tau_r:.4f} * ms,\n'
                    connection_details_str += f'        "tau_d"    : {tau_d:.4f} * ms,\n'
                    connection_details_str += f'        "tau_f"    : {tau_f:.4f} * ms,\n'
                    connection_details_str += f'        "U_se"     : {u_val:.4f},\n'
                    connection_details_str += f'        "delay"    : {delay:.1f} * ms\n'
                    connection_details_str += "    }"

                    parsed_connections.append({
                        'pre_neuron': pre_neuron,
                        'post_neuron': post_neuron,
                        'key_name': key_name,
                        'details_str': connection_details_str
                    })

                except KeyError as e:
                    print(f"Skipping row due to missing column: {e} in row: {row}")
                except ValueError as e:
                    print(f"Skipping row due to invalid data type: {e} in row: {row}")
                except Exception as e:
                    print(f"An unexpected error occurred while processing row: {row}. Error: {e}")


    except FileNotFoundError:
        return f"Error: The file {csv_filepath} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

    # Sort connections based on the 'order' list
    parsed_connections.sort(key=lambda x: (order.index(x['pre_neuron']), order.index(x['post_neuron'])))

    # Build the output string from sorted connections
    entry_strings = []
    for item in parsed_connections:
        entry_strings.append(f'    "{item["key_name"]}": {item["details_str"]}')

    output_dict_str = "syn_params = {\n"
    output_dict_str += ",\n".join(entry_strings)
    if entry_strings:
        output_dict_str += "\n"
    output_dict_str += "}"
    return output_dict_str

if __name__ == "__main__":
    # csv_file = join(base_dir, 'params', 'hippocampome', 'DG_CA3_EC_conn_parameters.csv')
    csv_file = join(base_dir, 'params', 'hippocampome', 'DG_CA3_EC_conn_parameters06-04-2025_12_04_30.csv')

    class Unit:
        def __init__(self, name):
            self.name = name
        def __rmul__(self, other):
            return f"{other}{self.name}"
        def __str__(self):
            return self.name

    nS = Unit("nS")
    ms = Unit("ms")

    parsed_params_str = parse_hippocampome_params(csv_file)
    print(parsed_params_str)
