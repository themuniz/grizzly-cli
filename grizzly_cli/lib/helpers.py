#!/usr/bin/env python3
# lib/helpers.py
# helper functions for processing CF course extract
# José Muñiz, School of Professional Studies, CUNY
# 2022-04-24

import json
import pandas as pd
from .console import console

with open("config.json") as file:
    try:
        config = json.load(file)
    except FileNotFoundError as e:
        console.log("No configuration file found.")


def ao_transform(acad_org: str) -> str:
    """For programs that need to be mapped to another program, return the new program, otherwise keep the program as is"""
    if acad_org in list(config["data"]["acad_org_transforms"].keys()):
        return config["data"]["acad_org_transforms"][acad_org]
    else:
        return acad_org


def extract_bb_course_id(bb_course_id: str) -> str:
    """Return the plain course ID from the provided URL. N.B.: these URLs don't seem to actually work, but the IDs are correct"""
    return bb_course_id.split("_")[2]


def combine_instructors_and_dedupe(source: pd.DataFrame) -> pd.DataFrame | None:
    """Return a DF where and the dupe course records have their instructors combined, and the subsequent records removed"""

    # Run through the courses collecting instructors by class#
    instructor_dict = {}

    def collect_instruct_names(row):
        if instructor_dict.get(row["Class#"]) is not None:
            instructor_dict[
                row["Class#"]
            ] = f"{instructor_dict[row['Class#']]}/{row['Name']}"
            return
        else:
            instructor_dict[row["Class#"]] = row["Name"]
            return

    source.apply(collect_instruct_names, axis=1)
    console.print("Collected instructor names")

    # Use instructor_dict to update the instructor courses
    def update_instructor_names(row) -> str:
        return instructor_dict[row["Class#"]]

    combined_names = source.copy()
    combined_names["Name"] = source.apply(update_instructor_names, axis=1)
    console.print("Updated instructor names for courses with multiple instructors")

    # Dedupe the course records
    deduped = combined_names.drop_duplicates(subset="Class#")
    console.print("Removed duplicate course records")
    return deduped
