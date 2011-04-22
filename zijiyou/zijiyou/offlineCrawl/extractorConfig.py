# -*- coding: utf-8 -*-

extractorConfig = {
                "Attraction":{
                           r'name':r'//div[@class="wrpHeader clearfix"]/h1[@id="HEADING"]/text()',
                           r'area':r'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li/a/text()',
                           r'address':r'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
                           r'desc':r'//div[@class="clearfix"]/div/div[@class="review-intro"]/p/text()',
                           r'descLink':r'//div[@class="clearfix"]/div/div[@class="review-intro"]',
                           r'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
                           r'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()'    
                },
                
                "ResponseBody":{
                            #第一部分和CommonSenseItem的一样
                            r'author':r'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                            r'date':r'//div[@class="article-title borderBom"]/p/span[2]/text()',
                            r'content':r'//div[@class="article-content"]',
                            r'pvNum':r'//em[@id="pvNum"]/text()',
                            r'replyNum':r'//div[@class="interaction clearfix"]/span/a[@href="#"]/parent::*/text()',
                            r'collectionNum':r'//em[@id="collectionNum"]/text()',
                            r'helpfulNum':r'//em[@id="helpfulNum"]/text()',
                            r'unhelpfulNum':r'//em[@id="unhelpfulNum"]/text()',
                            #第二部分不一样
                            r'title':r'//div[@class="article-title borderBom"]/div/h1/text()',
                            r'area':r'//ul[@class="article-extra borderBom"]/li[1]/div/a/text()',
                            r'type':r'//ul[@class="article-extra borderBom"]/li[2]/a/text()',
                            r'tag':r'//ul[@class="article-extra borderBom"]/li[3]/div/a/text()',
                            r'attractions':r'//ul[@class="article-senior-tags borderBom"]/li[1]/div/a/text()',
                            r'feature':r'//ul[@class="article-senior-tags borderBom"]/li[2]/div/a/text()'
                },
                
                "CommonSense":{
                            #第一部分和NoteItem的一样
                            r'author':r'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                            r'date':r'//div[@class="article-title borderBom"]/p/span[2]/text()',
                            r'content':r'//div[@class="article-content"]',
                            r'pvNum':r'//em[@id="pvNum"]/text()',
                            r'replyNum':r'//div[@class="interaction clearfix"]/span/a[@href="#"]/parent::*/text()',
                            r'collectionNum':r'//em[@id="collectionNum"]/text()',
                            r'helpfulNum':r'//em[@id="helpfulNum"]/text()',
                            r'unhelpfulNum':r'//em[@id="unhelpfulNum"]/text()',
                            #第二部分不一样
                            r'area':r'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li[4]/a/text()',
                            r'type':r'//div[@class="article-title borderBom"]/div/h1/text()'   
                },
                "Note":{
                            #第一部分和NoteItem的一样
                            r'author':r'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                            r'date':r'//div[@class="article-title borderBom"]/p/span[2]/text()',
                            r'content':r'//div[@class="article-content"]',
                            r'pvNum':r'//em[@id="pvNum"]/text()',
                            r'replyNum':r'//div[@class="interaction clearfix"]/span/a[@href="#"]/parent::*/text()',
                            r'collectionNum':r'//em[@id="collectionNum"]/text()',
                            r'helpfulNum':r'//em[@id="helpfulNum"]/text()',
                            r'unhelpfulNum':r'//em[@id="unhelpfulNum"]/text()',
                            #第二部分不一样
                            r'area':r'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li[4]/a/text()',
                            r'type':r'//div[@class="article-title borderBom"]/div/h1/text()'   
                }
}