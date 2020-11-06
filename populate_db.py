import argparse
from peering_functions import build_IX_table, build_peers_table

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="PeeringDB Info Application.")
    parser.add_argument("--build_ix_table", nargs='+', type=str, help="Build exchange database table, takes AS number as argument")
    parser.add_argument("--build_peers_table", nargs='+', type=str, help="Build peers database table, takes AS number as argument")
    args = parser.parse_args()
    if args.build_ix_table:
        if len(args.build_ix_table) != 1:
            print("ERROR: Takes exactly one argument.")
        else:
            build_IX_table(args.build_ix_table[0])
    if args.build_peers_table:
        if len(args.build_peers_table) != 1:
            print("ERROR: Takes exactly one argument.")
        else:
            build_peers_table(asn=args.build_peers_table[0])
