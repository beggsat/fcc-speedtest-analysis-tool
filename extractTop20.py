import argparse
import pandas as pd


def get_filepaths():
    """Collect Excel file paths from the terminal."""

    parser = argparse.ArgumentParser(description="Plot excel files")
    parser.add_argument(
        "filepath",
        type=str,
        nargs="+",
        help="provide the full path of your excel files",
    )
    parser.add_argument(
        "--sheet",
        type=int,
        nargs="?",
        default=1,
        help="optional provide the sheet number, defaults to first sheet",
    )
    parser.add_argument(
        "-output",
        type=str,
        nargs=1,
        help="output file name, required",
    )
    args = parser.parse_args()
    return args


def get_stats(data):
    gb = data.groupby(["grid_id"])
    counts = gb.size().to_frame(name="counts")
    # testing = (gb.agg({'DL Mbps': 'mean'}).rename(columns={'DL Mbps': 'dl_mean'}))
    stats = pd.concat(
        [
            counts,
            (gb.agg({"DL Mbps": "mean"}).rename(columns={"DL Mbps": "dl_mean"})),
            (gb.agg({"DL Mbps": "median"}).rename(columns={"DL Mbps": "dl_median"})),
            (gb.agg({"DL Mbps": "max"}).rename(columns={"DL Mbps": "dl_max"})),
            (gb.agg({"DL Mbps": "min"}).rename(columns={"DL Mbps": "dl_min"})),
            (gb.agg({"UL Mbps": "mean"}).rename(columns={"UL Mbps": "ul_mean"})),
            (gb.agg({"UL Mbps": "median"}).rename(columns={"UL Mbps": "ul_median"})),
            (gb.agg({"UL Mbps": "max"}).rename(columns={"UL Mbps": "ul_max"})),
            (gb.agg({"UL Mbps": "min"}).rename(columns={"UL Mbps": "ul_min"})),
        ],
        axis=1,
    ).reset_index()

    grids = data.loc[(stats['grid_id']), 'provider_n']
    stats['location'] = grids

    print(stats.to_string() + "\n")


def extract_values(args):
    """Load and extract top 20 of the Excel files. Also prints out some stats for helping with analysis"""

    # load the Excel files that we got from the provided arguments
    for path in args.filepath:
        outputnum = 0
        print("File entered:")
        print(path)
        print("Sheet #: " + str(args.sheet))

        all_tests = pd.read_excel(path, sheet_name=args.sheet - 1)
        top20 = (
            all_tests.sort_values(["grid_id", "DL Mbps"], ascending=(True, False))
            .groupby("grid_id", sort=False)
            .head(20)
        )

        print("Statistics for all tests:")
        get_stats(all_tests)
        print("Statistics for top 20 tests:")
        get_stats(top20)

        if outputnum == 0:
            print("output to file: " + args.output[0] + ".csv")
            top20.to_csv(args.output[0] + ".csv", index=False)
        else:
            print("output to file: " + args.output[0] + "_" + str(outputnum) + ".csv")
            top20.to_csv(args.output[0] + "_" + str(outputnum) + ".csv", index=False)
        outputnum += outputnum


if __name__ == "__main__":
    filepaths = get_filepaths()
    extract_values(filepaths)
