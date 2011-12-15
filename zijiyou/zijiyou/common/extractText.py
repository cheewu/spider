# -*- coding: utf-8 -*-
'''
Created on 2011-5-15

@author: shiym
'''
from lxml.html import fromstring
from lxml.html import tostring
from lxml import etree
import re

class Extracter(object):

    control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))
    control_char_re = re.compile('[%s]' % re.escape(control_chars))
    tagsIgnore=["head","style", "script", "noscript", "<built-in function comment>", "option","textarea"]
    title = ''
    publishDate = ''
    pdateReg = r'(\d{4}[年-]+\d{1,2}[月-]+\d{1,2})'
    
    def doExtract(self,html,threshold=None,htmlId = 'noid'):
        """
        抽取正文
        threshold 纯文本密度默认0.16
        RETURN:
        标题，发布时间，正文，图片列表
        """
        #初始化title publishdate
        self.title = ''
        self.publishDate = ''
        threshold = threshold == None and float(0.16) or float(threshold)
        if not type(html) == unicode:
            html = unicode(html,'utf-8')
        mtHtml,denstup = self._extMainText(html, threshold,htmlId=htmlId)
        # Transfer to plain text:
        text = self.getText(mtHtml,isextract=True)
        imgs = self.getImg(mtHtml)
        return self.title,self.publishDate,text.strip(),imgs
    
    def doExtract2(self,html,threshold=None,htmlId = 'noid'):
        """
        抽取正文
        threshold 纯文本密度默认0.16
        RETURN:
        标题，发布时间，正文，图片列表，密度字典（xpath，文本密度，文本长度，标签密度，标签个数）
        """
        #初始化title publishdate
        self.title = ''
        self.publishDate = ''
        threshold = threshold == None and float(0.16) or float(threshold)
        if not type(html) == unicode:
            html = unicode(html,'utf-8')
        mtHtml,denstup = self._extMainText(html, threshold,htmlId=htmlId)
        # Transfer to plain text:
        text = self.getText(mtHtml,isextract=True)
        imgs = self.getImg(mtHtml)
        return self.title,self.publishDate,text.strip(),imgs,denstup
    
    def getImg(self,html):
        """
        抽取html中的图片
        RETURN:
        [img]
        """
        if html is None or len(html) < 20:
            return None
        if not type(html) == unicode:
            html = unicode(html,'utf-8')
        root = fromstring(html)
        def _getImg(tree):
            imgs = []
            if str(tree.tag).lower() == 'img' and re.match('.*src[ ]*=".*(\w{20,100}).*',str(etree.tostring(tree,encoding=unicode))) is not None:
                img = '<img '
                #读标签属性
                for k,v in tree.attrib.items():
                    img += ' '+k+' ="' + v + '" '
                img += ' />'
                imgs.append(img)
            #递归在字节点找img
            for child in tree:
                imgsTmp = _getImg(child)
                if imgsTmp is not None and len(imgsTmp) > 0:
                    imgs.extend(imgsTmp)
            return imgs
        return _getImg(root)
    
    def getText(self,html,isextract=False):
        '''
        去掉除图片、标题标签外的其余标签，替换换行符号。
        '''
        if html is None or len(html) <20:
            return ''
        if not type(html) == unicode:
            html = unicode(html, 'utf-8')
        root = fromstring(html)
        tagsNewline=["p", "div", "br", "li"]
        tagsSave = ["h1", "h2", "h3", "h4", "h5", "h6", ]
        def _getText(tree):
            text = ''
            hasChild = False
            if len(tree) > 0:
                hasChild = True
            tag = str(tree.tag).lower()
            if tag in self.tagsIgnore:
                return ''
            #判断是否是保留标签 滤除小图标
            if tag in tagsSave or (tag == 'img' and re.match('.*src[ ]*=".*(\w{20,100}).*', str(etree.tostring(tree,encoding=unicode))) is not None):
                text += '<' + tag + ''
                #读取标签属性
                for k,v in tree.attrib.items():
                    text += ' '+k + ' ="' + v + '" '
                if tree.text or hasChild:
                    text += ' >'
                else:
                    text += '/>'
            #添加文本和继续往下遍历
            if tree.text is not None:
                text += tree.text
            for child in tree:
                text += _getText(child)
            #判断是否是保留标签,保留则添加关闭标签
            if tag in tagsSave or (tag == 'img' and re.match('.*src[ ]*=".*(\w{20,100}).*', str(etree.tostring(tree,encoding=unicode))) is not None):
                if tree.text or hasChild:
                    text += "</" + tag + ">"
            #换行
            elif str(tree.tag).lower() in tagsNewline:
                text += '\n'
            if tree.tail != None:
                text += tree.tail
            return text
        return _getText(root)
    
    def _extMainText(self,html, threshold, filterMode=False,htmlId = 'noid'):
        """
        抽取正文或纯文本密度大于阀值的片段
        PARAMETERS:
        html - UNICODE编码。
        threshold - 纯文本密度阀值
        filterMode - 是否使用过滤模式(小于阀值直接删除)
        RETURN:
        正文片段
        """
        html = self._removeControlChars(html)
        root = fromstring(html)
        densDic = self._calcDensity(root)
        if filterMode :
            return self._filterSpam(densDic, threshold)
        else:
            #(etree, 文本长度, 子节点列表, 子节点文本长度总和)
