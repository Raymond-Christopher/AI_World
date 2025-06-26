"""CSV parsing utilities for loading virtual country resource states and
resource weights.

This module provides helper functions to read CSV files that define:
1. Each country's resource quantities.
2. Resource weights used in computing state quality.
"""

import csv


def parse_country_resources(filepath):
    """Parses a CSV file of countries and their resource quantities.

    The file is expected to have a 'Country' column followed by resource
    columns, where each row contains the resource counts for a specific
    country.

    :param filepath: The path to the CSV file containing country
        resource data.
    :type filepath: str
    :return: A dictionary mapping country names to resource
        dictionaries.
    :rtype: dict
    """
    countries = {}
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country = row["Country"]
            resources = {k: int(v) for k, v in row.items() if k != "Country"}
            countries[country] = resources
    return countries


def parse_resource_weights(filepath):
    """Parses a CSV file of resource weights used in state quality evaluation.

    The file is expected to have two columns: 'Resource' and 'Weight'.

    :param filepath: The path to the CSV file containing resource weights.
    :type filepath: str
    :return: A dictionary mapping resource names to their corresponding weights.
    :rtype: dict
    """
    weights = {}
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            weights[row["Resource"]] = float(row["Weight"])
    return weights
