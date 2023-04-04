from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest, DataCollection, MosaickingOrder
import matplotlib.pyplot as plt
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

config = SHConfig()
config.sh_client_id=os.getenv("CLIENT_ID")
config.sh_client_secret=os.getenv("CLIENT_SECRET")

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2022, 12, 31)
n_chunks = 13
tdelta = (end - start) / n_chunks
edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
slots = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

evalscript = """
//VERSION=3

function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: { bands: 3 }
  };
}

function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
"""
bbox = BBox(bbox=[37.415937, 47.027546, 37.77579, 47.214904], crs=CRS.WGS84)

def get_true_color_request(time_interval):
    return SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=time_interval,
                other_args={"dataFilter": {"maxCloudCoverage": 5},"processing": {"harmonizeValues": True}}
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.JPG)],
        bbox=bbox,
        size=[2500, 1909.537],
        config=config,
    )

list_of_requests = [get_true_color_request(slot) for slot in slots]


for i,request in enumerate(list_of_requests):
    # print(request)
    image = request.get_data()
    print(slots[i])
    plt.imshow(image[0])
    plt.show()




# plt.imshow(image)
# plt.show()

