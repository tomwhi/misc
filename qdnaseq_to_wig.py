import pandas as pd
import begin
import logging

@begin.start(auto_convert=True)
def generate_wigs(qdnaseq_filename, copynumber_wig_filename, readcount_wig_filename):
    logging.basicConfig(level=logging.DEBUG)

    df = pd.read_table(qdnaseq_filename)
    df_nonnull = df.loc[~(df["segmented"].isnull()),:]

    curr_chrom = None
    curr_pos = -1
    idx = 0
    with open(copynumber_wig_filename, 'w') as copynumber_wigfile, open(readcount_wig_filename, 'w') as readcount_wigfile:
        for index, row in df_nonnull.iterrows():
            if row["chromosome"] != curr_chrom or row["start"] != curr_pos + 15000:
                idx += 1
                curr_chrom = row["chromosome"]
                print("fixedStep chrom=" + str(curr_chrom) + " start=" + str(row["start"]) + " step=15000 span=15000", file=copynumber_wigfile)
                print("fixedStep chrom=" + str(curr_chrom) + " start=" + str(row["start"]) + " step=15000 span=15000", file=readcount_wigfile)
            print("%f" % (row["copynumber"]), file=copynumber_wigfile)
            print("%d" % (row["readcount"]), file=readcount_wigfile)
            curr_pos = row["start"]
