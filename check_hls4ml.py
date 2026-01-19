import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import hls4ml
import ndjson
import os

print("TensorFlow version:", tf.__version__)
print("hls4ml version:", hls4ml.__version__)

# -------------------------
# 1. Define tiny Keras model
# -------------------------
model = Sequential([
    Dense(4, input_shape=(4,), activation='relu', name="dense1"),
    Dense(1, activation='linear', name="output")
])

model.summary()

# -------------------------
# 2. Create hls4ml config
# -------------------------
config = hls4ml.utils.config_from_keras_model(
    model,
    granularity='model',
    backend='oneAPI'
)

# Keep build tiny & fast
config['Model']['Precision'] = 'ap_fixed<16,6>'
config['Model']['ReuseFactor'] = 1

# -------------------------
# 3. Convert to hls4ml model
# -------------------------
hls_model = hls4ml.converters.convert_from_keras_model(
    model,
    hls_config=config,
    backend='oneAPI',
    output_dir='hls4ml_oneapi_test'
)
print("HLS model created")

# -------------------------
# 4. Compile (Python-level)
# -------------------------
hls_model.compile()
print("HLS model compiled")

# -------------------------
# 5. Build (report only)
# -------------------------
hls_model.build(build_type='report')
print("HLS oneAPI report build completed successfully")

# -------------------------
# 6. Summarise report contents
# -------------------------
report_file = os.path.join(
    'hls4ml_oneapi_test',
    'build',
    'myproject.report.prj',
    'reports',
    'resources',
    'json',
    'summary.ndjson'
)

with open(report_file, "r") as f:
    summary = ndjson.load(f)

resource_names = list(filter(lambda x: x["name"] == "Estimated Resource Usage", summary))[0]['columns'][1:-1]
available = list(filter(lambda x: x["name"] == "Available", summary))[0]['data'][:-1]
estimated_resources = list(filter(lambda x: x["name"] == "Total", summary))[0]['data'][:-1]

print("~~~~~~~~~~~~~~ Resource usage ~~~~~~~~~~~~~~")
for i, resource in enumerate(resource_names):
    print(f"--> {resource}:")
    print(f"      * Available resource: {available[i]}")
    print(f"      * Used resource (estimated): {estimated_resources[i]}")
    print(f"      * Percentage of used resource (estimated): {100*float(estimated_resources[i])/float(available[i]):.2f}%")
