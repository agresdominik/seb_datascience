 
""" 
    # window open times in CET time, because Prometheus export is in utc see set below
    window_open_times = [
        ('2024-12-01 23:15:00', '2024-12-01 23:45:00'),
        ('2024-12-02 12:05:00', '2024-12-02 12:35:00'),
        ('2024-12-03 19:10:00', '2024-12-03 19:40:00'),
        ('2024-12-04 08:27:00', '2024-12-04 08:57:00'),
        ('2024-12-05 22:20:00', '2024-12-05 22:50:00'),
        ('2024-12-06 07:59:00', '2024-12-06 08:29:00'),
        ('2024-12-06 14:51:00', '2024-12-06 15:21:00'),
        ('2024-12-07 06:35:00', '2024-12-07 07:05:00'),
        ('2024-12-08 09:06:30', '2024-12-08 09:36:30'),
        ('2024-12-08 18:25:30', '2024-12-08 18:55:30'),
        ('2024-12-09 23:00:00', '2024-12-09 23:30:00'),
        ('2024-12-10 07:32:00', '2024-12-10 08:02:00'),
        ('2024-12-10 18:08:00', '2024-12-10 18:38:00')
    ]
    """
WINDOW_OPEN_TIMES = [
    ('2024-12-01 22:00:00'),
    ('2024-12-02 11:05:00'),
    ('2024-12-03 18:10:00'),
    ('2024-12-04 07:27:00'),
    ('2024-12-05 21:20:00'),
    ('2024-12-06 06:59:00'),
    ('2024-12-06 13:51:00'),
    ('2024-12-07 05:35:00'),
    ('2024-12-08 08:06:00'),
    ('2024-12-08 17:25:00'),
    ('2024-12-09 22:00:00'),
    ('2024-12-10 06:32:00'),
    ('2024-12-10 17:08:00'),
    ('2024-12-10 20:15:00'),
    ('2024-12-10 22:27:00'),
    ('2024-12-11 07:30:00'),
    ('2024-12-11 09:15:00'),
    ('2024-12-11 12:13:00'),
    ('2024-12-14 12:45:00'),
    ('2024-12-15 14:02:00')
]