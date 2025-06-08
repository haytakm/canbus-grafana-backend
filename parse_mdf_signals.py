import argparse
import mdf_iter

RAW_COLUMNS = {
    'TimeStamp', 'BusChannel', 'ID', 'IDE', 'DataLength', 'DataBytes'
}

def list_signals(path, fs=None):
    """Return signal names present in an MDF file without using a DBC."""
    if fs is None:
        fh = open(path, 'rb')
    else:
        fh = fs.open(path, 'rb')
    with fh:
        mdf = mdf_iter.MdfFile(fh)
        df = mdf.get_data_frame()

    columns = [c for c in df.columns if c not in RAW_COLUMNS]

    if columns:
        return columns

    if 'ID' in df.columns:
        ids = sorted(set(hex(x) for x in df['ID'].unique()))
        return ids
    return []


def main():
    parser = argparse.ArgumentParser(description="List signals from an MDF file")
    parser.add_argument('mdf', help='Path to MDF file')
    args = parser.parse_args()

    signals = list_signals(args.mdf)
    if not signals:
        print('No signals found')
    else:
        for sig in signals:
            print(sig)


if __name__ == '__main__':
    main()
