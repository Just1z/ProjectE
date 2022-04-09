import io
from typing import Literal
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup


def get_markup(path="./example/text.html"):
    html_file = open(path, encoding="utf-8")
    html_markup = html_file.read()
    html_file.close()
    return html_markup


class HtmlParser:
    def __init__(self, html_markup):
        self.soup = BeautifulSoup(html_markup, "lxml")

    def get_tables(self):
        parsed_tables = []
        for tag_table in self.soup.find_all("table"):
            parsed_table = []
            tag_tbody = tag_table.find("tbody")
            rows = tag_tbody.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols = [element.text.strip() for element in cols]
                parsed_table.append([element for element in cols if element])
            parsed_tables.append(parsed_table)
        return parsed_tables

    def get_images(self):
        from requests import get
        binary_images = []
        for tag_img in self.soup.find_all("img"):
            url = tag_img.get("src")
            bytesio = io.BytesIO(get(url).content)
            binary_images.append(bytesio)
        return binary_images

    def get_title(self):
        tag_h1 = self.soup.find("h1")
        return tag_h1.text.strip()

    def get_condition(self, divider="\n"):
        task_condition_parts = []
        for tag_h3 in self.soup.find_all("h3"):
            task_condition_parts.append(tag_h3.text.strip())
        return divider.join(task_condition_parts)

    def get_content(self, order=None):
        if order is None:
            order = ["title", "condition", "tables", "images"]
        content = {element: None for element in order}
        content["title"] = self.get_title()
        content["condition"] = self.get_condition()
        content["tables"] = self.get_tables()
        content["images"] = self.get_images()
        return content


