from __future__ import annotations
import sys
import argparse
from pathlib import Path

import pandas as pd
from torchvision.datasets.utils import download_url
from tqdm import tqdm

def cprint(color, text, **kwargs):
    if color[0] == '*':
        pre_code = '1;'
        color = color[1:]
    else:
        pre_code = ''
    code = {
        'a': '30',
        'r': '31',
        'g': '32',
        'y': '33',
        'b': '34',
        'p': '35',
        'c': '36',
        'w': '37'
    }
    print("\x1b[%s%sm%s\x1b[0m" % (pre_code, code[color], text), **kwargs)
    sys.stdout.flush()


def parse_metadata(pde_names):
    """
    This function parses the argument to filter the metadata of files that need to be downloaded.

    Args:
    pde_names: List containing the name of the PDE to be downloaded
    df      : The provided dataframe loaded from the csv file

    Options for pde_names:
    - Advection
    - Burgers
    - 1D_CFD
    - Diff-Sorp
    - 1D_ReacDiff
    - 2D_CFD
    - Darcy
    - 2D_ReacDiff
    - NS_Incom
    - SWE
    - 3D_CFD

    Returns:
    pde_df : Filtered dataframe containing metadata of files to be downloaded
    """

    meta_df = pd.read_csv("pdebench_data_urls.csv")

    # Ensure the pde_name is defined
    pde_list = [
        "advection",
        "burgers",
        "1d_cfd",
        "diff_sorp",
        "1d_reacdiff",
        "2d_cfd",
        "darcy",
        "2d_reacdiff",
        "ns_incom",
        "swe",
        "3d_cfd",
    ]

    assert all(name.lower() in pde_list for name in pde_names), "PDE name not defined."

    # Filter the files to be downloaded
    meta_df["PDE"] = meta_df["PDE"].str.lower()

    return meta_df[meta_df["PDE"].isin(pde_names)]


def download_data(root_folder, pde_name):
    """ "
    Download data splits specific to a given PDE.

    Args:
    root_folder: The root folder where the data will be downloaded
    pde_name   : The name of the PDE for which the data to be downloaded
    """

    # print(f"Downloading data for {pde_name} ...")

    # Load and parse metadata csv file
    pde_df = parse_metadata(pde_name)

    # Iterate filtered dataframe and download the files
    for _, row in tqdm(pde_df.iterrows(), total=pde_df.shape[0]):
        try:
            file_path = Path(root_folder) / row["Path"]
            download_url(row["URL"], file_path, row["Filename"], md5=row["MD5"])
        except:
            cprint("r", f"******* Skip error occured at {row["Filename"]} *******")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog="Download Script",
        description="Helper script to download the PDEBench datasets",
        epilog="",
    )

    arg_parser.add_argument(
        "--root_folder",
        type=str,
        required=True,
        help="Root folder where the data will be downloaded",
    )
    arg_parser.add_argument(
        "--pde_name",
        action="append",
        help="Name of the PDE dataset to download. You can use this flag multiple times to download multiple datasets",
    )

    args = arg_parser.parse_args()

    download_data(args.root_folder, args.pde_name)
