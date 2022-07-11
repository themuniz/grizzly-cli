#!/usr/bin/env python3
# process_csv.py
# Script to process csv from CF format to DB format
# José Muñiz, School of Professional Studies, CUNY
# 2022-04-23

import os
import pandas as pd
from .helpers import ao_transform, extract_bb_course_id, combine_instructors_and_dedupe
from .console import console


def read_into_df(config: dict) -> pd.DataFrame:
    """Read source csv into dataframe, removing unneeded columns"""
    source = pd.read_csv(
        config["output_filename"],
        infer_datetime_format=True,
        parse_dates=["Start Date", "End Date"],
    )
    console.print("Successfully opened raw data for processing & cleaning")

    # Grab the columns we care about
    # ------------------------------
    # 'Acad Org', 'Session', 'Term', 'Class Stat', 'Subject', 'Catalog#',
    # 'Section', 'Class Title', 'Class#', 'Name', 'Start Date', 'End Date',
    # 'Blackboard Course ID'
    subset = source[config["data"]["columns"]]

    # - Remove acad_orgs we don't care about
    ao_removed = subset[~subset["Acad Org"].isin(config["data"]["acad_orgs_to_remove"])]
    console.print(
        f"Removed records from acad orgs: {config['data']['acad_orgs_to_remove']}"
    )

    # - Adjust acad_orgs that need remapping
    ao_transformed = ao_removed.copy()
    ao_transformed["Acad Org"] = ao_removed["Acad Org"].transform(ao_transform)
    console.print(f"Remapped programs: {config['data']['acad_org_transforms']}")
    console.print(
        f"Number of unique programs: {len(ao_transformed['Acad Org'].unique())}"
    )

    # - Extract BB course ID
    ao_transformed["Blackboard Course ID"] = ao_removed[
        "Blackboard Course ID"
    ].transform(extract_bb_course_id)
    console.print("Extracted BB course IDs from URLs")

    # - Combine instructor names in duped records, remove duped records
    # courses with multiple instructors show up as duplicate records.
    deduped = combine_instructors_and_dedupe(ao_transformed)

    # - Rewrite column names
    deduped.columns = [
        "acad_org",
        "session",
        "cf_term_id",
        "cf_status",
        "course_subject",
        "course_number",
        "section_number",
        "course_title",
        "cf_course_id",
        "instructor_name",
        "start_date",
        "end_date",
        "bb_course_id",
    ]
    deduped.to_csv(
        os.path.join(config["output_directory"], config["processed_filename"]),
        index=False,
    )
    console.print(f"Saved processed file as: {config['processed_filename']}")
    return deduped
