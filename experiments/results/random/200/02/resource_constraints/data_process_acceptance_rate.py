def average(l):
    print l
    return sum(l) / len(l)

target_name = './failed-count_summary.csv'
for number_of_vnf in [2, 3, 4, 5]:

    with open(target_name, 'a') as tg_file:
        s = 'vnf-' + str(number_of_vnf) + "\n"
        tg_file.write(s)
        s = ',Proposed,GD,SK-1,SK-10,BC,RA'  + "\n"
        tg_file.write(s)
    for number_of_sfc in [100, 200, 300, 400, 500]:
        file_name = './' + str(number_of_sfc) + '-' + str(number_of_vnf) +'-results-failed-count.csv'
        proposed_list = []
        gd_list = []
        sk_1_list = []
        sk_10_list = []
        bc_list = []
        ra_list = []
        with open(file_name, 'r') as rd_file:
            for line in rd_file.readlines():
                [pd, gd, sk1, sk10, bc, ra] = line.split(',')
                proposed_list.append(float(pd))
                gd_list.append(float(gd))
                sk_1_list.append(float(sk1))
                sk_10_list.append(float(sk10))
                bc_list.append(float(bc))
                ra_list.append(float(ra))


        pd, gd, sk1, sk10, bc, ra = \
            (number_of_sfc - average(proposed_list)) * 1.0 / number_of_sfc, \
            (number_of_sfc - average(gd_list)) * 1.0 / number_of_sfc, \
            (number_of_sfc - average(sk_1_list)) * 1.0 / number_of_sfc, \
            (number_of_sfc - average(sk_10_list)) * 1.0 / number_of_sfc, \
            (number_of_sfc - average(bc_list)) * 1.0 / number_of_sfc, \
            (number_of_sfc - average(ra_list)) * 1.0 / number_of_sfc

        s = ','.join([str(number_of_sfc), str(pd), str(gd), str(sk1), str(sk10), str(bc), str(ra)])
        with open(target_name, 'a') as tg_file:
            s = s  + "\n"
            tg_file.write(s)