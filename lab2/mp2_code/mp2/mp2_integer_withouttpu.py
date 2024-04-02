
import tflite_runtime.interpreter as tflite
#from pycoral.utils.edgetpu import make_interpreter
import numpy as np
import time
#step 1
interpreter = tflite.Interpreter(model_path = "/home/cyhh/mp2/lab2_sp24/full_int_Quant_model.tflite")
# interpreter = tflite.Interpreter(model_path = "/home/cyhh/mp2/lab2_sp24/full_int_Quant_model.tflite", experimental_delegates = [tflite.load_delegate('libedgetpu.so.1')])
interpreter.allocate_tensors()

#step2

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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
for input_images, groundtruth_label in zip(test_images, test_labels):
    
#     count += 1
#     if(count>50):
#         break
#     print('1')
    input_shape = input_details[0]['shape']
    input_data = input_images.astype(np.float32).reshape((1,28,28,1))
    interpreter.set_tensor(input_details[0]["index"],input_data)
    start_time = time.time()
    interpreter.invoke()
    end_time = time.time()
    inference_time = end_time - start_time
    output_data = interpreter.get_tensor(output_details[0]['index'])

    total_time += inference_time
    
    
    predicted_label = np.argmax(output_data, axis =1)
    correct_prediction += np.sum(predicted_label == groundtruth_label)
    num_prediction += 1
    

print("overal accuracy: {:.2f}%".format(correct_prediction/num_prediction * 100))
print("inference time: {:.32f}ms".format(total_time*1000))

