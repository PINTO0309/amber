from amber.dataset.images_dataset import ImagesDataset
from amber.dataset.conversion import image_to_tensor
from torch.utils.data import DataLoader
import torch
import tests
import os
from PIL import Image
from pathlib import Path


def test_read_image_vrx() -> None:
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    dataset = ImagesDataset(
        str(current_path / "rosbag" / "vrx" / "vrx.mcap"),
        str(current_path / "read_image_vrx.yaml"),
    )
    assert len(dataset) == 2
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)
    count = 0
    for i_batch, sample_batched in enumerate(dataloader):
        for sample in sample_batched:
            image = str(count) + ".png"
            assert torch.equal(
                sample,
                image_to_tensor(
                    Image.open(
                        str(current_path / "images" / "vrx" / image),
                    )
                ),
            )
            count = count + 1


def test_read_image_ford() -> None:
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    dataset = ImagesDataset(
        str(current_path / "rosbag" / "ford" / "ford.mcap"),
        str(current_path / "read_image_ford.yaml"),
    )
    assert len(dataset) == 39
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)
    count = 0
    for i_batch, sample_batched in enumerate(dataloader):
        for sample in sample_batched:
            image = str(count) + ".png"
            assert torch.equal(
                sample,
                image_to_tensor(
                    Image.open(
                        str(current_path / "images" / "ford" / image),
                    )
                ),
            )
            count = count + 1
