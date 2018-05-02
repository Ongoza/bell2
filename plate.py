from openalpr import Alpr
from argparse import ArgumentParser

# parser = ArgumentParser(description='OpenALPR Python Test Program')
#
# parser.add_argument("-c", "--country", dest="country", action="store", default="us",
#                   help="License plate Country" )
#
# parser.add_argument("--config", dest="config", action="store", default="/etc/openalpr/openalpr.conf",
#                   help="Path to openalpr.conf config file" )
#
# parser.add_argument("--runtime_data", dest="runtime_data", action="store", default="/usr/share/openalpr/runtime_data",
#                   help="Path to OpenALPR runtime_data directory" )
#
# parser.add_argument('plate_image', help='License plate image file')
#
# options = parser.parse_args()
options = {'plate_image': '/home/os/ea7.jpg', 'country': 'us',
           'runtime_data': '/usr/share/openalpr/runtime_data', 'config': '/etc/openalpr/openalpr.conf'}
print("config", options['country'])
alpr = None
try:
    alpr = Alpr(options['country'], options['config'], options['runtime_data'])
    # print('alpr', alpr)
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
    else:
        print("Using OpenALPR " + alpr.get_version())
        alpr.set_top_n(7)
        alpr.set_default_region("wa")
        alpr.set_detect_region(False)
        jpeg_bytes = open(options['plate_image'], "rb").read()
        results = alpr.recognize_array(jpeg_bytes)

        # Uncomment to see the full results structure
        # import pprint
        # pprint.pprint(results)

        print("Image size: %dx%d" % (results['img_width'], results['img_height']))
        print("Processing Time: %f" % results['processing_time_ms'])
        i = 0
        for plate in results['results']:
            i += 1
            print("Plate #", plate['candidates'][0]['plate'], " {:.2f}%".format(plate['candidates'][0]['confidence']))
            # print("   %12s %12s" % ("Plate", "Confidence"))
            # for candidate in plate['candidates']:
            #     prefix = "-"
            #     if candidate['matches_template']:
            #         prefix = "*"
            #     print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
    if alpr:
        print("end")
        alpr = 0
        # print("end2")
except:
    print("error")
    if alpr:
        print("end error")
        # alpr.unload()
        # print("end2 error")
