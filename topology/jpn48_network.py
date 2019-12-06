import networkx as nx
import matplotlib.pyplot as plt
from core.net import Net


bandwidth_capacity = 100
cpu_capacity = 100
def generate_substrate_network():
    substrate_network = Net()
    substrate_network.init_bandwidth_capacity(0, 1, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(0, 2, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(1, 2, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(1, 3, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(2, 3, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(2, 4, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(3, 5, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(3, 16, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(4, 5, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(4, 6, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(4, 8, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(5, 16, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(6, 16, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(6, 7, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(7, 8, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(7, 9, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(7, 10, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(8, 11, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(8, 9, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(9, 11, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(9, 12, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(10, 9, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(10, 13, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(10, 18, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(10, 16, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(11, 12, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(12, 14, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(12, 13, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(13, 14, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(13, 15, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(14, 19, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(15, 19, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(15, 18, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(15, 23, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(16, 17, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(16, 18, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(17, 20, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(17, 18, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(18, 23, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(19, 23, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(20, 21, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(21, 26, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(22, 23, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(22, 25, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(23, 24, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(24, 25, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(24, 31, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(24, 46, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(25, 26, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(26, 46, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(26, 27, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(26, 33, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(26, 28, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(27, 46, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(27, 28, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(27, 31, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(28, 30, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(29, 32, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(29, 47, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(30, 32, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(30, 36, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(31, 29, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(32, 47, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(32, 34, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(33, 30, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(33, 35, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(34, 47, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(34, 40, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(35, 37, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(36, 37, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(36, 34, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(37, 38, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(38, 40, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(38, 41, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(38, 39, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(39, 40, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(39, 44, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(40, 42, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(41, 43, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(42, 44, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(43, 45, bandwidth_capacity)

    substrate_network.init_bandwidth_capacity(44, 45, bandwidth_capacity)







##############
    substrate_network.init_link_latency(0, 1, 1.5884322213336)
    substrate_network.init_link_latency(0, 2, 1.36694566212203)

    substrate_network.init_link_latency(1, 2, 0.595078345833503)
    substrate_network.init_link_latency(1, 3, 0.606753089165439)

    substrate_network.init_link_latency(2, 3, 0.424627093187248)
    substrate_network.init_link_latency(2, 4, 0.612090114688609)

    substrate_network.init_link_latency(3, 5, 0.70582162543929)
    substrate_network.init_link_latency(3, 16, 0.910629979890955)

    substrate_network.init_link_latency(4, 5, 0.203807662166071)
    substrate_network.init_link_latency(4, 6, 0.26351563520654)
    substrate_network.init_link_latency(4, 8, 0.818566289616265)

    substrate_network.init_link_latency(5, 16, 0.623764858020544)

    substrate_network.init_link_latency(6, 16, 0.600748935451872)
    substrate_network.init_link_latency(6, 7, 0.544710167458582)

    substrate_network.init_link_latency(7, 8, 0.318887275009433)
    substrate_network.init_link_latency(7, 9, 0.264182763396936)
    substrate_network.init_link_latency(7, 10, 0.355245761386032)

    substrate_network.init_link_latency(8, 11, 0.425294221377644)
    substrate_network.init_link_latency(8, 9, 0.390269991381838)

    substrate_network.init_link_latency(9, 11, 0.220485866925979)
    substrate_network.init_link_latency(9, 12, 0.10106992084504)

    substrate_network.init_link_latency(10, 9, 0.24917237911302)
    substrate_network.init_link_latency(10, 13, 0.321555787771019)
    substrate_network.init_link_latency(10, 18, 0.39160424776263)
    substrate_network.init_link_latency(10, 16, 0.76352821390857)

    substrate_network.init_link_latency(11, 12, 0.130757125317676)

    substrate_network.init_link_latency(12, 14, 0.0960664594170678)
    substrate_network.init_link_latency(12, 13, 0.158109381123924)

    substrate_network.init_link_latency(13, 14, 0.121750894747325)
    substrate_network.init_link_latency(13, 15, 0.289200070536798)

    substrate_network.init_link_latency(14, 19, 0.505016040130002)

    substrate_network.init_link_latency(15, 19, 0.408282452522538)
    substrate_network.init_link_latency(15, 18, 0.547045116124969)
    substrate_network.init_link_latency(15, 23, 0.876606442180744)

    substrate_network.init_link_latency(16, 17, 0.847586365898504)
    substrate_network.init_link_latency(16, 18, 0.704820933153695)

    substrate_network.init_link_latency(17, 20, 0.198137072547702)
    substrate_network.init_link_latency(17, 18, 0.643111575542037)

    substrate_network.init_link_latency(18, 23, 0.836578750756965)

    substrate_network.init_link_latency(19, 23, 0.619762088878167)

    substrate_network.init_link_latency(20, 21, 0.255843661016983)

    substrate_network.init_link_latency(21, 26, 0.494008424988463)

    substrate_network.init_link_latency(22, 23, 0.10106992084504)
    substrate_network.init_link_latency(22, 25, 0.357914274147617)

    substrate_network.init_link_latency(23, 24, 0.221820123306771)

    substrate_network.init_link_latency(24, 25, 0.28152809634724)
    substrate_network.init_link_latency(24, 31, 1.21884320385405)
    substrate_network.init_link_latency(24, 46, 0.298539865202346)

    substrate_network.init_link_latency(25, 26, 0.0333564095198152)

    substrate_network.init_link_latency(26, 46, 0.139096227697629)
    substrate_network.init_link_latency(26, 27, 0.130089997127279)
    substrate_network.init_link_latency(26, 33, 0.845584981327315)
    substrate_network.init_link_latency(26, 28, 0.25817860968337)

    substrate_network.init_link_latency(27, 46, 0.173453329503039)
    substrate_network.init_link_latency(27, 28, 0.123085151128118)
    substrate_network.init_link_latency(27, 31, 0.253842276445794)

    substrate_network.init_link_latency(28, 30, 0.47833091251415)

    substrate_network.init_link_latency(29, 32, 0.248505250922623)
    substrate_network.init_link_latency(29, 47, 0.522694937175504)

    substrate_network.init_link_latency(30, 32, 0.239499020352273)
    substrate_network.init_link_latency(30, 36, 0.538038885554619)

    substrate_network.init_link_latency(31, 29, 0.219485174640384)

    substrate_network.init_link_latency(32, 47, 0.531367603650656)
    substrate_network.init_link_latency(32, 34, 0.648448601065208)

    substrate_network.init_link_latency(33, 30, 0.47299388699098)
    substrate_network.init_link_latency(33, 35, 0.405613939760953)

    substrate_network.init_link_latency(34, 47, 0.837913007137758)
    substrate_network.init_link_latency(34, 40, 0.555384218504923)

    substrate_network.init_link_latency(35, 37, 0.85559190418326)

    substrate_network.init_link_latency(36, 37, 0.442973118423146)
    substrate_network.init_link_latency(36, 34, 0.220819431021177)

    substrate_network.init_link_latency(37, 38, 0.493341296798067)

    substrate_network.init_link_latency(38, 40, 0.662124728968332)
    substrate_network.init_link_latency(38, 41, 0.17879035502621)
    substrate_network.init_link_latency(38, 39, 0.394939888714612)

    substrate_network.init_link_latency(39, 40, 0.493674860893265)
    substrate_network.init_link_latency(39, 44, 0.568726782312849)

    substrate_network.init_link_latency(40, 42, 0.690477677060175)

    substrate_network.init_link_latency(41, 43, 0.334564787483746)

    substrate_network.init_link_latency(42, 44, 0.419957195854473)

    substrate_network.init_link_latency(43, 45, 2.52841584160199)

    substrate_network.init_link_latency(44, 45, 2.24722130934995)



    substrate_network.init_node_cpu_capacity(1, 100)
    substrate_network.init_node_cpu_capacity(2, 100)
    substrate_network.init_node_cpu_capacity(3, 100)
    substrate_network.init_node_cpu_capacity(4, 100)
    substrate_network.init_node_cpu_capacity(5, 100)
    substrate_network.init_node_cpu_capacity(6, 100)

    for i in range(0, 48):
        print i
        substrate_network.init_node_cpu_capacity(i, cpu_capacity)




    substrate_network.pre_get_single_source_minimum_latency_path()
    substrate_network.update()

    return substrate_network

JPN48 = generate_substrate_network()

if __name__ == '__main__':
    substrate_network = generate_substrate_network()
    nx.draw(substrate_network)  # networkx draw()
    plt.draw()  # pyplot draw()
    plt.show()