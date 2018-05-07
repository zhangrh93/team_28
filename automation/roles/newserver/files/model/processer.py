import json
import numpy as np
import regex as re

class Processer:
    # processer turns a piece of text into sequence
    def __init__(self):
        with open("word_dict.json","r",encoding="utf-8") as f:
            self.word_dict = json.load(f)

    def process(self, text):
        eyes = r"[8:=;]"
        nose = r"['`\-]?"
        max_length = 30
        FLAGS = re.MULTILINE | re.DOTALL
        # define some helper functions
        def hashtag(text):
            text = text.group()
            hashtag_body = text[1:]
            if hashtag_body.isupper():
                result = " {} ".format(hashtag_body.lower())
            else:
                result = " ".join(["<hashtag>"] + re.split(r"(?=[A-Z])", hashtag_body, flags=FLAGS))
            return result

        def allcaps(text):
            text = text.group()
            return text.lower() + " <allcaps> "

        def re_sub(pattern, repl):
            return re.sub(pattern, repl, text, flags=FLAGS)

        text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", " <url> ")
        text = re_sub(r"@\w+", " <user> ")
        text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), " <smile> ")
        text = re_sub(r"{}{}p+".format(eyes, nose), " <lolface> ")
        text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), " <sadface> ")
        text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), " <neutralface> ")
        text = re_sub(r"/"," / ")
        text = re_sub(r"<3"," <heart> ")
        text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", " <number> ")
        text = re_sub(r"#\S+", hashtag)
        text = re_sub(r"([!?.]){2,}", r"\1 <repeat> ")
        text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 <elong> ")
        text = re_sub(r"!"," ! ")
        text = re_sub(r"\?"," ? ")
        text = re_sub(r":"," : ")
        text = re_sub(r"\."," . ")
        text = re_sub(r","," , ")
        text = re_sub(r";"," ; ")
        text = re_sub(r"-"," - ")
        text = re_sub(r"\""," \" ")
        text = re_sub(r"\*"," \* ")
        text = re_sub(r"…"," … ")
        text = re_sub(r"&lt"," < ")
        text = re_sub(r"&gt"," < ")
        text = re_sub(r"&amp"," & ")
        text = re_sub(r"([A-Z]){2,}", allcaps)

        text = text.lower()

        mapping = np.zeros(max_length)
        tokens = text.split()
        r = max_length if len(tokens) > max_length else len(tokens)
        mask = r-1
        for i in range(r):
            mapping[i] = self.word_dict.get(tokens[i], len(self.word_dict)-1)

        return mapping, mask

if __name__=="__main__":
    p = Processer()
    print(p.process("i am #666 into 8("))
