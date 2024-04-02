import cv2
import picamera
import numpy as np
from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def capture_image():
    # Instrctor note: this can be directly taken from the PiCamera documentation
    # Create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.capture(stream, format='jpeg')
        
    # Construct a numpy array from the stream
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    
    # "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)
    
    # OpenCV returns an array with data in BGR order. 
    # The following code invert the order of the last dimension.
    image = image[:, :, ::-1]
    return image


################################################



def detect_and_crop(mtcnn, image):
    detection = mtcnn.detect_faces(image)[0]
    #TODO
    box = detection["box"]
    start_x = box[0]
    start_y = box[1]
    width = box[2]
    height = box[3]

    start_x = start_x = start_x - 0.1 * width if (start_x - 0.1 * width > 0) else 0
    start_y = start_y = start_y - 0.1 * height if (start_y - 0.1 * height > 0) else 0

    width = width * 1.2
    height = height * 1.2
 

    # according to the shape of center crop picture, we choose from the original array.
    cropped_image = image[start_y: start_y + height, start_x: start_x + width]
    bounding_box = [start_x, start_y, width, height]
    show_bounding_box(image, bounding_box)

    # print('shape of new image',image_newarray.shape)
    # plt.title('Center-Crop')
    # plt.axis('off')
    # plt.imshow(cropper_image)
    
    return cropped_image, (start_x, start_y, width, height)



def show_bounding_box(image, bounding_box):
    x1, y1, w, h = bounding_box
    fig, ax = plt.subplots(1,1)
    ax.imshow(image)
    ax.add_patch(Rectangle((x1, y1), w, h, linewidth=1, edgecolor='r', facecolor='none'))
    plt.show()
    return

def pre_process(face, required_size=(160, 160)):
    ret = cv2.resize(face, required_size)
    ret = ret.astype('float32')
    mean, std = ret.mean(), ret.std()
    ret = (ret - mean) / std
    return ret


def run_model(model, face):
# students will need to fill in the following function
    #TODO


    # Load the TFLite model and allocate tensors.


    # Get input and output tensors.
    input_details = model.get_input_details()
    output_details = model.get_output_details()

    # Test the model on random input data.
    input_shape = input_details[0]['shape']
    input_data = face.reshape(input_shape)
    model.set_tensor(input_details[0]['index'], input_data)

    model.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data = model.get_tensor(output_details[0]['index'])
   
    return output_data






### verification ###


mtcnn = MTCNN()
image = capture_image()
cropped_image = detect_and_crop(mtcnn, image)


tfl_file = "inception_model.tflite"
interpreter = tf.lite.Interpreter(model_path=tfl_file)
interpreter.allocate_tensors()