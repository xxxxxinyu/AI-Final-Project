from tensorflow.keras.layers import *
from tensorflow.keras.models import Model, Sequential
import visualkeras

model = Sequential([
    Conv2D(64, 3, activation='relu', input_shape=(128,128,1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(32, 3, activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    
    Dense(3, activation='softmax')
])

visualkeras.layered_view(model, legend=True, to_file='architecture.png')