import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.datasets import imdb
from keras.preprocessing import sequence
import pandas as pd

"""
The task is character generation. 
Using the NLP model to generate the next character in a sequence of text. 
We are going to use it over and over again to generate an entire play. 

#Word Embeddings: a layer that we will add to our model

#LTSM longterm-shortterm memory

"""
# loading a text file
PATH = 'scripts.txt'

text = open(PATH, 'rb').read().decode(encoding='utf-8')

print('Length of text: {} characters'.format(len(text)))

print(text[:500])

# Ecoding
vocab = sorted(set(text))
# Creating a mapping unique characters to indices
char2idx = {u: i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)


def text_to_int(text):
    return np.array([char2idx[c] for c in text])


text_as_int = text_to_int(text)

print('Text:', text[:13])
print('Encoded:', text_to_int(text[:13]))

# create a function to convert numeric values to text


def int_to_text(ints):
    try:
        ints = ints.numpy()
    except:
        pass
    return ''.join(idx2char[ints])


print(int_to_text(text_as_int[:13]))

# create a training example input: Hell output: ello
# length of sequence for a training example
seq_length = 100
examples_per_epoch = len(text)//(seq_length+1)

# create training examples / targets
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)
# Use the batch method to turn this stream of chars into batches of desired length
sequences = char_dataset.batch(seq_length+1, drop_remainder=True)


def split_input_target(chunk):
    input_text = chunk[:-1]  # hell
    target_text = chunk[1:]  # ello
    return input_text, target_text


# Use map to apply the function to every entry
dataset = sequences.map(split_input_target)

for x, y in dataset.take(2):
    print("\n\nEXAMPLE\n")
    print("INPUT")
    print(int_to_text(x))
    print("\nOUTPUT")
    print(int_to_text(y))

BATCH_SIZE = 64
VOCAB_SIZE = len(vocab)
EMBEDDING_DIM = 256
RNN_UNITS = 1024

# buffer size to shuffle the dataset
# TF data is design to work with possibly infinite sequences,
# it maintains a buffer in which it shuffles elements

BUFFER_SIZE = 10000

data = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

# Building the Model
# Use embedding layer as LSTM
# Use one dense layer that contains a node  in our training data
# The dense layer will give us probability distribution over all nodes


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                  batch_input_shape=[batch_size, None]),
        tf.keras.layers.LSTM(rnn_units,
                             return_sequences=True,
                             stateful=True,
                             recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)

    ])
    return model


model = build_model(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, BATCH_SIZE)
model.summary()

# Creating a Loss Function

for input_example_batch, target_example_batch in data.take(1):
    # ask our model for a prediction on our first batch of training data
    example_batch_predicitons = model(input_example_batch)
    # print out the output shape
    print(example_batch_predicitons.shape,
          "# (batch_size, sequence_length, vocab_size)")

# we can see that the prediction is an array of 64 arrays, one for each entry in the batch
print(len(example_batch_predicitons))
print(example_batch_predicitons)

# Examine one prediction
pred = example_batch_predicitons[0]
print(len(pred))
print(pred)
# 2d aray of length 100
# where each interior array is the prediction for the next character at each step time

# prediction at the first timestep
time_pred = pred[0]
print(len(time_pred))
print(time_pred)

# to determine the predicted character we need to sample the output distribution
sampled_indices = tf.random.categorical(pred, num_samples=1)

# reshape array and convert all integers to numbers to see the actual characters
sampled_indices = np.reshape(sampled_indices, (1, -1))[0]
predicted_chars = int_to_text(sampled_indices)

# loss function


def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


# compile the model
model.compile(optimizer='adam', loss=loss)

# creating checkpoints
# Dir where all checkpoints are saved
checkpint_dir = './training_checkpoints'
# Name of the checkpoint file
checkpoint_prefix = os.path.join(checkpint_dir, "ckpt_{epoch}")

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True
)
# train the model
history = model.fit(data, epochs=40, callbacks=[checkpoint_callback])

# Loading the model
model = build_model(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)

# find the latest checkpoint that stores the models weights
model.load_weights(tf.train.latest_checkpoint(checkpint_dir))
model.build(tf.TensorShape([1, None]))

# Generating text Function


def generate_text(model, start_string):
    # number of characters to generate
    num_generate = 800
    # converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)
    # Empty string to store our results
    text_generated = []
    # Low temperatures results in more predictable text
    # Higher temperatures results in more surprising text
    # play with it to find the best setting
    temperature = 1.0

    # here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the character returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(
            predictions, num_samples=1)[-1, 0].numpy()

        # we pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id])
        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))


inp = input("Type a starting word: ")
print(generate_text(model, inp))
