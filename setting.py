HOST = 'gardenia.csie.ntu.edu.tw'
USER = 'r324_data_reader'
PASSWORD = 'agent#336'
DATABASE = 'blt-thesis'

BEGIN = '2014-09-01'
END = '2014-09-07'

FEATURE_LENGTH = 49
FEATURE_MAPPING = {
    '99': {
        'S4_PIR': 1,
        'S6_Temp': 2,
        'S6_Humi': 3,
        'S24_PIR': 4,
        'S26_Temp': 5,
        'S26_Humi': 6,
        'S28_Temp': 7,
        'S28_Humi': 8,
        'S60_Light': 9,
        'S61_Sound': 10,
        'S65_Light': 11,
        'S67_Sound': 12
    },
    '100': {
        'S3_PIR': 13,
        'S6_Temp': 14,
        'S6_Humi': 15,
        'S14_PIR': 16,
        'S20_Magnet': 17,
        'S24_PIR': 18,
        'S26_Temp': 19,
        'S26_Humi': 20,
        'S28_Magnet': 21,
        'S60_Light': 22,
        'S65_Light': 23,
        'S67_Sound': 24,
        'S69_Sound': 25
    },
    '101': {
        'S4_PIR': 26,
        'S6_Temp': 27,
        'S6_Humi': 28,
        'S54_Sound': 29,
        'S56_Sound': 30
    },
    '102': {
        'S11_PIR': 31,
        'S12_PIR': 32,
        'S15_Magnet': 33,
        'S21_PIR': 34,
        'S22_Temp': 35,
        'S22_Humi': 36,
        'S31_PIR': 37,
        'S32_PIR': 38,
        'S33_PIR': 39,
        'S34_PIR': 40,
        'S55_Light': 41,
        'S56_Sound': 42,
        'S57_Sound': 43,
        'S58_Sound': 44
    },
    '103': {
        'A9_WallBtn': 45,
        'A5_WallBtn': 46,
        'A7_WallBtn': 47,
        'A11_WallBtn': 48
    }
}
