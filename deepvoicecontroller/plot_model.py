from keras.utils import plot_model
from model import Model
model = Model()
plot_model(model.model, to_file="model.png", show_shapes = True, show_layer_names = False)
