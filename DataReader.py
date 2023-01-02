import pandas as pd
import scipy.sparse as sps
import numpy as np
from pandas import Series


class DataReader(object):

    def __init__(self, urm_path, icm_type_path, icm_length_path):
        self.urm_df = pd.read_csv(urm_path, dtype={'Impressions': 'str'})
        self.icm_type_df = pd.read_csv(icm_type_path)
        self.icm_length_df = pd.read_csv(icm_length_path)

        self.num_users = len(self.urm_df["UserID"].unique())

        urm_items = self.urm_df['ItemID'].unique()
        icm_items = self.icm_length_df['item_id']
        self.cold_items = [item for item in icm_items if item not in urm_items]
        self.num_items = len(urm_items) + len(self.cold_items)

    def load_urm_sps(self):
        urm_all = sps.coo_matrix((np.ones(len(self.urm_df["UserID"].values)),
                                  (self.urm_df["UserID"].values, self.urm_df["ItemID"].values)),
                                 shape=(self.num_users, self.num_items), dtype='d')

        return urm_all

    def load_icm_type(self):
        mapped_type_id, original_type_id = pd.factorize(np.sort(self.icm_type_df["feature_id"].unique()))
        type_original_id_to_index = pd.Series(mapped_type_id, index=original_type_id)
        self.icm_type_df["mapped_type"] = self.icm_type_df["feature_id"].map(type_original_id_to_index)
        icm_type = sps.csr_matrix((np.ones(len(self.icm_type_df["item_id"].values)),
                                   (self.icm_type_df["item_id"].values, self.icm_type_df["mapped_type"].values)))

        return icm_type

    def load_icm_length(self):
        data = self.icm_length_df["data"].values
        row = self.icm_length_df["item_id"].values
        col = np.zeros(len(self.icm_length_df["data"].values), dtype=int)
        icm_length = sps.coo_matrix((data, (row, col)))
        return icm_length
