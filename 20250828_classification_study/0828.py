import tensorflow as tf
from tensorflow.keras import layers, models


train = tf.keras.utils.image_dataset_from_directory(
    "data/train",      
    validation_split=0.2,  
    subset="training",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

val = tf.keras.utils.image_dataset_from_directory(
    "data/train",      
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

test = tf.keras.utils.image_dataset_from_directory(
    "data/test",       
    image_size=(224, 224),
    batch_size=32
)

normalization_layer = layers.Rescaling(1./255)
train_ds = train.map(lambda x, y: (normalization_layer(x), y))
val_ds   = val.map(lambda x, y: (normalization_layer(x), y))
test_ds  = test.map(lambda x, y: (normalization_layer(x), y))

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224,224,3)),
    layers.MaxPooling2D((2, 2,)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.ConvD(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


history = model.fit(
    train,
    validation_data=val,
    epochs=10   
)

test_loss, test_acc = model.evaluate(test)
print(f"Test accuracy: {test_acc:.2f}")
