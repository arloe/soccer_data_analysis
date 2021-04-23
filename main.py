import argparse
import os
from python import data_collection


def main( driver_dir, outpath, file ):
    # crawling
    player, position = data_collection.basic_info( driver_dir = driver_dir )
    df = data_collection.get_stat(  driver_dir = driver_dir
                                  , player_name_list = player
                                  , position_list = position
                                  )
    # to csv
    output_file = os.path.join( outpath, file )
    df.to_csv( output_file, index = False )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Crawling")

    parser.add_argument(  "-d", "--driver_dir", default = None, type = str
                        , help = "path of chrome driver")
    parser.add_argument(  "-o", "--output", default = None, type = str
                        , help = "path of output file")
    parser.add_argument( "-f", "--file", default = None, type = str
                        , help = "file name of output")
    args = parser.parse_args()
    
    outpath = os.path.join("./data", "" if args.outpath is None else args.outpath)
    
    main(args.driver_dir, outpath, args.file)
