import io

from PIL import Image


class ImageProcessing:
    def __init__(self, file: bytes, resolution: tuple[int, int]):
        self.__src_file = file
        self.__resolution = resolution
        self.__file_format = self.__get_file_format()

    def get_metadata(self) -> dict:
        """Получение метаданных файла."""

        converted_file = self.get_converted_file()
        metadata = dict(
            resolution=self.__resolution,
            format=self.__file_format,
            size=self.__get_size(converted_file),
        )
        return metadata

    def get_converted_file(self) -> bytes:
        """Получение преобразованного изображения в бинарном виде."""

        file_change_resolution = self.__change_resolution(self.__src_file)
        file_convert_grayscale = self.__converting_image_to_grayscale(
            file_change_resolution
        )
        return file_convert_grayscale

    def __get_file_format(self) -> str:
        """Получение формата файла."""

        image = Image.open(io.BytesIO(self.__src_file))
        file_format = image.format
        return file_format

    def __converting_image_object_to_bytes(self, image: Image) -> bytes:
        """Преобразование объекта Image в биты."""

        output_buffer = io.BytesIO()
        image.save(output_buffer, format=self.__file_format)
        binary_file = output_buffer.getvalue()
        return binary_file

    def __change_resolution(self, file: bytes) -> bytes:
        """Изменение разрешения изображения."""

        image = Image.open(io.BytesIO(file))
        image = image.resize(self.__resolution)
        new_binary_file = self.__converting_image_object_to_bytes(image)
        return new_binary_file

    def __converting_image_to_grayscale(self, file: bytes) -> bytes:
        """Преобразование изображения в оттенки серого."""

        image = Image.open(io.BytesIO(file))
        image = image.convert("L")
        new_binary_file = self.__converting_image_object_to_bytes(image)
        return new_binary_file

    @staticmethod
    def __get_size(file: bytes) -> int:
        """Получение размера изображения в байтах."""

        size = len(file)
        return size
