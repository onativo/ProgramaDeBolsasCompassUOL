#criando a ligação entre o tensorflow e sagemaker

import argparse
import json
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

if __name__ == "__main__":
    
    #trabalhar com linhas de comando para chamadas externas no py
    parser = argparse.ArgumentParser()
    
    #parametros relacionados à rene neural
    parser.add_argument('--epochs', type=int, default=2) #epocas de treino
    parser.add_argument('--learning-rate', type=float, default=0.001) #taxa de aprendizagem
    parser.add_argument('--batch-size', type=int, default=32) #batchsize
    parser.add_argument('--dropout', type=int) #
    
    #variaveis de ambiente
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAINING'))
    parser.add_argument('--model-dir', type=str)
    parser.add_argument('--sm-model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    
    args, _ = parser.parse_known_args()
    
    X_train = np.load(os.path.join(args.train, 'train_data.npy'))
    y_train = np.load(os.path.join(args.train, 'train_labels.npy'))
    X_test = np.load(os.path.join(args.train, 'eval_data.npy'))
    y_test = np.load(os.path.join(args.train, 'eval_labels.npy'))
    
    #pré processamento da base de dados
    #X_train = X_train.astype('float32')
    #X_test = X_test.astype('float32')
    #X_train = X_train / 255
    #X_test = X_test / 255
    
    #construção da rede neural
    rede_neural = Sequential()
    rede_neural.add(Dense(input_shape = (784, ), units = 397, activation = 'relu'))
    
    if args.dropout == 1:
        rede_neural.add(Dropout(0.2))
        
    rede_neural.add(Dense(units = 397, activation = 'relu'))
    if args.dropout == 1:
        rede_neural.add(Dropout(0.2))
        
    rede_neural.add(Dense(units = 10, activation = 'softmax'))
    rede_neural.compile(optimizer = Adam(learning_rate = args.learning_rate), loss = 'sparse_categorical_crossentropy', metrics = ['acc'])
    rede_neural.fit(X_train, y_train, batch_size = args.batch_size, epochs = args.epochs)
    score = rede_neural.evaluate(X_test, y_test)
    
    print('Loss: ', score[0])
    print('Accuracy: ', score[1])
    
    rede_neural.save(os.path.join(args.sm_model_dir, "000000001"))