from enum import Enum
from collections import namedtuple
from pathlib import Path
from typing import Iterator, Generator
import rlwrapper
import exam


class ItemLevel(Enum):
    """top level text
       top level image
           sub level text
           sub level image

           sub level test

       top level image
           sub level text

           sub level image
    """

    top = 0
    sub = 1


Item = namedtuple("Item", ["item_level", "text", "image"])


class SerializeExam:
    """Serialize questions, made of text and image, and
    answers, made of text and image.
    """

    def __init__(self, exam_alike: exam.Exam):
        self._exam: exam.Exam = exam_alike

    def assignment(self) -> Generator[Item, None, None]:
        for question in self._exam.questions:
            yield Item(ItemLevel.top, question.text, question.image)
            for answer in question.answers:
                yield Item(ItemLevel.sub, answer.text, answer.image)

    def correction(self) -> Generator[Item, None, None]:
        if self._exam.questions != ():
            yield Item(ItemLevel.top, f"correction", Path("."))
        for question in self._exam.questions:
            yield Item(ItemLevel.sub, f"{question.correct_letter}", Path("."))


class RLInterface:
    def __init__(self, input_generator: Iterator[Item], output_file: Path, **kwargs):
        """This class print a two nesting level series of items in pdf.
        """
        file_name: Path = kwargs.get("destination", Path(".")) / output_file
        self._input = input_generator
        sub_item_bullet_type: str = kwargs.get("sub_item_bullet_type", "A")
        top_item_bullet_type: str = kwargs.get("top_item_bullet_type", "1")
        page_heading: str = kwargs.get("heading", "")
        page_footer: str = kwargs.get("footer", "")
        self._doc = rlwrapper.PDFDoc(
            file_name,
            top_item_bullet_type=top_item_bullet_type,
            sub_item_bullet_type=sub_item_bullet_type,
            page_heading=page_heading,
            page_footer=page_footer
        )

    def build(self) -> None:
        try:
            item = next(self._input)
            assert item.item_level == ItemLevel.top
            self._doc.add_item(item)
            while True:
                item = next(self._input)
                if item.item_level == ItemLevel.top:
                    self._doc.add_item(item)
                elif item.item_level == ItemLevel.sub:
                    self._doc.add_sub_item(item)
                else:
                    raise ValueError
        except StopIteration:
            self._doc.build()