class Content2Image:
    font_path = "./static/fonts/Cousine-Regular.ttf"
    text_color = (0, 0, 0, 255)
    table_color = (0, 0, 0, 255)
    background = (0, 0, 0, 0)

    def __init__(self, content: dict, fixed_width=1000, indent_coef=0.01, spacing_coef=0.003):
        """
        :param content:
        :param fixed_width: ширина изображения, высота вычисляется в зависимости от объема контента и fixed_width
        :param indent_coef: коэффициент расчета расстояния между частями задания (заголовком, условием, таблицами и т.п.)
        :param spacing_coef: коэффициент расчета расстояние между строчками текста
        """
        self.content = content
        self.width = fixed_width
        self.heading_fontsize = fixed_width // 40
        self.content_fontsize = int(fixed_width / 62.5)
        self.indent = int(fixed_width * indent_coef)
        self.spacing = int(fixed_width * spacing_coef)

    def draw_title(self, xy: tuple[int, int] | None = None,
                   anchor="lm",
                   align: Literal["left", "right", "center"] = "left"):
        if not self.content["title"]:
            return Image.new("RGBA", (self.width, 0), (0, 0, 0, 0))
        line_length = int((1600 / self.heading_fontsize) * (self.width / 1000))
        text_container = self.content["title"].split("\n")
        for i in range(len(text_container)):
            line = text_container[i]
            transfers = len(line) // line_length
            j = 0
            for transfer in range(transfers):
                line = line[:line_length * (j + 1) + j] + "\n" + line[line_length * (j + 1) + j:]
                j += 1
            text_container[i] = line
        text = "\n".join(text_container)

        height = self.indent + (self.heading_fontsize + self.spacing) * (text.count("\n") + 1)
        if xy is None and anchor != "lm":
            xy = (0, 0)
        elif xy is None and anchor == "lm":
            xy = (0, height // 2)
        font = ImageFont.truetype(self.font_path, self.heading_fontsize, encoding="UTF-8")
        image = Image.new("RGBA", (self.width, height), self.background)
        drawer = ImageDraw.Draw(image)
        drawer.text(xy, text, self.text_color, font, anchor, self.spacing, align)
        return image

    def draw_condition(self, xy: tuple[int, int] | None = None,
                       anchor="lm",
                       align: Literal["left", "right", "center"] = "left"):
        if not self.content["condition"]:
            return Image.new("RGBA", (self.width, 0), (0, 0, 0, 0))
        line_length = int((1600 / self.content_fontsize) * (self.width / 1000))
        text_container = self.content["condition"].split("\n")
        for i in range(len(text_container)):
            line = text_container[i]
            transfers = len(line) // line_length
            j = 0
            for transfer in range(transfers):
                line = line[:line_length * (j + 1) + j] + "\n" + line[line_length * (j + 1) + j:]
                j += 1
            text_container[i] = line
        text = "\n".join(text_container)

        height = self.indent + (self.content_fontsize + self.spacing) * (text.count("\n") + 1)
        if xy is None and anchor != "lm":
            xy = (0, 0)
        elif xy is None and anchor == "lm":
            xy = (0, height // 2)
        font = ImageFont.truetype(self.font_path, self.content_fontsize, encoding="UTF-8")
        image = Image.new("RGBA", (self.width, height), self.background)
        drawer = ImageDraw.Draw(image)
        drawer.text(xy, text, self.text_color, font, anchor, self.spacing, align)
        return image

    def draw_images(self, image_scale=0.5):
        if not self.content["images"]:
            return Image.new("RGBA", (self.width, 0), (0, 0, 0, 0))
        images = [Image.open(binary) for binary in self.content["images"]]
        for image in images:
            image.thumbnail((self.width, image.size[1]))
        height = 2 * self.indent + self.spacing * (len(images) - 1) + sum(image.size[1] for image in images)
        result = Image.new("RGBA", (self.width, height), self.background)
        indent = Image.new("RGBA", (self.width, self.indent), self.background)
        spacing = Image.new("RGBA", (self.width, self.spacing), self.background)
        bottom = 0
        result.paste(indent, (0, 0))
        bottom += indent.size[1]
        result.paste(images[0], (0, bottom))
        bottom += images[0].size[1]
        result.paste(spacing, (0, bottom))
        bottom += spacing.size[1]
        for i, image in enumerate(images[1:], 1):
            result.paste(image, (0, bottom))
            bottom += image.size[1]
            result.paste(spacing, (0, bottom))
            bottom += spacing.size[1]
        result.paste(indent, (0, bottom))
        w, h = result.size
        w, h = int(w * image_scale), int(h * image_scale)
        result.thumbnail((w, h))
        return result

    def draw_content(self, image_scale=0.5):  # TODO: order
        title = self.draw_title()
        condition = self.draw_condition()
        images = self.draw_images(image_scale)

        height = sum(image.size[1] for image in [title, condition, images])
        content = Image.new("RGBA", (self.width, height), self.background)
        bottom = 0
        content.paste(title, (0, bottom))
        bottom += title.size[1]
        content.paste(condition, (0, bottom))
        bottom += condition.size[1]
        content.paste(images, ((self.width - images.size[0]) // 2, bottom))
        return content


def auto(path="./example/empty_or_incorrect.html"):
    try:
        markup = get_markup(path)
        parser = HtmlParser(markup)
        content = parser.get_content()
        content2image = Content2Image(content, fixed_width=1000, indent_coef=0.01, spacing_coef=0.003)
        # при таком значении проводил все расчеты, поэтому лучше оставить fixed_width=1000
        # если нужен другой размер, то либо поменять fixed_width, либо использовать resize или thumbnail в pillow
        content2image.font_path = "./static/fonts/Cousine-Regular.ttf"  # по умолчанию
        content2image.text_color = (0, 0, 0, 255)  # по умолчанию
        content2image.table_color = (0, 0, 0, 255)  # по умолчанию
        content2image.background = (0, 0, 0, 0)  # по умолчанию
    except Exception:
        return Image.new("RGB", (100, 100), (255, 0, 0))

    return content2image.draw_content(image_scale=0.3)


if __name__ == "__main__":
    auto().show()
