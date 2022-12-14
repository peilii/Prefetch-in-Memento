import matplotlib.pyplot as plt
import re
import numpy as np
from statistics import mean, median, mode, variance
from matplotlib.ticker import PercentFormatter

max_latency_in_figure = 500
result_dir = "/u2/pei/simulator/results/dynamic_html_baseline_v2_splitup/dynamic-html_bypass/"
class Stat:
    def __init__(self):
        self.physical_address = 0
        self.size = 0
        self.alloc_cycle = 0
        self.access_create_cycle = 0
        self.access_handle_cycle = 0
        self.alloc_time_create = 0
        self.access_time_create = 0

    # def __init__(self, physical_address, size, alloc_cycle, access_create_cycle, access_handle_cycle):
    #     self.physical_address = physical_address
    #     self.size = size
    #     self.alloc_cycle = alloc_cycle
    #     self.access_create_cycle = access_create_cycle
    #     self.access_handle_cycle = access_handle_cycle

    def setPA(self, physical_address):
        self.physical_address = physical_address
    
    def setSize(self, size):
        self.size = size
    
    def setAllocCycle(self, alloc_cycle):
        self.alloc_cycle = alloc_cycle
    
    def setAccessCreateCycle(self, access_create_cycle):
        self.access_create_cycle = access_create_cycle

    def setAccessHandleCycle(self, access_handle_cycle):
        self.access_handle_cycle = access_handle_cycle

    def calculateAllocAccessDistance(self):
        return int(str(self.access_create_cycle), 0) - int(str(self.alloc_cycle), 0)

    def calculateAccessLatency(self):
        return int(str(self.access_handle_cycle), 0) - int(str(self.access_create_cycle), 0)

    def setAllocTimeCreate(self, time_create):
        self.alloc_time_create = time_create
    
    def setAccessTimeCreate(self, time_create):
        self.access_time_create = time_create

    def calculateTimeCreate(self):
        return self.access_time_create - self.alloc_time_create
    



# VA to Stat
total_stat = {}

# alloc - access distance (/cycles)

# number

# size