#            maxPart, textLen, maxPartChilds, textLenChilds= self._getMainText3(densDic, threshold)
#            densidic = None
#            xpath = None
#            if maxPart is not None:
##                densidic,xpath = self._findDensityDicDirth(densDic)
#                densidic,xpath = self._findDensityDic(maxPart, densDic)
#            elif maxPartChilds is not None and len(maxPartChilds) >0:
##                densidic,xpath = self._findDensityDicDirth(densDic)
#                densidic,xpath = self._findDensityDic(maxPartChilds[0], densDic)
#            else:
#                print 'id:%s 没有找到正文' % (htmlId)
#                return ''
#            print 'id:%s max部分xpath:%s 文本密度：%s 文本长度:%s 标签密度%s 标签个数%s ' % (htmlId,xpath,densidic[0],densidic[1],densidic[4],densidic[5])
#            if textLenChilds >= textLen:
#                return ''.join(map(lambda tree: etree.tostring(tree, encoding = unicode) if tree != None else '', maxPartChilds))
#            else:
#                return etree.tostring(maxPart, encoding = unicode) if maxPart != None else ''
            mainTag = self._getMainText4(densDic, threshold)
            densdic = {'xpath':mainTag['xpath'],'文本密度':mainTag['self'][0],'文本长度':mainTag['self'][1],'标签密度':mainTag['self'][4],'标签个数':mainTag['self'][5]}
            return etree.tostring(mainTag['self'][3],encoding = unicode) if mainTag['self'][3] is not None else '' , densdic
    
    def _calcDensity(self,tree):
        """
        计算纯文本密度 = 标签下包含的纯文本长度 / 标签下的总长度
        标签密度=1000*标签数/文字数
        其中，图片的长度作为字数计算
        同时找到发布时间
        RETURN：
        {
        'self': (纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数), 
        'child': 子标签的密度字典
        }
        """
        tag = str(tree.tag).lower()
        #找title
        if len(self.title) < 1 and tag == 'head':
            subtags = tree[:]
            for subtag in subtags:
                if str(subtag.tag) == 'title' and subtag.text:
                    self.title = str(subtag.text)
                    if self.title:
                        self.title = self.title.strip()
                        break
        text = tree.text if tree.text != None else ''
        #找时间
        if len(self.publishDate) < 1 :
            match = re.search(self.pdateReg, str(text))
            if match :
                self.publishDate = match.group(1)
                self.publishDate = self.publishDate.strip()
        if tag in ["style", "script", "noscript", "<built-in function comment>", "option","textarea"]:#textarea
            return None
        #an optional tail string. be used to hold additional data associated with the element. contains any text found after the element’s end tag and before the next tag.
        tail = tree.tail if tree.tail != None else ''
        countTextLen = len(text.strip()) + len(tail.strip())
        totalLen = len(etree.tostring(tree, encoding = unicode).strip()) if tree != None else 1
        if tag == 'br':
            return {'self': (1.0 / totalLen, 1, totalLen, tree,0,0)}
        dicList = []
        treeOrig = tree[:]
        #标签数
        tagNum = len(treeOrig)
        #遍历字节点
        for subtree in treeOrig:
            #记录有tail的节点下标和text
            textNode = None
            index = 0
            if subtree.tail and len(subtree.tail.strip()) > 0:
                index = tree.index(subtree)
                textNode = subtree.tail
                subtree.tail = ''
            dic = self._calcDensity(subtree)
            if dic is None:
                continue
            dicList.append(dic)
            textLen = dic['self'][1]
            countTextLen += textLen
            tagNum += dic['self'][5]
            # subtree.tail 视为紧邻subtree的子节点:
            if textNode is not None and len(textNode.strip())>0:
                textNodeTotalLen = len(textNode.strip())
                textNodeTextLen = len(textNode.strip())
                textTree = etree.Element('span')
                textTree.text = textNode
                tree.insert(index + 1, textTree)
                dicList.append({'self': (float(textNodeTextLen) / textNodeTotalLen, textNodeTextLen, textNodeTotalLen, textTree, 0,0)})#一处
                countTextLen += textNodeTextLen
            #图片的长度作为字数计算
            if str(subtree.tag).lower() == 'img':
                #滤除小图标
                if re.match('.*src[ ]*=".*(\w{20,100}).*', str(etree.tostring(subtree,encoding=unicode))) is not None:
                    countTextLen += len(etree.tostring(subtree, encoding = unicode).strip())
        density = float(countTextLen) / totalLen if totalLen != 0 else 0.0
        tagdens = 1000 * float(tagNum) / countTextLen if countTextLen != 0 else 0.0
        return {'self': (density, countTextLen, totalLen, tree,tagdens,tagNum), 'child': dicList}
    
    def _removeControlChars(self,html):
        """
        null字节替换为空格
        html-unicode
        """
        assert type(html) == unicode, 'Input html text must be unicode!'
        return self.control_char_re.sub(' ', html)
    
    def _filterSpam(self,densDic, threshold):
        """
        过滤模式
        遍历html文档，文本密度低于阀值的分支全部删除，返回剩余部分
        RETRUN:
        主文本字符串
        """
        dens, textLen, totalLen, tree = densDic['self']
        # If density is larger than threshold, keep and return current tag branch:
        if dens >= threshold:
            return etree.tostring(tree, encoding = unicode)
        if str(tree.tag).lower() == 'br':
            return etree.tostring(tree, encoding = unicode)
        # If density of current tag branch is too small, check its children:
        else:
            frags = []
            if densDic.has_key('child'):
                for childDic in densDic['child']:
                    frags.append(self._filterSpam(childDic, threshold))
            return ''.join(frags)
    
    def _getMainText(self,densDic, threshold):
        """
        Get the largest html fragment with text density larger than threshold according 
        to density dictionary.
    
        And the largest html fragment could be made up of several continuous brother
        html branches.
    
        Return: (etree instance, text length, list of child etrees, total text length of child etrees)
        """
        dens, textLen, totalLen, tree,tagDens,tagNum = densDic['self']
        maxChildTrees = []
        maxChildTreesTextLen = 0
        # If density is bigger than threshold, current tag branch is the largest:
        if dens >= threshold:
            maxTree = tree
            maxTextLen = textLen
        # If density of current tag branch is too small, check its children:
        else:
            maxTree = None
            maxTextLen = 0
            maxChildSubTrees = []
            maxChildSubTreesTextLen = 0
            childTreesTmp = []
            childTreesTmpTextLens = []
            childTreesTmpTotalLens= []
            if densDic.has_key('child'):
                for childDic in densDic['child']:
                    childDens, childTextLen, childTotalLen, childTree,tagDens,tagNum = childDic['self']
                    tree, textLen, childTrees, childTreesTextLen = self._getMainText(childDic, threshold)
                    # Remember the largest tag branches of children:
                    if childTreesTextLen > maxChildSubTreesTextLen:
                        maxChildSubTrees, maxChildSubTreesTextLen = childTrees, childTreesTextLen
                    childTreesTmp.append(childTree)
                    childTreesTmpTextLens.append(childTextLen)
                    childTreesTmpTotalLens.append(childTotalLen)
                    if textLen > maxTextLen:
                        maxTree = tree
                        maxTextLen = textLen
                # Find the largest html fragment under current tag branch:
                for j in range(1, len(childTreesTmp) + 1):
                    for i in range(j):
                        childTreesTmpTotalLen= sum(childTreesTmpTotalLens[i:j])
                        childTreesTmpTextLen = sum(childTreesTmpTextLens[i:j])
                        childTreesTmpTotalLen = 1 if childTreesTmpTotalLen == 0 else childTreesTmpTotalLen
                        if float(childTreesTmpTextLen) / childTreesTmpTotalLen >= threshold:
                            if childTreesTmpTextLen > maxChildTreesTextLen:
                                maxChildTrees = childTreesTmp[i:j]
                                maxChildTreesTextLen = childTreesTmpTextLen
                # Compare html fragment of current tag branch and the ones of children:
                if maxChildSubTreesTextLen > maxChildTreesTextLen:
                    maxChildTrees, maxChildTreesTextLen = maxChildSubTrees, maxChildSubTreesTextLen
        return (maxTree, maxTextLen, maxChildTrees, maxChildTreesTextLen)

    def _getMainText2(self,densDic, threshold):
        """
        找超过密度阀值的最大的文本块
        不应该包含 “上一篇 下一篇”或“上一页 下一页“
        最大文本块可以是连续的子节点节点序列
        
        RETURN：
        (etree, 文本长度, 子节点列表, 子节点文本长度总和)
        """
        #纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数
        dens, textLen, totalLen, tree,tagDens,tagNum = densDic['self']
        #默认
        maxTree = None
        maxTextLen = 1
        maxChildTrees = []
        maxChildTreesTextLen = 0
        # 当前分支文本密度是否满足阀值
        if dens >= threshold :#and tree.text and not re.match('(.*上一篇.*下一篇.*)|(.*上一页.*下一页.*)|(.*前一页.*后一页.*)', tree.text)
            maxTree = tree
            maxTextLen = textLen
        needDeep = False
        if densDic.has_key('child'):
            for p in densDic['child']:
                if p['self'][0] >= threshold and p['self'][1] >= textLen-10:
                    needDeep = True
                    break
        # 否则递归子节点
        if maxTree is None or needDeep:
            maxTree = None
            maxTextLen = 0
            maxChildSubTrees = []
            maxChildSubTreesTextLen = 0
            childTreesTmp = []
            childTreesTmpTextLens = []
            childTreesTmpTotalLens= []
            if densDic.has_key('child'):
                for childDic in densDic['child']:
                    #(纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数)
                    childDens, childTextLen, childTotalLen, childTree ,childTagDens,childTagNum= childDic['self']
                    # 最大正文--孙子节点 (etree, 文本长度, 子节点列表, 子节点文本长度总和)
                    tree, textLen, childTrees, childTreesTextLen= self._getMainText(childDic, threshold)
                    if tree is not None and str(tree.tag).lower() in ['td','div'] and childTreesTextLen >= maxChildSubTreesTextLen -15 : #and not re.match('(.*上一篇.*下一篇.*)|(.*上一页.*下一页.*)|(.*前一页.*后一页.*)', tree.text)
                        maxChildSubTrees, maxChildSubTreesTextLen = childTrees, childTreesTextLen
                    # 最大正文--连续子节点序列
                    if childTree is not None and str(childTree.tag).lower() in ['td','div']:
                        childTreesTmp.append(childTree)
                        childTreesTmpTextLens.append(childTextLen)
                        childTreesTmpTotalLens.append(childTotalLen)
                        if textLen >= maxTextLen -15:
                            maxTree = tree
                            maxTextLen = textLen
                # 最大正文--连续子节点序列，序列满足阀值要求
                for j in range(1, len(childTreesTmp) + 1):
                    for i in range(j):
                        childTreesTmpTotalLen= sum(childTreesTmpTotalLens[i:j])
                        childTreesTmpTextLen = sum(childTreesTmpTextLens[i:j])
                        childTreesTmpTotalLen = 1 if childTreesTmpTotalLen == 0 else childTreesTmpTotalLen
                        if float(childTreesTmpTextLen) / childTreesTmpTotalLen >= threshold :
                            #滤除没有文本内容的标签
                            if childTreesTmpTextLen >= maxChildTreesTextLen -15:
                                maxChildTrees = childTreesTmp[i:j]
                                maxChildTreesTextLen = childTreesTmpTextLen
                # 连续字节点的文本长度与孙子节点文本长度比较，选择文本更长的节点作为当前节点的子节点
                if maxChildSubTreesTextLen >= maxChildTreesTextLen -15:
                    maxChildTrees, maxChildTreesTextLen = maxChildSubTrees, maxChildSubTreesTextLen
        #(etree, 文本长度, 子节点列表, 子节点文本长度总和, 标签密度，标签数,正文密度)
        return (maxTree, maxTextLen, maxChildTrees, maxChildTreesTextLen)
    
    def _getMainText3(self,densDic, threshold,tagdensth=10,xpath = ''):
        """
        找正文块
        不应该包含 “上一篇 下一篇”或“上一页 下一页“
        最大文本块可以是连续的同级节点序列
        
        RETURN：
        (正文结点实例etree, 文本长度, 子节点列表, 子节点文本长度总和)
        """
        #纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数
        dens, textLen, totalLen, tree,tagDens,tagNum = densDic['self']
        #无用节点
        if str(tree.tag).lower() in self.tagsIgnore:
            return None
        #主文本块
        maxTree = None
        maxTextLen = 1
        xpath += '/'+ str(tree.tag).lower()
        #主文本节点序列
        maxChildTrees = []
        maxChildTreesTextLen = 0
        # 当前分支文本密度是否满足阀值
        if dens >= threshold and str(tree.tag).lower() in ['div','td'] and re.match('(.*上一篇.*下一篇.*)|(.*前一篇.*后一篇.*)|(.*上一页.*下一页.*)|(.*前一页.*后一页.*)', str(etree.tostring(tree, encoding = unicode))) is None:
            maxTree = tree
            maxTextLen = textLen
        needDeep = False
        if densDic.has_key('child'):
            for p in densDic['child']:
                if p['self'][0] >= threshold and p['self'][1] >= textLen-15:
                    needDeep = True
                    break
        # 查看子节点序列是否满足。
        if maxTree is None or needDeep:
            childTrees=[]
            childTreesTextLens = []
            childTreesTotalLens= []
            childTreesTextLen = 0
            if densDic.has_key('child'):
                for childDic in densDic['child']:
                    #本级别节点一定不是主文本，主文本在其子节点中
                    if re.match('(.*上一篇.*下一篇.*)|(.*前一篇.*后一篇.*)|(.*上一页.*下一页.*)|(.*前一页.*后一页.*)', str(etree.tostring(childDic['self'][3], encoding = unicode))) is not None:
                        maxTree = None
                        maxTextLen = 0
                        childTrees = []
                        break
                    #主文本可能的块
                    if str(childDic['self'][3].tag).lower() in ['div','td']:
                        childTrees.append(childDic['self'][3])
                        childTreesTextLens.append(childDic['self'][1])
                        childTreesTotalLens.append(childDic['self'][2])
                for j in range(1,len(childTrees)+1):
                    for i in range(j):
                        #连续子节点序列的正文密度比
                        childTreesTextLen = sum(childTreesTextLens[i:j])
                        childTreesTotalLen = sum(childTreesTotalLens[i:j])
                        densTmp = float(childTreesTextLen) /childTreesTotalLen
                        if densTmp >= threshold:
                            #滤除铆文
                            if childTreesTextLen >= maxChildTreesTextLen - 30:
                                maxChildTrees,maxChildTreesTextLen = childTrees[i:j],childTreesTextLen
                                #子节点序列才是正文
                                if maxChildTreesTextLen >= maxTextLen-30:
                                    maxTree,maxTextLen = None,0
                            else:
                                break
        if maxTree is not None or len(maxChildTrees)>0:
            return (maxTree, maxTextLen, maxChildTrees, maxChildTreesTextLen,xpath)
        #递归，找子节点中最大的html段
        if densDic.has_key('child'):
            maxtup = [None,0,None,0]#加div的count=1.。。
            for childDic in densDic['child']:#加过滤：a img span input h1
                tup = self._getMainText3(childDic, threshold,xpath = xpath)
                if tup is not None and len(tup)>0 and tup[1] >= maxtup[1] - 30:
                    maxtup = tup
            return maxtup
        return None
    
    def _getMainText4(self,densDic, threshold,tagdensth=65,xpath = ''):
        """
        找正文块--采用层次非递归遍历法
        不应该包含 “上一篇 下一篇”或“上一页 下一页“
        最大文本块只可以是一个节点
        
        RETURN：
        {'self': (纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数), 'child': 子标签的密度字典,'xpath':''}
        """
        #节点队列，元素为节点信息元组 {'self': (纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数), 'child': 子标签的密度字典,'xpath':''}
        tagList = []
        #根节点入队列
        densDic['xpath']='/%s' %(str(densDic['self'][3].tag).lower() if densDic['self'][3] is not None else '')
        tagList.append(densDic)
        #依次访问节点队列元素
        index = 0
        #正文节点信息元组 {'self': (纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数), 'child': 子标签的密度字典,'xpath':''}
        maxTagTup={'self': (0.0, 0, 1 ,None, 0.0,1), 'child': [],'xpath':''}
        mainTag = None
        while index < len(tagList):
            #节点出队列
            tag = tagList[index]
            index += 1
            #节点的子节点入队列
            if tag.has_key('child'):
                #div计数器，便于debug
                count = 0
                for p in tag['child']:#无效节点不如队列
                    #无用节点
                    tagName = str(p['self'][3].tag).lower()
                    if str(p['self'][3].tag).lower() == 'div':
                        count += 1
                    if tagName in self.tagsIgnore or tagName in ['a','img','input','h1','h2','title','p'] or p['self'][1] < 200 :
                        continue
                    p['xpath'] = tag['xpath'] + '/%s[%s]' % (str(p['self'][3].tag).lower() if p['self'][3] is not None else '',count)
                    tagList.append(p)
            #访问节点 记录当前找到的最大的正文节点：如果新节点的正文数量 >= 当前最大找到的最大正文节点正文数-60，
            if str(tag['self'][3].tag).lower() in ['td','div'] and tag['self'][4] <=tagdensth and tag['self'][1] >= maxTagTup['self'][1] * (48 + len(maxTagTup['xpath'].split('/')) - len(tag['xpath'].split('/'))) / 50 - 50 and re.match('(.*前一篇.*后一篇.*)|(.*上一页.*下一页.*)|(.*前一页.*后一页.*)', str(etree.tostring(tag['self'][3], encoding = unicode))) is None:
                maxTagTup = tag
                #正文不应该包含 “上一篇 下一篇”或“上一页 下一页“
                if maxTagTup['self'][0] >= threshold :
                    mainTag = maxTagTup
                    #break条件：mainTag的子节点不会有更好的表现
                    isbreak = True
                    if mainTag.has_key('child'):
                        for child in mainTag['child']:
                            if child['self'][1] >= maxTagTup['self'][1] * (48 + len(maxTagTup['xpath'].split('/')) - len(tag['xpath'].split('/'))) / 50 - 50 :
                                isbreak = False
                                break
                    if isbreak:
                        break
        #完成节点遍历，没有找到符合条件的正文块，返回最大的正文块
        if mainTag is not None:
            return mainTag
        else:
            return maxTagTup
    
    def _findDensityDic(self,tree,densDic,xpath=''):
        """
        在densDic中定位tree，找到其密度字典：(纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数)
        RETRUN：
        (纯文本密度, 纯文本长度, 标签下的文本总长度 ,etree实例, 标签密度,标签数)
        """
        xp = xpath+'/'+str(densDic['self'][3].tag).lower()
        if densDic['self'][3] == tree:
            return densDic['self'],xp
        elif 'child' in densDic:
            for p in densDic['child']:
                target,xp2 = self._findDensityDic(tree, p,xp)
                if target is not None:
                    return target,xp2
        return None,None
    
    def _findDensityDicDirth(self,densDic,xpath=''):
        """
        找"上一篇、下一篇"
        """
        xp = xpath+'/'+str(densDic['self'][3].tag).lower()
        if re.match('(.*上一篇.*下一篇.*)|(.*上一页.*下一页.*)|(.*前一页.*后一页.*)', str(etree.tostring(densDic['self'][3],encoding = unicode))) is not None:
            return densDic['self'],xp
        elif 'child' in densDic:
            for p in densDic['child']:
                target,xp2 = self._findDensityDicDirth(p,xp)
                if target is not None:
                    return target,xp2
        return None,None
        
        