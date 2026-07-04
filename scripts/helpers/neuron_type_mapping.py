neuron_type_mapping = {
    "pp": "Entorhinal cortex",
    "mgc": "Mature granule",
    "igc": "Immature granule",
    "mc": "Mossy",
    "hipp": "HIPP",
    "bc": "Basket",
    "pca3": "CA3 Pyramidal",
    "ica3": "CA3 Inhibitory",
}

neuron_type_abbreviation = {
    "pp": "EC",
    "mgc": "mGC",
    "igc": "iGC",
    "mc": "MC",
    "hipp": "HIPP",
    "bc": "BC",
    "pca3": "pCA3",
    "ica3": "iCA3",
}


def display_label(key, use_abbreviation=True):
    table = neuron_type_abbreviation if use_abbreviation else neuron_type_mapping
    return table.get(key, key)
