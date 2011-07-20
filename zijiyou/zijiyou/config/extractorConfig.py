# -*- coding: utf-8 -*-

extractorConfig = {

                    "lotourSpider":{
                            "Article":{
                                    r'publishDate':r'/html/body/div[2]/div/div/div/p',
                                    r'content':r'//*[@id="zoom"]',                                                
                                    r'title':r'//div[@id="maincontent"]/h6',
                            },
                     },
                    "daodaoSpider":{
                            "POI":{
                                    r'name':r'//div[@class="wrpHeader clearfix"]/h1[@id="HEADING"]/text()',
                                    r'area':r'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li/a/text()',
                                    r'address':r'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
                                    r'desc':r'//div[@class="clearfix"]/div/div[@class="review-intro"]/p/text()',
                                    r'descLink':r'//div[@class="clearfix"]/div/div[@class="review-intro"]',
                                    r'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
                                    r'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()'    
                            },
                            "Article":{
                                    #第一部分和CommonSenseItem的一样
                                    r'author':r'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                                    r'publishDate':r'//div[@class="article-title borderBom"]/p/span[2]/text()',
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
                },
                "lvpingSpider":{                                    
                            "Attraction":{
                                    r'name':r'//h1[@property="v:name"]/text()',
#                                    r'address':r'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
                                    r'desc':r'//div[@id="hiddenContent"]',
                                    'area':'//div[@class="breadBar"]/a//text()', 
#                                    r'descLink':r'//div[@class="clearfix"]/div/div[@class="review-intro"]',
#                                    r'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
#                                    r'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()'
                                    r'ticket':r'//div[@id="hiddenContent"]/span[2]/following-sibling::p/text()',
                                    r'replyNum':r'//em[@property="v:count"]/text()',
                                    r'popularity':r'//div[@class="order_num"]/text()'
                            },                                    
                            "AttractionRegex":{
#                                    r'address':r'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
#                                    r'descLink':r'//div[@class="clearfix"]/div/div[@class="review-intro"]',
#                                    r'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
#                                    r'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
                                    'center':r'//div[@class="hotel_map_detail"]/div[@class="search_map_blk"]/a/img/@src',
                                    'centerRegex':'center=(\d+[.]?\d*)[,](\d+[.]\d*)[&]*',
                                    'englishName':r'//h1[@property="v:name"]/i/text()',
                                    'englishNameRegex':r'([\w _-]+)',      
#                                    'area':'//div[@class="breadBar"]/a//text()',    
#                                    'areaRegex':r'首页[ -]+(.*)-[^-]*景点'
                                    'traffic':r'//div[@id="hiddenContent"]',
                                    'trafficRegex':r'<span style="font-weight:bold;.*<span style="font-weight:bold;">',
                            },
                            
                            "Article":{
                                        #第一部分和CommonSenseItem的一样
                                    r'author':r'//div[@class="memberInfor cf desDistance"]/a[1]/text()',
                                    r'publishDate':r'//div[@class="memberInfor cf desDistance"]/em/text()',
                                    r'content':r'//div[@class="yjDetail cf"]',
#                                    r'pvNum':r'',
                                    r'replyNum':r'//div[@class="memberInfor cf desDistance"]/a[2]/text()',
#                                    r'collectionNum':r'',
#                                    r'helpfulNum':r'',
#                                    r'unhelpfulNum':r'',
                                        #第二部分不一样
                                    r'title':r'//div[@class="viewnameShow"]/h1/text()',
                                    r'area':r'//div[@class="breadBar"]/a//text()',
                                    r'type':r'//div[@class="breadBar"]/a[5]/text()',
                                    r'destination':r'//div[@class="breadBar"]/a[4]/text()',
#                                    r'tag':r'',
#                                    r'attractions':r'',
#                                    r'feature':r'',
                            },                            
                            
                            "Note":{
                                        #第一部分和NoteItem的一样
#                                    r'author':r'',
                                    r'publishDate':r'//h6[@class="cf"]/span[2]/text()',
                                    r'content':r'//ul[@class="playAt_detail"]',
#                                    r'pvNum':r'//em[@id="pvNum"]/text()',
                                    r'replyNum':r'//h6[@class="cf"]/span[2]/a/text()',
#                                    r'collectionNum':r'//em[@id="collectionNum"]/text()',
#                                    r'helpfulNum':r'//em[@id="helpfulNum"]/text()',
#                                    r'unhelpfulNum':r'//em[@id="unhelpfulNum"]/text()',
                                        #第二部分不一样
                                    r'area':r'//div[@class="breadBar"]/a//text()',
                                          
                            },
                            
                            "NoteResp":{
                                    'noteType':'url' 
                            },
                            
                            "MemberInfo":{
                                    r'name':r'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
                                    r'ageRange':r'//div[@class="aboutmecon"]/dl/dd[5]/em/text()',
                                    r'gender':r'//div[@class="aboutmecon"]/dl/dd[6]/em/text()',
                                    r'currentAddress':r'//div[@class="aboutmecon"]/dl/dd[1]/em/text()',
                                    r'joinDate':r'//div[@class="personalinfor"]/ul/li[2]/p[3]/strong/text()',
                                    r'selfIntroduction':r'//div[@class="aboutmecon"]/dl/dd[2]/em/text()',
                                    r'comsumptionLevel':r'//div[@class="aboutmecon"]/dl/dd[3]/em/text()',
                                    r'travalPurpose':r'//div[@class="aboutmecon"]/dl/dd[4]/em/text()',
                                    r'travelPreference':r'//div[@class="aboutmecon"]/dl/dd[7]/span//text()',
                                    r'travelPartner':r'//div[@class="aboutmecon"]/dl/dd[8]/span//text()',
                            },
                            #js方式，暂时爬不到数据
#                                    "MemberTrack":{
#                                    r'name':r'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
#                                    r'gone':r'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon01.gif"]/parent::*/a/text()',
#                                    r'know':r'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon02.gif"]/parent::*/a/text()',
#                                    r'like':r'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon03.gif"]/parent::*/a/text()',
#                                    r'plan':r'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon04.gif"]/parent::*/a/text()'
#                                    },
                            "MemberFriend":{
                                    r'name':r'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
                                    r'nameList':r'//li[@class="two"]/a/text()',
                                    r'cityList':r'//li[@class="two"]/span/text()',
#                                    r'goneNumList':r'//li[@class="three"]/text()',
#                                    r'discoverList':r'//li[@class="three"]/span/text()',
                                    r'linkList':r'//li[@class="two"]/a/@href',
                            },
                            "MemberNoteList":{
                                    r'author':r'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
                                    r'titleList':r'//dl[@id="showbgcolor"]/dd/strong/a/text()',
                                    r'dateList':r'//dl[@id="showbgcolor"]/dd/span[1]/text()',
                                    r'destinationList':r'//dl[@id="showbgcolor"]/dd/q//text()',
                                    r'pvNumList':r'//dl[@id="showbgcolor"]/dd/span[2]/text()',
                                    r'replyNumList':r'//dl[@id="showbgcolor"]/dd/span[3]/text()',
                                    r'linkList':r'//dl[@id="showbgcolor"]/dd/strong/a/@href',
                            },
                            
                            "Region":{
                                    r'name':r'//div[@class="citynameShow cf"]/strong/text()',
                                    r'area':r'//div[@class="breadBar"]/a/text()',
                                    r'introduction':r'//p[@id="city_intro02"]',
                                    r'hotHotelLink':r'//a[@id="link_hotels_lc"]/@href',
                            }
                },
                "meishiSpider":{    
                            "Article":{
                                    'content':'//table/tr/td[@class="main2"]/p[2]',
                            },                         
                            "ArticleRegex":{
                                    'title':'//table/tr/td[@class="main1"]',
                                    'titleRegex':'<font color="c00000">(.*?)</font>',
                                    'author':'//table/tr/td[@class="main2"]/p[1]/font[1]',
                                    'authorRegex':']:\s*(.*?)\s*<font',
                            }
                },
                "mafengwoSpider":{
                            "Article":{
                                    'author':'//div[@id="first_lz_area"]/div[@class="top_area"]/div[@class="nameanddate"]/span[@class="author_name"]/a/text()',
                                    'publishDate':'//div[@id="first_lz_area"]/div[@class="top_area"]/div[@class="nameanddate"]/span[@class="date m_l_5"]/text()',
                                    'title':'//div[@class="M_nav"]/div[@class="Mztit"]/h1/text()',
                                    'content':'//div[@id="first_lz_area"]/div[@id="pnl_contentinfo"]',
                                    'destination':'//div[@class="r_con"]/div[@class="xg_mdd"]/div[@class="mdd_name"]/a/text()',
                            },
                            "POI":{
                                    'name':'//div[@class="main_nav"]/div[@class="mddtit"]/h1/text()',
                                    'area':'//div[@class="spot_head"]/div[@class="l_area"]/div[@class="spot_name"]/text()',
                            },
                },
                "17uSpider":{
                             #第一部分
                            "Article1":{
                                    
                                    'author':'//div[@id="bContent"]/div[@id="bArticleBody"]/div[@class="bArticleHeader"]/span[@class="bArtitleAutor"]/a[1]/text()',
                                    'category':'//div[@id="bArticleContent"]/div[@class="info"]/a/text()',
                                    'content':'//div[@id="bArticleContent"]/font/text()',
                                    
                            },
                            "Article1Regex":{
                                    'title':'//div[@id="bContent"]/div[@id="bArticleBody"]/div[@class="bArticleHeader"]/h3/text()',
                                    'titleRegex':'(.*)\r\s*',
                                    'publishDate':'//div[@id="bContent"]/div[@id="bArticleBody"]/div[@class="bArticleHeader"]/span[@class="bArtitleAutor"]/a[2]/@title',
                                    'publishDateRegex':'(\d{4}-\d{1,2}-\d{1,2})',
                                    'pvNum':'//div[@id="bArticleAttribute"]/span[@class="bAttrLeft"]',
                                    'pvNumRegex':u'点击'+'：(\d+)',
                                    'replyNum':'//div[@id="bArticleAttribute"]/span[@class="bAttrLeft"]',
                                    'replyNumRegex':u'评论'+'：(\d+)',
                            },
                            "Article2":{
                                    'title':'//div[@class="center"]/div[@class="leftside"]/div[@class="leftside_top"]/h2[@class="leftside_head"]/text()',
                                    'content':'//div[@id="infor_main"]',
                            }
                },
}