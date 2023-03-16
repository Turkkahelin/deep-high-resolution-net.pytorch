import queue
import pathlib

from torch.utils.data import Dataset, IterableDataset
import torchvision.transforms
import torchvision.transforms.functional as TF

from PIL import Image

class CustomDataset(Dataset):
    """Custom Dataset for handling single images and videos.

    Custom torch.utils.data.Dataset class for handling single images and videos
    and creating Dataset objects from them.
    """
    def __init__(self, path: str, transform: torchvision.transforms = None) -> None:
        """Initializes CustomDataset

        Args:
            path (str): Path to the image or video
            transform (torchvision.transforms, optional):
                Transfrom that's used for transforming the images to tensors.
                Defaults to None.
        """
        super().__init__()
        self.path = path
        self.transform = transform
        self.queue = self.__load_data(self.path)


    def __load_data(self, path: str) -> queue.Queue:
        """Loads the data from the path. Data can be image or video.
        TODO: Implement video support.

        Args:
            path (str): Path to the image or video

        Returns:
            queue.Queue: Queue which has the images loaded
        """
        buffer = queue.Queue()
        file_extension = pathlib.Path(path).suffix
        if file_extension == ".jpg" or file_extension == ".png":
            image = Image.open(path)
            #buffer.put(TF.to_tensor(image))
            buffer.put(image)
        return buffer

    def __read_next_image(self):
        while self.queue.qsize() > 0:
            image = self.queue.get()
            if self.transform is not None:
                image = self.transform(image)
            yield image

        return None

    def __iter__(self):
        return self.__read_next_image()

    def __len__(self):
        return self.queue.qsize()

    def __getitem__(self, x):
        image = self.queue.get()
        if self.transform is not None:
            image = self.transform(image)

        return image, None
