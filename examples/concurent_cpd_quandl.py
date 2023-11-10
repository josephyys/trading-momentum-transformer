import multiprocessing
import argparse
import os

from settings.default import (
    QUANDL_TICKERS,
    CPD_QUANDL_OUTPUT_FOLDER,
    CPD_DEFAULT_LBW,
)

# Set this to the number of tickers you want to process
N_FIRST_TICKERS = 1  # For example, process the first 5 tickers only
N_WORKERS = N_FIRST_TICKERS  # Adjust the number of workers accordingly

def main(lookback_window_length: int):
    if not os.path.exists(CPD_QUANDL_OUTPUT_FOLDER(lookback_window_length)):
        os.mkdir(CPD_QUANDL_OUTPUT_FOLDER(lookback_window_length))

    # Adjust all_processes to only include the first N_FIRST_TICKERS
    all_processes = [
        f'python -m examples.cpd_quandl "{ticker}" "{os.path.join(CPD_QUANDL_OUTPUT_FOLDER(lookback_window_length), ticker + ".csv")}" "1990-01-01" "2021-12-31" "{lookback_window_length}"'
        for ticker in QUANDL_TICKERS[:N_FIRST_TICKERS]  # Slicing the ticker list
    ]
    process_pool = multiprocessing.Pool(processes=N_WORKERS)
    process_pool.map(os.system, all_processes)

if __name__ == "__main__":

    def get_args():
        """Returns settings from command line."""

        parser = argparse.ArgumentParser(
            description="Run changepoint detection module for all tickers"
        )
        parser.add_argument(
            "lookback_window_length",
            metavar="l",
            type=int,
            nargs="?",
            default=CPD_DEFAULT_LBW,
            help="CPD lookback window length",
        )
        return [
            parser.parse_known_args()[0].lookback_window_length,
        ]

    main(*get_args())
