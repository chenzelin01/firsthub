# -*- coding:utf-8 -*-
import gensim
import jieba
import os
from time import time
import re
if __name__ == '__main__':
    pattern = re.compile("[\S]*(\s)*[\S]*")
    # this option is only can used in linux environment
    # jieba.enable_parallel(2)
    with open('corpus_small.txt', 'r', encoding='utf-8') as f:
        t1 = time()
        txt = f.read()
        txt = txt.replace("<content>", " ")
        txt = txt.replace("</content>", " ")
        print(txt)
        with open('result.txt', 'w', encoding='utf-8') as result_f:
            result = jieba.cut(txt, cut_all=True)
            print("time using: ", time() - t1)
            # print("Full mode: ", "/".join(result))
            result_txt = " ".join(result)
            # for word in result:
            #     if re.match(pattern, word)[1] is None and len(word) > 0:
            result_f.write(result_txt)
            #         print(word)
        # model = gensim.models.Word2Vec(result_txt)
        # model.save('model')
        model = gensim.models.Word2Vec.load('model')
        sim = model.similarity("水", "林")
        print(sim)
        print("time using: ", time() - t1)
