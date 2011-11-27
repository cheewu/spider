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
    tagsIgnore=["head","style", "script", "noscript", "<built-in function comment>", "option"]
    title = ''
    publishDate = ''
    pdateReg = r'(\d{4}[年-]+\d{1,2}[月-]+\d{1,2})'
    
    def doExtract(self,html,threshold=None):
        """
        抽取正文
        threshold 纯文本密度默认0.16
        RETURN:
        标题，发布时间，正文
        """
        #初始化title publishdate
        self.title = ''
        self.publishDate = ''
        threshold = threshold == None and float(0.16) or float(threshold)
        if not type(html) == unicode:
            html = unicode(html,'utf-8')
        mtHtml = self._extMainText(html, threshold)
        # Transfer to plain text:
        text = self.getText(mtHtml,isextract=True)
        return self.title,self.publishDate,text.strip()
    
    def getText(self,html,isextract=False):
        if not type(html) == unicode:
            html = unicode(html, 'utf-8')
        root = fromstring(html)
        tagsNewline=["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "br", "li"]
        tagsSave = ["img"]
        def _getText(tree):
            text = ''
            hasChild = False
            if len(tree) > 0:
                hasChild = True
            tag = str(tree.tag).lower()
            if tag in self.tagsIgnore:
                return ''
            #判断是否是保留标签
            if tag in tagsSave:
                text += "<" + tag + " "
                #读取标签属性
                for k,v in tree.attrib.items():
                    text += " "+k + " ='" + v + "' "
                if tree.text or hasChild:
                    text += " >"
                else:
                    text += " />"
            #添加文本和继续往下遍历
            if tree.text != None:
                text += tree.text
            for child in tree:
                text += _getText(child)
            #判断是否是保留标签,保留则添加关闭标签
            if tag in tagsSave:
                if tree.text or hasChild:
                    text += "</" + tag + ">"
            elif str(tree.tag).lower() in tagsNewline:
                text += '\n'
            if tree.tail != None:
                text += tree.tail
            return text
        return _getText(root)
    
    def _extMainText(self,html, threshold, filterMode=False):
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
        if filterMode:
            return self._filterSpam(densDic, threshold)
        else:
            #etree instance, text length, list of child etrees, total text length of child etrees
            maxPart, textLen, maxPartChilds, textLenChilds = self._getMainText(densDic, threshold)
            if textLenChilds > textLen:
                return ''.join(map(lambda tree: etree.tostring(tree, encoding = unicode) if tree != None else '', maxPartChilds))
            else:
                return etree.tostring(maxPart, encoding = unicode) if maxPart != None else ''
    
    def _calcDensity(self,tree):
        """
        计算纯文本密度 = 标签下包含的纯文本长度 / 标签下的总长度
        同时找到发布时间
        RETURN：
        {
        'self': (标签密度, 纯文本长度, 标签下的文本总长度 , etree实例), 
        'child': 子标签的密度字典
        }
        """
        #a tag which is a string identifying what kind of data this element represents (the element type, in other words).
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
        if tag in self.tagsIgnore:
            return {'self': (0.0, 0, 0, tree)}
        #a text string.
        text = tree.text if tree.text != None else ''
        #找时间
        if len(self.publishDate) < 1 :
            match = re.search(self.pdateReg, str(text))
            if match :
                self.publishDate = match.group(1)
                self.publishDate = self.publishDate.strip()
        #an optional tail string. be used to hold additional data associated with the element. contains any text found after the element’s end tag and before the next tag.
        tail = tree.tail if tree.tail != None else ''
        countTextLen = len(text.strip()) + len(tail.strip())
        totalLen = len(etree.tostring(tree, encoding = unicode)) if tree != None else 0
        if tag == 'br':
            return {'self': (1.0 / totalLen, 1, totalLen, tree)}
        dicList = []
        treeOrig = tree[:]
        for subtree in treeOrig:
            textNode = None
            index = 0
            if subtree.tail and len(subtree.tail.strip()) > 0:
                index = tree.index(subtree)
                textNode = subtree.tail
                subtree.tail = ''
            dic = self._calcDensity(subtree)
            dicList.append(dic)
            textLen = dic['self'][1]
            countTextLen += textLen
            # subtree.tail 视为独立的etree 分支:
            if textNode != None:
                textNodeTotalLen = len(textNode.strip())
                textNodeTextLen = len(textNode.strip())
                textTree = etree.Element('span')
                textTree.text = textNode
                tree.insert(index + 1, textTree)
                dicList.append({'self': (float(textNodeTextLen) / textNodeTotalLen, textNodeTextLen, textNodeTotalLen, textTree)})
                countTextLen += textNodeTextLen
        density = float(countTextLen) / totalLen if totalLen != 0 else 0.0
        return {'self': (density, countTextLen, totalLen, tree), 'child': dicList}
    
    def _removeControlChars(self,html):
        """
        null字节替换为空格
        html-unicode
        """
        assert type(html) == unicode, 'Input html text must be unicode!'
        return self.control_char_re.sub(' ', html)
    
    def _filterSpam(self,densDic, threshold):
        """
        Walk through html document, drop off all etree branches that having low text
        density, and return the left parts of fragments.
    
        Return: html fragments of main text
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
        dens, textLen, totalLen, tree = densDic['self']
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
                    childDens, childTextLen, childTotalLen, childTree = childDic['self']
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
