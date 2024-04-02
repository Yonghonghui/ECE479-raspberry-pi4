
import tflite_runtime.interpreter as tflite
import numpy as np
import time
#step 1
# interpreter = tflite.Interpreter(model_path = "/home/cyhh/mp2/lab2_sp24/Dynamic_range_Quant_model.tflite")
interpreter = tflite.Interpreter(model_path = "/home/cyhh/mp2/lab2_sp24/Dynamic_range_Quant_model.tflite", experimental_delegates = [tflite.load_delegate('libedgetpu.so.1')])
interpreter.allocate_tensors()

#step2

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_details = interpreter.get_input_details()
input_shape = (20,28,28,1)
interpreter.resize_tensor_input(input_details[0]["index"], input_shape)
interpreter.allocate_tensors()

#load test image
test_images = np.load('/home/cyhh/mp2/lab2_sp24/test_images.npy')
test_labels = np.load('/home/cyhh/mp2/lab2_sp24/test_labels.npy')

#step 3

#print(test_images.shape)
num_prediction = 0
correct_prediction = 0
count = 0
total_time = 0
# print(test_images.shape)
batch_size = 20  # Define batch size

for i in range(0, len(test_images), batch_size):
    batch_images = test_images[i:i+batch_size]  # Get batch of images
    batch_labels = test_labels[i:i+batch_size]  # Corresponding batch of labels

    input_shape = input_details[0]['shape']
    input_data = np.array(batch_images, dtype=np.float32).reshape((batch_size, 28, 28, 1))  # Reshape batch
    interpreter.set_tensor(input_details[0]["index"], input_data)

    start_time = time.time()
    interpreter.invoke()
    end_time = time.time()
    inference_time = end_time - start_time
    total_time += inference_time

    output_data = interpreter.get_tensor(output_details[0]['index'])

    for output, groundtruth_label in zip(output_data, batch_labels):
        predicted_label = np.argmax(output)
        correct_prediction += 1 if predicted_label == groundtruth_label else 0
        num_prediction += 1

    

print("overal accuracy: {:.2f}%".format(correct_prediction/num_prediction * 100))
print("inference time: {:.32f}ms".format(total_time*1000))

