# Parameter file


DEFAULT_ITEM_TYPE = ['PSScene4Band']
GEOJSON_DIRECTORY = 'geojson_cities/'
ACTIVATION_REQUEST = ['planet data download --activate-only --item-type PSScene3Band --asset-type analytic --string-in id ', ' --quiet']
TRIM_LEVEL = 5 # how many coordinate decimal points to use, this is approx 1m
NUMBER_OF_CHUNKS = 6
PRINT_LIM = 10
ASSET_TYPE = 'analytic'
DESIRED_ITEM_TYPE = "PSScene3Band"
NUM_TRIES = 15
CHUNK_DIR = "chunked_geojson/"
OUTPUT_DIR = "image_chunks/"