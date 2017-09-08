import pandas as pd
import begin

@begin.start(auto_convert=True)
def generate_wigs(qdnaseq_filename, copynumber_bedgraph_filename):
    df = pd.read_table(qdnaseq_filename)
    df_nonnull = df.loc[~(df["segmented"].isnull()),:]

    curr_chrom = None
    curr_start = None
    curr_end = None
    segments = []
    curr_val = None
    for index, row in df_nonnull.iterrows():
        if curr_val != row["segmented"] or curr_chrom != row["chromosome"]:
            if curr_start != None:
                # Record previous:
                segments.append((curr_chrom, curr_start, curr_end, curr_val))
            # Start new:
            curr_start = row["start"]
            curr_chrom = row["chromosome"]
            curr_val = row["segmented"]
        curr_end = row["end"]

    # Record final:
    segments.append((curr_chrom, curr_start, curr_end, curr_val))

    with open(copynumber_bedgraph_filename, 'w') as segfile:
        for seg in segments:
            print("\t".join([str(item) for item in seg]), file=segfile)
