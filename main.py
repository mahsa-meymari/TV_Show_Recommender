from DataReader import DataReader

reader = DataReader(
    urm_path = 'Data/interactions_and_impressions.csv',
    icm_type_path='Data/data_ICM_type.csv',
    icm_length_path='Data/data_ICM_length.csv')
print('{:.2f} percent of items have no interaction with our items'.format(len(reader.cold_items)/ reader.num_items*100))
URM = reader.load_urm_sps()
ICM_type = reader.load_icm_type
ICM_length = reader.load_icm_length()