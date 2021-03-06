import begin, json


def extract_termini(bounds):
    regs = bounds.split(",")
    toks1 = regs[0].replace(":", "-").split("-")
    toks2 = regs[1].replace(":", "-").split("-")
    return ((toks1[0], int(toks1[1]), int(toks1[2])), (toks2[0], int(toks2[1]), int(toks2[2])))


class Event:
    def __init__(self, fields):
        self._patient_id = fields[0]
        self._sample_type = fields[1]
        self._sample_id = fields[2]
        self._event_type = fields[3]
        termini = extract_termini(fields[4])
        self._t1_chrom = termini[0][0]
        self._t1_start = int(termini[0][1])
        self._t1_end = int(termini[0][2])
        self._t2_chrom = termini[1][0]
        self._t2_start = int(termini[1][1])
        self._t2_end = int(termini[1][2])

    def to_string(self):
        return "%s_%s_%s_%s_%s:%d-%d_%s:%d-%d" % (self._patient_id,
                                                  self._sample_type,
                                                  self._sample_id,
                                                  self._event_type,
                                                  self._t1_chrom,
                                                  self._t1_start,
                                                  self._t1_end,
                                                  self._t2_chrom,
                                                  self._t2_start,
                                                  self._t2_end)


class EventCluster:
    def __init__(self, event):
        self._t1_chrom = event._t1_chrom
        self._t1_start = event._t1_start
        self._t1_end = event._t1_end
        self._t2_chrom = event._t2_chrom
        self._t2_start = event._t2_start
        self._t2_end = event._t2_end
        self._event_type = event._event_type
        self.events = [event]

    def get_key(self):
        return "%s_%s:%d-%d_%s:%d-%d" % (self._event_type,
                                         self._t1_chrom,
                                         self._t1_start,
                                         self._t1_end,
                                         self._t2_chrom,
                                         self._t2_start,
                                         self._t2_end)

    def overlap(self, event):
        if event._event_type != self._event_type:
            return False

        if event._t1_chrom != self._t1_chrom:
            return False
        if event._t2_chrom != self._t2_chrom:
            return False

        if event._t1_start > self._t1_end:
            return False
        if event._t1_end < self._t1_start:
            return False

        if event._t2_start > self._t2_end:
            return False
        if event._t2_end < self._t2_start:
            return False

        return True

    def expand(self, event):
        assert event._t1_chrom == self._t1_chrom
        assert event._t2_chrom == self._t2_chrom

        if event._t1_start < self._t1_start:
            self._t1_start = event._t1_start
        if event._t1_end > self._t1_end:
            self._t1_end = event._t1_end

        if event._t2_start < self._t2_start:
            self._t2_start = event._t2_start
        if event._t2_end > self._t2_end:
            self._t2_end = event._t2_end

        self.events.append(event)


@begin.start(auto_convert=True)
def process(events_filename="all_events.txt", output1="events.txt", output2="events.json"):
    events = [Event(line.strip().split()) for line in open(events_filename).readlines()]

    event_clusters = []
    for event in events:
        assigned_cluster = None
        for cluster in event_clusters:
            if cluster.overlap(event):
                assigned_cluster = cluster
                assigned_cluster.expand(event)

        if assigned_cluster == None:
            assigned_cluster = EventCluster(event)
            event_clusters.append(assigned_cluster)

    with open(output1, 'w') as out1:
        for cluster in event_clusters:
            event_strs = [event.to_string() for event in cluster.events]
            event_str = " ".join(event_strs)
            line = "%s # %s" % (cluster.get_key(), event_str)
            print(line, file=out1)
