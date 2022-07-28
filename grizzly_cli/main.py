#!/usr/bin/env python3
"""grizzly-cli.py

CLI to the Grizzly API
José Muñiz, School of Professional Studies, CUNY
"""

import json
import os

import polars as pl
import requests
import click
from rich.table import Table
from xlsx2csv import Xlsx2csv

from .lib.console import console
from .lib.process_csv import read_into_df


APP_NAME = "Grizzly"

def read_config():
    cfg = os.path.join(click.get_app_dir(APP_NAME), 'config.toml')
    return cfg

with open("config.json") as file:
    config = json.load(file)


@click.command()
@click.option("-v", "--verify-ssl", is_flag=True, default=config["verify_ssl"])
@click.option("-d", "--dry-run", is_flag=True, default=False)
def run(verify_ssl: bool, dry_run: bool):
    """
    Process CUNYfirst course data and import into OFDIT database.

    Options:

        --verify-ssl: require verification of SSL certificate on API

        --dry-run: process extract but do not POST to API
    """
    r = requests.get(f'{config["api_url"]}/d/users', verify=verify_ssl)
    console.print_json(data=r.json(), ensure_ascii=False)
    # cycles = get_cycles()
    # data_directory = setup(term, year)
    # data_file = locate_datafile(data_directory)
    # convert_to_csv(data_file)
    # processed = read_into_df(config)
    # print_stats(processed)
    if not dry_run:
        # post_sections()
        console.print("Done & done. ✅")


def setup(term, year) -> str:
    """Returns the name of the data directory"""
    data_directory = f"{config['data_directory']}/{term} {year}"
    if os.path.isdir(data_directory):
        console.print(f"Found the data directory at: {data_directory}")
    else:
        raise Exception(f"Could not access the data directory at {data_directory}")
    return data_directory


def locate_datafile(data_directory) -> str:
    """Returns the name of the most current data file"""
    datafiles = [
        os.path.join(data_directory, x)
        for x in os.listdir(data_directory)
        if x.endswith(".xlsx")
    ]
    current_data_file = max(datafiles, key=os.path.getctime)
    console.print(f"Current datafile: {current_data_file}")
    return current_data_file


def convert_to_csv(excel_file):
    """Converts data file format to csv"""
    Xlsx2csv(excel_file, outputencoding="utf-8").convert(config["output_filename"])
    console.print(f"Converted xlsx file to {config['output_filename']}")
    return


def print_stats(df):
    """Print summary stats for eyeball checks"""
    table = Table(title="Summary count")

    table.add_column("Academic Org", justify="right", style="cyan", no_wrap=True)
    table.add_column("Session", style="magenta")
    table.add_column("Course count", justify="right", style="green")
    groups = df.groupby(["acad_org", "session"])
    for group_key, group_value in groups:
        table.add_row(f"{group_key[0]}", f"{group_key[1]}", f"{len(group_value)}")

    console.print(table)
    console.print(f"Record count: {len(df.index)}")


if __name__ == "__main__":
    run()
