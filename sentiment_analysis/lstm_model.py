"""
Team 28
Ruihan Zhang 865529
Linrong Chen 854645
Ming Yin 816159
Hongyun Ma 805266
Jinge Zhang 769474
"""


import tensorflow as tf
import numpy as np

class LSTM:
    def __init__(self, sess):
        saver = tf.train.import_meta_graph("model/lstm.meta", clear_devices=True)
        saver.restore(sess, "model/lstm")
        print("model loaded")

        input_collection = tf.get_collection("inference_input")
        self.x, self.mask, self.keep_prob = input_collection

        self.softmax = tf.get_collection("softmax")[0]

    def predict(self, seq, mask, sess):
        seq = np.array(seq)
        seq_in = np.reshape(seq, [1]+list(seq.shape))
        mask = np.array([0, mask])
        mask_in = np.reshape(mask, [1]+list(mask.shape))

        feed_dict={self.x:seq_in, self.mask:mask_in, self.keep_prob:1}
        prob = sess.run(self.softmax, feed_dict=feed_dict)
        prob = np.reshape(prob,2)

        return prob

if __name__=="__main__":
    with tf.Session() as sess:
        model = LSTM(sess)
        print(model.predict(np.ones(30), 5, sess))