if __name__ == "__main__":
    file = open(result_dir + 'stat.txt', 'r')
    lines = file.readlines()

    alloc_access_list = []
    access_latency_list = []
    alloc_access_cnt = 0
    access_latency_cnt = 0
    max_latency = 0
    max_addr = 0
    max_dist = 0
    l1 = 0
    l2 = 0
    l3 = 0
    memory = 0

    l1_cycle_all = 0
    l2_cycle_all = 0
    l3_cycle_all = 0
    tlb_cycle_all = 0
    mem_cycle_all = 0

    l1_lat_avg = 0
    l2_lat_avg = 0
    l3_lat_avg = 0
    mem_lat_avg = 0

    tail_cycle_l1 = 0
    tail_cycle_tlb = 0
    tail_cycle_l2 = 0
    tail_cycle_l3 = 0
    tail_cycle_mem = 0

    tail_l1_handle = 0
    tail_l2_handle = 0
    tail_l3_handle = 0
    tail_mem_handle = 0
    time_create = 0
    for line in lines:
        match = re.findall(r'0[xX][0-9a-fA-F]+', line)
        if "[Allocate]" in line:
            # 0[xX][0-9a-fA-F]+
            match = re.findall(r'0[xX][0-9a-fA-F]+', line)
            line_list = line.split(',')
            sz = 0
            for l in line_list:
                if "size:" in l:
                    l_list = l.split(':')
                    sz = int(l_list[1].strip())
                elif "time create" in l:
                    l_list = l.split(':')
                    time_create = int(l_list[1].strip())

            if sz <= 512 and sz > 0 and match[2] != '0x0':
                stat = Stat()
                stat.setPA(match[1])
                stat.setAllocCycle(match[2])
                stat.setAllocTimeCreate(time_create)
                total_stat[match[0]] = stat

        elif "[Access]" in line:
            tp = 0
            line_list = line.split(',')
            level = ""
            tlb_cycle = 0
            l1_cycle = 0
            l2_cycle = 0
            l3_cycle = 0
            mem_cycle = 0
            for l in line_list:
                if "level:" in l:
                    l_list = l.split(':')
                    level = l_list[1].strip()
                elif "cycle_tlb" in l:
                    l_list = l.split(':')
                    tlb_cycle = int(l_list[1].strip())
                    tlb_cycle_all += tlb_cycle
                elif "cycle_L1" in l:
                    l_list = l.split(':')
                    l1_cycle = int(l_list[1].strip())
                    l1_cycle_all += l1_cycle
                elif "cycle_L2" in l:
                    l_list = l.split(':')
                    l2_cycle = int(l_list[1].strip())
                    l2_cycle_all += l2_cycle
                elif "cycle_L3" in l:
                    l_list = l.split(':')
                    l3_cycle = int(l_list[1].strip())
                    l3_cycle_all += l3_cycle
                elif "cycle_Mem" in l:
                    l_list = l.split(':')
                    mem_cycle = int(l_list[1].strip())
                    mem_cycle_all += mem_cycle
                elif "time create" in l:
                    l_list = l.split(':')
                    time_create = int(l_list[1].strip())
            if match[0] not in total_stat:
                continue
            if level == "l1d" and l1_cycle > 1000:
                continue
            stat = Stat()
            total_stat[match[0]] = stat
            total_stat[match[0]].setAccessCreateCycle(match[1])
            total_stat[match[0]].setAccessHandleCycle(match[2])
            latency = total_stat[match[0]].calculateAccessLatency()

            if (level == "l1d"):
                l1 += 1
                l1_lat_avg += latency
            elif level == "l2cache":
                l2 += 1
                l2_lat_avg += latency
            elif level == "memory":
                memory += 1
                mem_lat_avg += latency
            else:
                l3 += 1
                l3_lat_avg += latency

            if max_latency < latency:
                max_latency = latency
                max_addr = match[0]
            # if total_stat[match[0]].alloc_cycle != '0x0':
            access_latency_cnt += 1
            if latency < max_latency_in_figure:
                access_latency_list.append(latency)
            else:
                tail_cycle_l1 += l1_cycle
                tail_cycle_l2 += l2_cycle
                tail_cycle_l3 += l3_cycle
                tail_cycle_mem += mem_cycle
                tail_cycle_tlb += tlb_cycle
                if (level == "l1d"):
                    tail_l1_handle += 1
                elif level == "l2cache":
                    tail_l2_handle += 1
                elif level == "memory":
                    tail_mem_handle += 1
                else:
                    tail_l3_handle += 1

            stat.setAccessTimeCreate(time_create)
            distance = total_stat[match[0]].calculateAccessLatency()

            # if total_stat[match[0]].alloc_cycle != '0x0':
            if distance >= 0:
                alloc_access_cnt += 1

                if distance < 500:
                    alloc_access_list.append(distance)
                if max_dist < distance:
                    max_dist = distance
                    max_addr = match[0]
    print("Statistics of Allocation-access distance:")
    print("Mean:{}".format(np.mean(alloc_access_list)))
    print("Median:{}".format(median(alloc_access_list)))
    print("Mode:{}".format(mode(alloc_access_list)))
    print("Max: {}".format(max_dist))
    print("Total # of access: {}".format(alloc_access_cnt))
    f = plt.figure(1)
    counts, edges = np.histogram(alloc_access_list, bins=np.arange(0, 500, 10))
    

    # plt.hist(alloc_access_list, 100)
    print("***********")
    counts = counts.tolist()
    edges = edges.tolist()
    counts.append(alloc_access_cnt - len(alloc_access_list))
    for i in range(len(counts)):
        counts[i] = counts[i] * 100 / alloc_access_cnt
    
    x = []
    for i in range(len(edges)):
        left = '0' if i == 0 else edges[i]
        right = 'inf' if i == len(edges) - 1 else edges[i + 1]
        x += ["[{}, {})".format(left, right)]
    

    
    # print(x)

    # _, _, bars = plt.hist(alloc_access_list, bins=10)
    # plt.bar_label(bars)
    # print(counts)
    # print(edges)
    plt.xticks(fontsize=8, rotation=90)
    plt.bar(x, counts)
    # print(bars)
    # plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

    plt.xlabel('Allocation-Access Distance (Cycles)')
    plt.ylabel('% of Total Accesses')
    plt.tight_layout()
    f.savefig(result_dir + 'alloc_access_list.png')

    print("Statistics of Access latency:")
    print("Mean:{}".format(np.mean(access_latency_list)))
    print("Median:{}".format(median(access_latency_list)))
    print("Mode:{}".format(mode(access_latency_list)))
    print("Max:{}".format(max_latency))
    print("Total # of access: {}".format(access_latency_cnt))
    g = plt.figure(2)
    counts, edges = np.histogram(access_latency_list, bins=np.arange(0, max_latency_in_figure, 25))
    counts = counts.tolist()
    edges = edges.tolist()
    counts.append(access_latency_cnt - len(access_latency_list))
    for i in range(len(counts)):
        counts[i] = counts[i] * 100 / access_latency_cnt

    x = []
    for i in range(len(edges)):
        left = '0' if i == 0 else edges[i]
        right = 'inf' if i == len(edges) - 1 else edges[i + 1]
        x += ["[{}, {})".format(left, right)]
    # _, _, bars = plt.hist(access_latency_list, bins=50)
    # print(counts)
    # print(edges)
    # plt.bar_label(bars)
    # plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.xticks(fontsize=6, rotation=90)
    plt.bar(x, counts)
    plt.xlabel('First Access Latency (Cycles)')
    plt.ylabel('% of Total Accesses')
    plt.tight_layout()
    g.savefig(result_dir + 'access_latency_list.png')


    print("l1 : {}".format(l1))
    print("l2 : {}".format(l2))
    print("l3 : {}".format(l3))
    print("memory : {}".format(memory))
    total = 100 / (l1 + l2 + l3 + memory)
    h = plt.figure(3)
    x = ["l1", "l2", "l3", "memory"]
    counts = [l1 * total, l2 * total, l3 * total, memory * total]
    plt.bar(x, counts)
    plt.xlabel('Level')
    plt.ylabel('% of Total Accesses')
    plt.tight_layout()
    h.savefig(result_dir + 'level_handle.png')

    print("TLB cycle: {}".format(tlb_cycle_all))
    print("l1 cycle: {}".format(l1_cycle_all))
    print("l2 cycle: {}".format(l2_cycle_all))
    print("l3 cycle: {}".format(l3_cycle_all))
    print("mem cycle: {}".format(mem_cycle_all))

    p = plt.figure(4)
    cycles = [tlb_cycle_all, l1_cycle_all, l2_cycle_all, l3_cycle_all, mem_cycle_all]
    x = ["tlb", "l1", "l2", "l3", "memory"]
    plt.bar(x, cycles)

    plt.xlabel('Level')
    plt.ylabel('% of Total Cycles')
    plt.tight_layout()
    p.savefig(result_dir + 'cycle_breakdown.png')

    q = plt.figure(5)
    x = ["l1", "l2", "l3", "memory"]
    cycles = [l1_lat_avg / l1 if l1 != 0 else 0, l2_lat_avg / l2 if l2 != 0 else 0, l3_lat_avg / l3 if l3 != 0 else 0, mem_lat_avg / memory if memory != 0 else 0]
    plt.bar(x, cycles)
    plt.xlabel('Level handle')
    plt.ylabel('Average Latency in Cycles')
    plt.tight_layout()
    q.savefig(result_dir + 'avg_level_latency_breakdown.png')

    r = plt.figure(6)
    cycles = [tail_cycle_tlb, tail_cycle_l1, tail_cycle_l2, tail_cycle_l3, tail_cycle_mem]
    x = ["tlb", "l1", "l2", "l3", "memory"]
    plt.bar(x, cycles)

    plt.xlabel('Level')
    plt.ylabel('# of Total Cycles')
    plt.tight_layout()
    r.savefig(result_dir + 'tail_cycle_breakdown.png')

    s = plt.figure(7)
    x = ["l1", "l2", "l3", "memory"]
    cycles = [tail_l1_handle, tail_l2_handle, tail_l3_handle, tail_mem_handle]
    plt.bar(x, cycles)
    plt.xlabel('Level handle')
    plt.ylabel('# of access')
    plt.tight_layout()
    s.savefig(result_dir + 'tail_level_breakdown.png')

