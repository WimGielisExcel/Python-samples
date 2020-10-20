from TM1py.Services import TM1Service

def count_public_views_and_subsets():

    ####################################################
    # Author: Wim Gielis
    # Date: 17-10-2020
    # Purpose:
    # - list the number of public cube views and dimension subsets
    # - for clean up purposes, of objects lurking around in the TM1 data directory
    # - there is a similar coding in Turbo Integrator available at GitHub. All in all, I prefer the solution in TI.
    ####################################################

    # =============================================================================================================
    # START of parameters and settings
    # =============================================================================================================

    # TM1 connection settings (IntegratedSecurityMode = 1 for now)
    ADDRESS = 'localhost'
    USER = 'wim'
    PWD = ''
    PORT = 8001
    SSL = False

    RESULT_FILE = r'D:\count public views and subsets.txt'

    # list a cube or dimension only if the count of views, dimensions, resp. exceeds the threshold
    threshold_views = 8
    threshold_subsets = 8

    # =============================================================================================================
    # END of parameters and settings
    # =============================================================================================================

    log_lines = []
    public_views = {}
    public_subsets = {}

    tm1 = TM1Service(address=ADDRESS, port=PORT, user=USER, password=PWD, namespace='', gateway='', ssl=SSL)

    # iterate through cubes and dimensions to count the public views, subsets, resp.
    cube_names = tm1.cubes.get_all_names()
    for cube_name in cube_names:
        private_view_names, public_views_names = tm1.cubes.views.get_all_names(cube_name=cube_name)
        public_views[cube_name] = len(public_views_names)

    # - remove dictionary items if the count does not exceed the threshold
    # - sort the dictionary
    if public_views:
        public_views = dict(filter(lambda elem: elem[1] >= threshold_views, public_views.items()))
    if public_views:
        public_views = sorted(public_views.items(), key=lambda x: x[1], reverse=True)

    # now similar coding for subsets, but we will increment dictionary values
    dimension_names = tm1.dimensions.get_all_names()
    for dimension_name in dimension_names:
        subsets = tm1.dimensions.subsets.get_all_names(dimension_name=dimension_name, hierarchy_name=dimension_name, private=False)
        # increment instead of write, because PAW alternate hierarchies will be counted with the main (container) dimension
        if dimension_name in public_subsets:
            public_subsets[dimension_name] += len(subsets)
        else:
            public_subsets[dimension_name] = len(subsets)

    if public_subsets:
        public_subsets = dict(filter(lambda elem: elem[1] >= threshold_subsets, public_subsets.items()))
    if public_subsets:
        public_subsets = sorted(public_subsets.items(), key=lambda x: x[1], reverse=True)

    # output to a text file
    log_lines.append("Public cube views: (at least " + str(threshold_views) + ")")
    log_lines.append("-" * 35 + "\n")
    for k, value in public_views:
        log_lines.append("\t{}\t\t{}".format(value, k))

    log_lines.append("\n\nPublic dimension subsets: (at least " + str(threshold_subsets) + ")")
    log_lines.append("-" * 35 + "\n")
    for k, value in public_subsets:
        log_lines.append("\t{}\t\t{}".format(value, k))

    with open(RESULT_FILE, 'w', encoding='utf-8') as file:
        file.write("\n".join(log_lines))
        file.close()

if __name__ == "__main__":
    count_public_views_and_subsets()
