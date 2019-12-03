

# def check_edge_bandwidth_sufficiency(substrate_network, e1, e2, bandwidth_usage_info, bandwidth_request):
#     edge_key = frozenset((e1,e2))
#     residual_bandwidth = None
#     if edge_key in bandwidth_usage_info:
#         residual_bandwidth = bandwidth_usage_info[edge_key] - bandwidth_request
#     else:
#         residual_bandwidth = substrate_network.get_link_bandwidth_free(e1,
#                                                                        e2) - bandwidth_request
#     if residual_bandwidth < 0:
#         return None
#     else:
#         bandwidth_usage_info[edge_key] = residual_bandwidth
#         return bandwidth_usage_info
#
# def check_path_bandwidth_sufficiency(substrate_network, path, bandwidth_usage_info, bandwidth_request):
#     length = len(path)
#     for i in range(0, length - 1):
#         e1 = path[i]
#         e2 = path[i+1]
#         res = check_edge_bandwidth_sufficiency(substrate_network, e1, e2, bandwidth_usage_info, bandwidth_request)
#         if res:
#
#
#
# def check_path_bandwidth_sufficiency(substrate_network, path, bandwidth_usage_info, bandwidth_request):
#     length = len(path)
#     for i in range(0, length - 1):
#         edge_key = frozenset((path[i], path[i + 1]))
#         residual_bandwidth = None
#         if edge_key in bandwidth_usage_info:
#             residual_bandwidth = bandwidth_usage_info[edge_key] - bandwidth_request
#         else:
#             residual_bandwidth = substrate_network.get_link_bandwidth_free(path[i],
#                                                                                 path[i + 1]) - bandwidth_request
#         if residual_bandwidth < 0:
#             return None
#         bandwidth_usage_info[edge_key] = residual_bandwidth
#     return bandwidth_usage_info