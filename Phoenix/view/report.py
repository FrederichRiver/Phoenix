#!/usr/bin/python3

"""
{
    "title",
    "date",
    "total_asset",
    [
        "each_asset":{
            "volume",
            "value"
        }
    ]
    "cash",
    "debt",
    "leverage",
    "sharpe_ratio"
}
"""

class Report(object):
    def __init__(self, **kargs) -> None:
        self.param = kargs

    def toMarkdown(self):
        pass

    def toHTML(self):
        pass

    def toPDF(self):
        pass

class MARKDOWN(object):
    def __init__(self) -> None:
        pass

    def title1(self, title: str) -> str:
        return f"# {title}\n"

    def title2(self, title: str) -> str:
        return f"## {title}\n"

    def title3(self, title: str) -> str:
        return f"### {title}\n"

    def title4(self, title: str) -> str:
        return f"#### {title}\n"

    def ol(self, l: list):
        txt = ''
        for i in range(len(l)):
            txt += f"{i+1}. {l[i]}\n"
        return txt

    def ul(self, l: list):
        txt = ''
        for i in range(len(l)):
            txt += f"* {l[i]}\n"
        return txt