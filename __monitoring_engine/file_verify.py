import sys
import csv


def verify_file(filename, tolerance=3):
    in_f = open(filename, "r", encoding="utf-8")
    in_csv = csv.reader(in_f)

    HEADERS = next(in_csv)

    timestamp_idx = HEADERS.index("timestamp")
    datetime_idx = HEADERS.index("datetime")
    elapsedTime_idx = HEADERS.index("elapsedTime")

    start_timestamp = -1

    for row in in_csv:
        timestamp_val = row[timestamp_idx]
        datetime_val = row[datetime_idx]
        elapsedTime_val = row[elapsedTime_idx]

        if start_timestamp == -1:
            if elapsedTime_val in ("-0:00", "0:00", "0:01", "0:02", "0:03"):
                start_timestamp = timestamp_val


    return start_timestamp


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(verify_file(sys.argv[1]))
    elif len(sys.argv) == 1:
        print(verify_file("chat_archive/Fauna/only_up_i_wont_let_this_game_win.y952Zpm290s.csv"))
        