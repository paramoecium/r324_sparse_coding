import datetime
import time
import argparse
import numpy as np
import shutil
import MySQLdb
HOST = 'gardenia.csie.ntu.edu.tw'
USER = 'yuchentsai'
PASSWORD = 'r324reader#336'
DATABASE = 'blt-thesis'

BEGIN = '2015-06-15'
END = '2015-06-17'

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


def to_file(in_dir,file_name, data):
    file = open('{}/{}'.format(in_dir,file_name), 'wb')
    vector = ['?'] * FEATURE_LENGTH
    template = ', '.join(['{}'] * FEATURE_LENGTH) + '\n'
    reference = 0
    for row in data:
        [node_id, name, value, created_at] = row
        timestamp = int(time.mktime(created_at.timetuple()))
        if reference == 0:
            vector[0] = timestamp
            reference = timestamp
        if reference != timestamp:
            file.write(template.format(*vector))
            vector = ['?'] * FEATURE_LENGTH
            vector[0] = timestamp
            reference = timestamp
        try:
            index = FEATURE_MAPPING[str(node_id)][name]
            vector[index] = value
        except Exception:
            print 'Exception: ', node_id, '; ' ,name, '; ', index, '; ', value
            pass
    file.close()
    print 'Write "{}"'.format(file_name)


def downLoad(in_dir):
    # database connection
    db = MySQLdb.connect(HOST, USER, PASSWORD, DATABASE)

    # cursor method
    cursor = db.cursor()

    time_cursor = datetime.datetime.strptime(BEGIN, '%Y-%m-%d')
    time_delta = datetime.timedelta(int(1))
    time_lists = list()

    while time_cursor.strftime('%Y-%m-%d') <= END:
        sql = "SELECT node_id, name, value, created_at \
               FROM r324_data \
               WHERE created_at >= '{0}' AND \
                     created_at <= '{1}' \
			   ORDER BY created_at ASC".format(
            time_cursor.strftime('%Y-%m-%d 00:00:00'),
            time_cursor.strftime('%Y-%m-%d 23:59:59'))
        # cursor execute
        cursor.execute(sql)
        results = cursor.fetchall()
        filename = time_cursor.strftime('%Y-%m-%d')
        to_file(in_dir,filename, results)
        time_lists.append(filename)

        time_cursor += time_delta
    db.close()

    with open('{}/{}'.format(in_dir,"filename.list"), "w") as op:
        op.write("\n".join(time_lists))

def check(index, vector):
	# import pdb; pdb.set_trace()
	for i, v in enumerate(vector[:45]):
		if np.isnan(v):
			print 'missing value in line', index, ', attr ', i

def smooth(x):
	for i, line in enumerate(x):
		for i2, v2 in enumerate(line[:45]):
			if np.isnan(v2):
				print 'missing value in line', i, ', attr ', i2
				x[i][i2] = x[i-1][i2]


if __name__ == '__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('dir', type=str, help='the dir to save raw data')
	args = argparser.parse_args()
	args = vars(args)


	in_dir = args['dir']

	downLoad(in_dir)
	with open('{}/filename.list'.format(in_dir), 'r') as fp:
		filenames = fp.read().splitlines()

	with open('{}/filename.list'.format(in_dir), 'r') as fp:
		filenames = fp.read().splitlines()
	with open('{}/{}'.format(in_dir,'merge_'+BEGIN+'_to_'+END), 'w') as op:
		for file in filenames:
			x = np.genfromtxt('{}/{}'.format(in_dir,file), delimiter=',')
			smooth(x)
			x = x.astype('str')
			for line in x:
				print >> op, ", ".join(line)
	print 'Write "{}"'.format('merge_'+BEGIN+'_to_'+END)
