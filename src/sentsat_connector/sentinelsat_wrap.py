from sys import platform
from pandas.core.frame import DataFrame
from sentinelsat import SentinelAPI
from sentinelsat import exceptions
from datetime import date
import pandas as pd
import time

from sentinelsat.exceptions import LTAError

class Sentinel:
    """SentinelSat wrapper class"""   

    def __init__(self, user: str, passwd: str) -> None:
        self.api = SentinelAPI(user, passwd, api_url="https://scihub.copernicus.eu/dhus/")


    def find_data(self, start: date, end: date, cloud: int, tiles: list[str], platformname: str = 'Sentinel-2') -> DataFrame:
        products = {}

        for tile in tiles:
            tile_products = self.api.query(identifier='*_T{}_*'.format(tile),
                                        platformname=platformname,
                                        date=[start, end],
                                        processinglevel='Level-2A',
                                        cloudcoverpercentage=(0, cloud))
            print('Tile - {}. Images found: {}'.format(tile, len(tile_products)))
            products.update(tile_products)
        return self.api.to_dataframe(products)

    
    def to_csv(self, products_df: DataFrame, output_file: str):
        products_df['complete'] = False
        products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
        products_df_sorted.to_csv(output_file)

    
    def read_csv(self, csv_file: str) -> DataFrame:
        return pd.read_csv(csv_file, index_col=0)


    def __initiate_download___(self, product_id: str, dir: str) -> bool:
        try:
            is_online = self.api.is_online(product_id)

            if is_online:
                print('Product {} is online. Starting download.'.format(product_id))
                self.api.download(product_id, directory_path=dir)
                return True
            else:
                print('Product {} is offline. Triggering retrieval.'.format(product_id))
                self.api.trigger_offline_retrieval(product_id)
                time.sleep(10)
        except exceptions.InvalidChecksumError as e:
            print("Invalid checksum detected, skipping.")
        except exceptions.ServerError as e:
            print("Server error, skipping.")
        except exceptions.LTAError as e:
            print("LTA error received. Timeout 1000 seconds")
            time.sleep(10)
        except exceptions.SentinelAPIError as e:
            print(e)
            print("Timeout 1000 seconds.")
            time.sleep(10)
        return False




    def download(self, products_df: DataFrame, data_file: str, dir: str): 
        while not products_df[products_df['complete']==False].empty:
            products_id = products_df.index.tolist()
            for product_id in products_id:
                self.__initiate_download___(product_id, dir)
            
            print('After last iteration, products complete: {}'.format(len(products_df['complete']==True)))
        print('All products have been downloaded.')

