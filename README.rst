Python OneMap SG API
====================

.. image:: https://travis-ci.org/windspeed-io/python-onemapsg.svg?branch=master
    :target: https://travis-ci.org/windspeed-io/python-onemapsg

.. image:: https://coveralls.io/repos/github/windspeed-io/python-onemapsg/badge.svg?branch=master
    :target: https://coveralls.io/github/windspeed-io/python-onemapsg?branch=master

.. image:: https://badge.fury.io/py/python-onemapsg.svg
    :target: https://badge.fury.io/py/python-onemapsg

Python Client for OneMap SG v2.

Only supports Python 3.6 and up.

This package can be used in production but is not fully featured yet.


Getting Started
===============

.. code-block:: python

    >> from onemapsg import OneMap
    >> onemap = OneMap('your-email', 'your-password')
    >> search = onemap.search('One Raffles Quay')
    # You can work directly with the SearchResult object
    >> search.found
    1
    >> search.page_num
    1
    >> len(search.results)
    1
    >> result = search.results[0]  # One Raffles Quay
    >> result.address
    '1 RAFFLES QUAY ONE RAFFLES QUAY SINGAPORE 048583'
    >> result.blk_no
    '1'
    >> result.building
    'ONE RAFFLES QUAY'
    >> result.lat_long
    ('1.28118338714692', '103.851899818913')
    >> result.postal
    '048583
    >> result.road_name
    'RAFFLES QUAY'
    >> result.search_value
    'ONE RAFFLES QUAY'
    # You can convert the results to a dictionary too
    >> search_as_dict = search.to_dict()
    >> from pprint import pprint
    >> pprint(search_as_dict)
    {'found': 1,
     'page_num': 1,
     'results': [{'address': '1 RAFFLES QUAY ONE RAFFLES QUAY SINGAPORE 048583',
                 'blk_no': '1',
                 'building': 'ONE RAFFLES QUAY',
                 'coordinates': ('30067.9405244123', '29292.2770711072'),
                 'lat_long': ('1.28118338714692', '103.851899818913'),
                 'postal': '048583',
                 'road_name': 'RAFFLES QUAY',
                 'search_value': 'ONE RAFFLES QUAY'}],
     'total_num_pages': 1}
    >> next_search = onemap.search('Paragon')
    >> pprint(next_search.to_dict())
    {'found': 7,
     'page_num': 1,
     'results': [{'address': '290 ORCHARD ROAD THE PARAGON SINGAPORE 238859',
                 'blk_no': '290',
                 'building': 'THE PARAGON',
                 'coordinates': ('28282.5637398548', '31801.0936260298'),
                 'lat_long': ('1.30387230879998', '103.835857545469'),
                 'postal': '238859',
                 'road_name': 'ORCHARD ROAD',
                 'search_value': 'THE PARAGON'},
                 ...
                 ...
                 ...
     'total_num_pages': 1}
     >> next_result = next_search.results[0]  # Paragon
     # Find the route between One Raffles Quay and Paragon
     >> orq_latlong = ','.join(result.lat_long)
     >> paragon_latlong = ','.join(next_result.lat_long)
     >> route = onemap.route(orq_latlong, paragon_latlong, 'drive')
     >> pprint(route.to_dict())
    {'route_geometry': 'uiyFapzxRt@`@lAr@v@b@wAxCMXkAdCi@xAiArBq@xAoAnC_@t@sB|DQT}@fBWh@iChFYd@}C`Ek@n@[Vm@Vc@Jm@Dc@EqAe@i@ZkAbDgAnA}@UMGu@]uEqBOGMEsAe@aEoB{G}CMGKE_Bo@}@UcAEsEVg@BaCNiA|AI\\wAb@qClAWFaBn@u@d@EDKN_@r@g@lBc@hBM~@AZPtBA\\yA~LSvAu@~EUbAq@xBuAk@}BaAm@WuB_A_AGk@BqDoAe@S',
    'route_instructions': [['Head',
                            'RAFFLES QUAY',
                            125,
                            '1.281708,103.851687',
                            16,
                            '125m',
                            'South West',
                            'North',
                            'driving',
                            'Head Southwest On Raffles Quay'],
                            ['Right',
                            'CROSS STREET',
                            641,
                            '1.280771,103.851082',
                            73,
                            '641m',
                            'North West',
                            'South West',
                            'driving',
                            'Turn Right Onto Cross Street'],
                            ...
                            ...
                            ['Slight Left',
                            'ORCHARD LINK',
                            60,
                            '1.302314,103.835849',
                            11,
                            '60m',
                            'North',
                            'North East',
                            'driving',
                            'Make A Slight Left To Stay On Orchard Link'],
                            ['Slight Right',
                            'BIDEFORD ROAD',
                            134,
                            '1.302845,103.835865',
                            15,
                            '134m',
                            'North East',
                            'North',
                            'driving',
                            'Continue Slightly Right Onto Bideford Road'],
                            ['Left',
                            'BIDEFORD ROAD',
                            0,
                            '1.303932,103.836371',
                            0,
                            '0m',
                            'North',
                            'North East',
                            'driving',
                            'You Have Arrived At Your Destination, On The Left']],
    'route_name': ['UPPER CROSS STREET', 'CLEMENCEAU AVENUE'],
    'route_summary': {'end_point': 'BIDEFORD ROAD',
                    'start_point': 'RAFFLES QUAY',
                    'total_distance': 4163,
                    'total_time': 489},
    'status': 0,
    'status_message': 'Found route between points'}
    # You can get the decoded polyline lat longs
    >> pprint(route.lat_longs)
    [(1.28171, 103.85169),
    (1.28144, 103.85152),
    (1.28105, 103.85126),
    (1.28077, 103.85108),
    ...
    (1.30007, 103.83581),
    (1.30018, 103.83547),
    (1.30043, 103.83486),
    (1.30086, 103.83508),
    (1.30149, 103.83541),
    (1.30172, 103.83553),
    (1.30231, 103.83585),
    (1.30263, 103.83589),
    (1.30285, 103.83587),
    (1.30374, 103.83627),
    (1.30393, 103.83637)]
