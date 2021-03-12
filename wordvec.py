import re
import linecache
import jieba
import gensim
import pandas as pd
def sim_comp(word_list,sentence):#每个都要计算相似度，要改
    wdlist=[]
    #wdsim=[]
    index=0
    for word in word_list:
        wd_ind=sentence.find(word)
        if (wd_ind+1)!=0:
            wdlist.append(word)
            #print(word)
            word_list=word_list[index:len(word_list)]
            index=-1
        index+=1
    #print(wdlist)
    if len(wdlist)==0:
        return 0
    #wdlist=sorted(wdlist, key=lambda k: k[1],reverse=True)
    return wdlist


class Data_preview:#excel 乱码
    def __init__(self,path,batch_size):
        self.count=0
        self.path=path
        self.list=[]
        self.stop_words_list=[]
        self.batch_size=batch_size
        self.stopwordlist_preview()
        #self.columns_add()
        #self.word_2_vec_model()
        #self.model_test()
        self.sen_vec()
    def stopwordlist_preview(self):
        stop = pd.read_csv('cn_stopwords.txt',
                           encoding='utf-8',
                           header=None,
                           sep='\n',
                           engine='python',
                           quoting=3)
        stop = [' ', ''] + list(stop[0])
        self.stop_words_list=stop
        #print(self.stop_words_list)
    def word_2_vec_model(self):
        with open(self.path,
              'r',
                  encoding='Utf-8') as f:
            text = 'leedvan'
            i=0
            #r1='[a-zA-Z0-9]+'
            cut_text=[]
            last_line=0
            first_time=True
            get_line=lambda file,nums_line:linecache.getline(file, nums_line).strip()
            while i<=self.batch_size and f.readline():
                #print(self.list)
                if i==self.batch_size:#没执行
                    self.list.append(cut_text)#文件尾
                    if first_time==True:
                        print(1)
                        self.model_training(first_=True)
                        first_time = False
                    else:
                        self.model_training()
                        i-=1
                    last_line+=i  #继承上一次的读取位置
                    i=0
                    cut_text=[]
                    self.list=[]

                i=i+1
                text=get_line(self.path,last_line+i)
                words=jieba.cut(text)
                for word in words:
                    if word not in self.stop_words_list and not re.match('[0-9a-zA-Z]',word):
                        #if word not in stop_word_list1 and not re.match('[0-9a-zA-Z]',word):
                        cut_text.append(word)

            self.model_training(flag=1)

    def model_training(self,flag=0,first_=False):
        if first_ and len(self.list):
            model = gensim.models.Word2Vec(self.list,
                                       sg=1,
                                       size=50,
                                       window=5,
                                       min_count=2,
                                       negative=3,
                                       sample=0.001,
                                       hs=1,
                                       workers=4,

                                       )
            print(first_)
            model.save('emotion_vocabulary')
        elif len(self.list) and flag==0:
            model=gensim.models.Word2Vec.load("emotion_vocabulary")
            model.build_vocab(sentences=self.list, update=True)
            model.train(sentences=self.list, total_examples=model.corpus_count, epochs=model.iter)
            model.save('emotion_vocabulary')
            self.count+=1
            print("追加训练 ",self.count)
        elif flag==1:
            model = gensim.models.Word2Vec.load("emotion_vocabulary")
            model.wv.save_word2vec_format("emotion_vocabulary1.txt", binary=False)
            print("model trained successfully")
        else: print("no data is read")
        #model.wv.save_word2vec_format("emotion_vocabulary",binary = "True
    def model_test(self):
        #model.wv.load_word2vec_format("emotion_vocabulary",encodeing='gb18030')
        #model=gensim.models.Word2Vec.load("model_test")
        model = gensim.models.KeyedVectors.load_word2vec_format("emotion_vocabulary.txt", binary=False)
        voc_list=model.wv.index2word
        #print('最接近的5个为')
        list1=["舒服","好累","太慢了","温馨","氛围",'最美的','美好',
               "很美", "好美", '热情', '美得',
               '满街', '美景', '处处是'
               ]
        for word in list1:
            if word in voc_list:
                #y1 = model.similarity(u"不错", u"好")
                y2 = model.most_similar(word, topn=3)
                print('与',word,'最接近的3个为',y2)
        #print(model["有点"])

    def sen_vec(self):

        i = 0
        ILLEGAL_CHARACTERS = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
        list_name = ['zhiti', 'qinggan', 'renzhi', 'ganzhi', 'shejiao', 'sikao']
        list_ganzhi = ["舒服", "好累", "太慢了", "温馨", "氛围", '最美的', '美好',
                       "很美", "好美", '热情', '美得',
                       '满街', '美景', '处处是'
                       ]

        list_zhiti = ["刷微博", "做饭", "回程", "买菜", "自拍", '前往', '看到',
                      "遇到", "去", '路过', '饱览',
                      '瞭望', '参观', '分享', '发照片', '留念', '吐槽']

        list_qinggan = ["只是我", "我只能", "心心念", "朝思暮想的", "很喜欢", '情迷', '令人惶恐',
                        "竟然", "巧遇", '努力', '最爱的',
                        '浮想联翩', '享受', '再来一次', '还是要']

        list_renzhi = ["每日", "餐", "日常", "循例", "国民", '地域名', '景点名',
                       "景色类型", "等", '当地', '就成了',
                       '室外桃园']

        list_shejiao = ["我们", "异乡人", "老朋友", "伙伴", "陪伴", '同游者', '法国人',
                        "帮我们", "欢迎", '交流', '收留',
                        '服务周到', '真会玩', '带礼物给', '发照片', '留念', '吐槽']

        list_sikao = ["人生", "也只有", "回望过去", "欠考虑", "便在于", '厚重感', '顿悟',
                      "且行且珍惜", "谈不上", '在我看来', '并不是因为',
                      '生活的真谛']
        model = gensim.models.KeyedVectors.load_word2vec_format("emotion_vocabulary.txt",
                                                                binary=False)
        voc_list = model.wv.index2word
        data = pd.read_csv('D:\\NLP_DATA\\comments_10w2.csv')
        ganzhi_sim = []
        for con in data.iloc:
            word_sim = []
            temp = ILLEGAL_CHARACTERS.sub(r'', con[3])
            word = sim_comp(voc_list, temp)
            if word:  # chained index error
                # print(word)
                for test in list_sikao:
                    if test in voc_list:
                        for word1 in word:
                            x = model.similarity(test, word1)
                            # print((test,word))
                            word_sim.append(x)
                        # print(x)

                word_sim = sorted(word_sim, reverse=True)
                ganzhi_sim.append(word_sim[0])
                # print(word_sim)
            else:
                print(-1)
                ganzhi_sim.append(0)
            i += 1
            print(i)
        with pd.ExcelWriter('six_section1.xlsx') as writer:
            dataframe = pd.DataFrame({'similarity': ganzhi_sim})
            dataframe.to_excel(writer, sheet_name='qinggan')  # 这句话有问题

if __name__=='__main__':
    Data_preview('D:\\NLP_DATA\\comments_5w.txt',1000)
