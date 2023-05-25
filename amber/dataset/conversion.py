from PIL import Image
from mcap.records import Message, Schema
from mcap_ros2.decoder import Decoder
from mcap_ros2._dynamic import DecodedMessage
from pyzstd import decompress
from amber.exception import ImageDecodingError
import numpy as np
import torch
import torchvision.transforms as transforms


def decompress_message(message: Message) -> Message:
    message.data = decompress(message.data)
    return message


def ros_message_to_image(ros_message: DecodedMessage) -> Image:
    match ros_message.encoding:
        case "rgb8":
            return Image.frombytes(
                "RGB", (ros_message.width, ros_message.height), ros_message.data
            )
        case "8UC3":
            image = Image.frombytes(
                "RGB", (ros_message.width, ros_message.height), ros_message.data
            )
            b, g, r = image.split()
            return Image.merge("RGB", (r, g, b))
        case _:
            raise ImageDecodingError(
                "image_encodings in sensor_msgs/msg/Image is "
                + ros_message.encoding
                + " , it was not supported yet."
            )


def image_to_tensor(image: Image) -> torch.Tensor:
    return transforms.Compose([transforms.PILToTensor()])(image)


def decode_image_message(
    message: Message, schema: Schema, decompress: bool
) -> torch.Tensor:
    decoder = Decoder()
    if decompress:
        ros_message = decoder.decode(schema, decompress_message(message))
    else:
        ros_message = decoder.decode(schema, message)
    return image_to_tensor(ros_message_to_image(ros_message))
