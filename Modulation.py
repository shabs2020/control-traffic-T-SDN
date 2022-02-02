import math


def _calculate_regen(link_distance, max_distance):
    regenerators = 0
    if link_distance > max_distance:
        regenerators = math.ceil(link_distance / max_distance) - 1
    return regenerators


# def _BPSK():
#     max_distance=4000
#     max_capacity = 300
#     spectralEfficiency=1
#     return max_distance,spectralEfficiency,'BPSK'

def _QPSK():
    max_distance = 2397
    max_capacity = 100
    spectralEfficiency = 2
    return max_capacity, max_distance, spectralEfficiency, 'QPSK'


def _8QAM():
    max_distance = 1096
    max_capacity = 150
    spectralEfficiency = 3
    return max_capacity, max_distance, spectralEfficiency, '8QAM'


def _16QAM():
    max_distance = 537
    max_capacity = 200
    spectralEfficiency = 4
    return max_capacity, max_distance, spectralEfficiency, '16QAM'


def _32QAM():
    max_distance = 288
    max_capacity = 250
    spectralEfficiency = 5
    return max_capacity, max_distance, spectralEfficiency, '32QAM'


def _64QAM():
    max_distance = 135
    max_capacity = 300
    spectralEfficiency = 6
    return max_capacity, max_distance, spectralEfficiency, '64QAM'


def _calculate_bvt(bitrate, max_capacity):
    bvt_one_end = math.ceil(bitrate / max_capacity)
    return 2 * bvt_one_end


def _calc_slots(spectral_efficiency, bitrate):
    slots = math.ceil(2 * (((((bitrate*(10**9))) / spectral_efficiency) + 6.25) / (12.5*(10**9))))
    return slots


def _select_modulation(link_distance, bitrate):
    if (link_distance > 0) & (link_distance <= 135):
        max_capacity, max_distance, spectral_efficiency, mod_type = _64QAM()
    elif (link_distance > 135) & (link_distance <= 288):
        max_capacity, max_distance, spectral_efficiency, mod_type = _32QAM()
    elif (link_distance > 288) & (link_distance <= 537):
        max_capacity, max_distance, spectral_efficiency, mod_type = _16QAM()
    elif (link_distance > 537) & (link_distance <= 1096):
        max_capacity, max_distance, spectral_efficiency, mod_type = _8QAM()
    else:
        max_capacity, max_distance, spectral_efficiency, mod_type = _QPSK()

    # bvt = _calculate_bvt(bitrate, max_capacity)
    slots = _calc_slots(spectral_efficiency, bitrate)
    return  slots, mod_type, max_capacity
