# -*- coding: utf-8 -*-

extractorConfig = {
                "bbkerSpider":{
                               "KeyList":{"keyWords":'//div[@class="doc"]/div[@class="col"]/div[@class="taglist"]/span//text()'},
                               },
                "baseSeSpider":{
                                "Article":{
                                    'content':'//body',
                                    'title':'//div/h3/text()'
                                        }
                                },
                "daodaoSpider":{
                            "POI":{
                                    'name':'//div[@class="wrpHeader clearfix"]/h1[@id="HEADING"]/text()',
                                    'area':'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li/a/text()',
                                    'address':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
                                    'desc':'//div[@class="clearfix"]/div/div[@class="review-intro"]/p/text()',
                                    'descLink':'//div[@class="clearfix"]/div/div[@class="review-intro"]',
                                    'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
                                    'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()'    
                            },
                            "Article":{
                                    #第一部分和CommonSenseItem的一样
                                    'author':'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                                    'publishDate':'//div[@class="article-title borderBom"]/p/span[2]/text()',
                                    'content':'//div[@class="article-content"]',
                                    'pvNum':'//em[@id="pvNum"]/text()',
                                    'replyNum':'//div[@class="interaction clearfix"]/span/a[@href="#"]/parent::*/text()',
                                    'collectionNum':'//em[@id="collectionNum"]/text()',
                                    'helpfulNum':'//em[@id="helpfulNum"]/text()',
                                    'unhelpfulNum':'//em[@id="unhelpfulNum"]/text()',
                                    #第二部分不一样
                                    'title':'//div[@class="article-title borderBom"]/div/h1/text()',
                                    'area':'//ul[@class="article-extra borderBom"]/li[1]/div/a/text()',
                                    'type':'//ul[@class="article-extra borderBom"]/li[2]/a/text()',
                                    'tag':'//ul[@class="article-extra borderBom"]/li[3]/div/a/text()',
                                    'attractions':'//ul[@class="article-senior-tags borderBom"]/li[1]/div/a/text()',
                                    'feature':'//ul[@class="article-senior-tags borderBom"]/li[2]/div/a/text()'
                            },
                            "article":{
                                    #第一部分和CommonSenseItem的一样
                                    'author':'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                                    'publishDate':'//div[@class="article-title borderBom"]/p/span[2]/text()',
                                    'content':'//div[@class="article-content"]',
                                    'pvNum':'//em[@id="pvNum"]/text()',
                                    'replyNum':'//div[@class="interaction clearfix"]/span/a[@href="#"]/parent::*/text()',
                                    'collectionNum':'//em[@id="collectionNum"]/text()',
                                    'helpfulNum':'//em[@id="helpfulNum"]/text()',
                                    'unhelpfulNum':'//em[@id="unhelpfulNum"]/text()',
                                    #第二部分不一样
                                    'title':'//div[@class="article-title borderBom"]/div/h1/text()',
                                    'area':'//ul[@class="article-extra borderBom"]/li[1]/div/a/text()',
                                    'type':'//ul[@class="article-extra borderBom"]/li[2]/a/text()',
                                    'tag':'//ul[@class="article-extra borderBom"]/li[3]/div/a/text()',
                                    'attractions':'//ul[@class="article-senior-tags borderBom"]/li[1]/div/a/text()',
                                    'feature':'//ul[@class="article-senior-tags borderBom"]/li[2]/div/a/text()'
                            },
                            "Note":{
                                    #第一部分和NoteItem的一样
                                    'author':'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                                    'date':'//div[@class="article-title borderBom"]/p/span[2]/text()',
                                    'content':'//div[@class="article-content"]',
                                    'pvNum':'//em[@id="pvNum"]/text()',
                                    'replyNum':'//div[@class="interaction clearfix"]/span/a[@href="#"]/parent::*/text()',
                                    'collectionNum':'//em[@id="collectionNum"]/text()',
                                    'helpfulNum':'//em[@id="helpfulNum"]/text()',
                                    'unhelpfulNum':'//em[@id="unhelpfulNum"]/text()',
                                    #第二部分不一样
                                    'area':'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li[4]/a/text()',
                                    'type':'//div[@class="article-title borderBom"]/div/h1/text()'   
                            },
                            "note":{
                                    #第一部分和NoteItem的一样
                                    'author':'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                                    'date':'//div[@class="article-title borderBom"]/p/span[2]/text()',
                                    'content':'//div[@class="article-content"]',
                                    'pvNum':'//em[@id="pvNum"]/text()',
                                    'replyNum':'//div[@class="interaction clearfix"]/span/a[@href="#"]/parent::*/text()',
                                    'collectionNum':'//em[@id="collectionNum"]/text()',
                                    'helpfulNum':'//em[@id="helpfulNum"]/text()',
                                    'unhelpfulNum':'//em[@id="unhelpfulNum"]/text()',
                                    #第二部分不一样
                                    'area':'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li[4]/a/text()',
                                    'type':'//div[@class="article-title borderBom"]/div/h1/text()'   
                            },
                },
                   
                "lvpingSpider":{
                            "Attraction":{
                                    'name':'//h1[@property="v:name"]/text()',
#                                    'address':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
                                    'desc':'//div[@id="hiddenContent"]',
                                    'area':'//div[@class="breadBar"]/a//text()', 
#                                    'descLink':'//div[@class="clearfix"]/div/div[@class="review-intro"]',
#                                    'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
#                                    'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()'
                                    'ticket':'//div[@id="hiddenContent"]/span[2]/following-sibling::p/text()',
                                    'replyNum':'//em[@property="v:count"]/text()',
                                    'popularity':'//div[@class="order_num"]/text()'
                            },                                    
                            "AttractionRegex":{
#                                    'address':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/span/text()',
#                                    'descLink':'//div[@class="clearfix"]/div/div[@class="review-intro"]',
#                                    'popularity':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
#                                    'telNum':'//div[@class="leftContent"]/div[@class="ar-detail"]/ul/li/text()',
                                    'center':'//div[@class="hotel_map_detail"]/div[@class="search_map_blk"]/a/img/@src',
                                    'centerRegex':'center=(\d+[.]?\d*)[,](\d+[.]\d*)[&]*',
                                    'englishName':'//h1[@property="v:name"]/i/text()',
                                    'englishNameRegex':'([\w _-]+)',      
#                                    'area':'//div[@class="breadBar"]/a//text()',    
#                                    'areaRegex':'首页[ -]+(.*)-[^-]*景点'
                                    'traffic':'//div[@id="hiddenContent"]',
                                    'trafficRegex':'<span style="font-weight:bold;.*<span style="font-weight:bold;">',
                            },
                            
                            "Article":{
                                        #第一部分和CommonSenseItem的一样
                                    'author':'//div[@class="memberInfor cf desDistance"]/a[1]/text()',
                                    'publishDate':'//div[@class="memberInfor cf desDistance"]/em/text()',
                                    'content':'//div[@class="yjDetail cf"]',
#                                    'pvNum':'',
                                    'replyNum':'//div[@class="memberInfor cf desDistance"]/a[2]/text()',
#                                    'collectionNum':'',
#                                    'helpfulNum':'',
#                                    'unhelpfulNum':'',
                                        #第二部分不一样
                                    'title':'//div[@class="viewnameShow"]/h1/text()',
                                    'area':'//div[@class="breadBar"]/a//text()',
                                    'type':'//div[@class="breadBar"]/a[5]/text()',
                                    'destination':'//div[@class="breadBar"]/a[4]/text()',
#                                    'tag':'',
#                                    'attractions':'',
#                                    'feature':'',
                            },                            
                            
                            "Note":{
                                        #第一部分和NoteItem的一样
#                                    'author':'',
                                    'publishDate':'//h6[@class="cf"]/span[2]/text()',
                                    'content':'//ul[@class="playAt_detail"]',
#                                    'pvNum':'//em[@id="pvNum"]/text()',
                                    'replyNum':'//h6[@class="cf"]/span[2]/a/text()',
#                                    'collectionNum':'//em[@id="collectionNum"]/text()',
#                                    'helpfulNum':'//em[@id="helpfulNum"]/text()',
#                                    'unhelpfulNum':'//em[@id="unhelpfulNum"]/text()',
                                        #第二部分不一样
                                    'area':'//div[@class="breadBar"]/a//text()',
                                          
                            },
                            
                            "NoteResp":{
                                    'noteType':'url' 
                            },
                            
                            "MemberInfo":{
                                    'name':'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
                                    'ageRange':'//div[@class="aboutmecon"]/dl/dd[5]/em/text()',
                                    'gender':'//div[@class="aboutmecon"]/dl/dd[6]/em/text()',
                                    'currentAddress':'//div[@class="aboutmecon"]/dl/dd[1]/em/text()',
                                    'joinDate':'//div[@class="personalinfor"]/ul/li[2]/p[3]/strong/text()',
                                    'selfIntroduction':'//div[@class="aboutmecon"]/dl/dd[2]/em/text()',
                                    'comsumptionLevel':'//div[@class="aboutmecon"]/dl/dd[3]/em/text()',
                                    'travalPurpose':'//div[@class="aboutmecon"]/dl/dd[4]/em/text()',
                                    'travelPreference':'//div[@class="aboutmecon"]/dl/dd[7]/span//text()',
                                    'travelPartner':'//div[@class="aboutmecon"]/dl/dd[8]/span//text()',
                            },
                            #js方式，暂时爬不到数据
#                                    "MemberTrack":{
#                                    'name':'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
#                                    'gone':'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon01.gif"]/parent::*/a/text()',
#                                    'know':'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon02.gif"]/parent::*/a/text()',
#                                    'like':'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon03.gif"]/parent::*/a/text()',
#                                    'plan':'//div[@class="alldistrict"]/div/ul/div/ul/li/img[@src="/members/img/icon04.gif"]/parent::*/a/text()'
#                                    },
                            "MemberFriend":{
                                    'name':'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
                                    'nameList':'//li[@class="two"]/a/text()',
                                    'cityList':'//li[@class="two"]/span/text()',
#                                    'goneNumList':'//li[@class="three"]/text()',
#                                    'discoverList':'//li[@class="three"]/span/text()',
                                    'linkList':'//li[@class="two"]/a/@href',
                            },
                            "MemberNoteList":{
                                    'author':'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
                                    'titleList':'//dl[@id="showbgcolor"]/dd/strong/a/text()',
                                    'dateList':'//dl[@id="showbgcolor"]/dd/span[1]/text()',
                                    'destinationList':'//dl[@id="showbgcolor"]/dd/q//text()',
                                    'pvNumList':'//dl[@id="showbgcolor"]/dd/span[2]/text()',
                                    'replyNumList':'//dl[@id="showbgcolor"]/dd/span[3]/text()',
                                    'linkList':'//dl[@id="showbgcolor"]/dd/strong/a/@href',
                            },
                            
                            "Region":{
                                    'name':'//div[@class="citynameShow cf"]/strong/text()',
                                    'area':'//div[@class="breadBar"]/a/text()',
                                    'introduction':'//p[@id="city_intro02"]',
                                    'hotHotelLink':'//a[@id="link_hotels_lc"]/@href',
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
                                    'abstract':'//div[@class="center"]/div[@class="leftside"]/div[@class="leftside_top"]/div[@class="leftside_col"]/text()',
                                    'publishDate':'//div[@class="center"]/div[@class="leftside"]/div[@class="leftside_top"]/div[@class="zxd_artinfo"]/span[1]/text()',
                            },
                },
                   
                "lotourSpider":{
                            "Article1":{
                                    'title':'//div[@class="dzw_main"]/div[@class="dzw_left"]/div[@class="dzw_lefta"]/div[@class="dzw_leftat"]/div[@class="dzw_leftatl"]/h1/text()',
                                    'publishDate':'//div[@class="dzw_main"]/div[@class="dzw_left"]/div[@class="dzw_lefta"]/div[@class="dzw_leftat"]/div[@class="dzw_leftatl"]/p/span[1]/text()',
                                    'content':'//div[@class="dzw_main"]/div[@class="dzw_left"]/div[@class="dzw_lefta"]/div[@class="dzw_leftam"]',
                                    'destination':'//div[@class="dzw_main"]/div[@class="dzw_left"]/div[@class="dzw_lefta"]/div[@class="dzw_leftxgmdd"]/div[@class="dzw_leftxgmddt"]/h1/a/text()',
                            },
                            "Article1Regex":{
                                    'author':'//div[@class="dzw_main"]/div[@class="dzw_left"]/div[@class="dzw_lefta"]/div[@class="dzw_leftat"]/div[@class="dzw_leftatl"]/p/span[3]/text()',
                                    'authorRegex':u'作者：'+'\s*(.*)',
                            },
                            "Article2":{
                                    'title':'//div[@id="maincontent"]/h6/text()',
                                    'content':'//div[@id="maincontent"]/div[@class="mccont02"]',
                            },
                            "Article2Regex":{
                                    'publishDate':'//div[@id="maincontent"]/p[@class="mcplp"]/span[@class="mtile"]/text()',
                                    'publishDateRegex':'(\d{4}-\d{1,2}-\d{1,2})',
                            },
                },
                   
                "sinaSpider":{
                            'Article1':{
                                    'title':'h1[@id="artibodyTitle"]/text()',
                                    'publishDate':'//span[@id="pub_date"]/text()',
                                    'content':'//div[@id="artibody"]',
                                    'destination':'//p[@id="lo_links"]/a[4]/text()',
                            },
                },
                "hexunSpider":{
                            'Article':{
                                    'title':'//div[@id="artibodyTitle"]/h1/text()',
                                    'publishDate':'//div[@id="artibodyTitle"]/div[@class="a"]/span[@class="gray"]/text()',
                                    'content':'//div[@id="artibody"]',
                            },
                },
                "peopleSpider":{
                            'Article':{
                                    'title':'//h1[@id="p_title"]/text()',
                                    'publishDate':'//span[@id="p_publishtime"]/text()',
                                    'content':'//div[@id="p_content"]',
                            },
                },
                "sohuSpider":{
                            'Article1':{
                                    'title':'//div[@id="contentA"]/div[@class="left"]/h1/text()',
                                    'content':'//div[@id="contentText"]',
                                    'publishDate':'//div[@id="contentA"]/div[@class="left"]/div[@class="sourceTime"]/div[@class="r"]/text()',
                            },
                            'Article1Regex':{
                                    'author':'//div[@id="contentA"]/div[@class="left"]/div[@class="sourceTime"]/div[@class="l"]/text()',
                                    'authorRegex':u'作者：'+'\s*(.*)[\s]*',
                            },
                            'Article2':{
                                    'title':'//table/tbody/tr/td[@class="c_title bold"]/text()',
                                    'content':'//td[@id="fontzoom"]'
                            },
                            'Article2Regex':{
                                    'publishDate':'//table[@bgcolor="#d4e8f9"]/form/tbody/tr/td[@class="pd3"]/text()',
                                    'publishDateRegex':u'时间：'+'(\S+)',
                            },
                },
#                "bbkerSpider":{
#                            'Article':{
#                                    'content':'//div[@id="pageright"]/div[@class="doc"]/div[@class="doccol"]/div[@class="info"]/ul[normalize-space(li)="地图:"]/parent::*/following-sibling::*[@*]',
#                                    'title':'//div[@id="pageright"]/div[@class="doc"]/div[@class="doccol"]/center/text()',
#                                    'author':'//div[@class="info"]/ul[count(li)=5]/li[1]/a/text()',
#                            },
#                            'ArticleRegex':{
#                                    'geotag':'//div[@class="info"]/ul[normalize-space(li)="地理标签:"]',
#                                    'geotagRegex':'<a\s*[^>]*\s*>(.*?)<\s*/a\s*>',
#                                    'tag':'//div[@class="info"]/ul[normalize-space(li)="标签:"]',
#                                    'tagRegex':'<a\s*[^>]*\s*>(.*?)<\s*/a\s*>',
#                                    'publishDate':'//div[@class="info"]/ul[count(li)=5]/li[4]/text()',
#                                    'publishDateRegex':u'发表:\s*'+'(.*)',
#                            },
#                },
                "21cnSpider":{
                            'Article':{
                                    'title':'//div[@id="text"]/div[@class="bd"]/h1/text()',
                                    'publishDate':'//div[@id="text"]/div[@class="bd"]/address/span[@class="time"]/text()',
                                    'content':'//div[@id="text"]/div[@class="bd"]/address/following-sibling::*[name()!="div"]',
                            },
                },
                "bytravelSpider":{
                            'Article1':{
                                    'title':'//table/tr/th[@bgcolor="f7f8f9"]/h1/text()',
                                    'content':'//td[@class="f14"]/font[@class="f14"]/div[@class="f14b"]/preceding-sibling::*'
                            },
                            'Article1Regex':{
                                    'destination':'//table/tr/th[@bgcolor="f7f8f9"]/following-sibling::script/text()',
                                    'destinationRegex':'="(.*)"',
                            },
                            'Article2':{
                                    'title':'//table/tr/td/div/a/span[@class="title"]/text()',
                                    'content':'//tbody/tr/td[@valign="top"]',
                            },
                            'Article2Regex':{
                                    'destination':'//td[@class="f12"]/span[@class="t360"]/strong/a[last()]/text()',
                                    'destinationRegex':'(.*)'+u'特产',
                            },
                },
                "yahooSpider":{
                            'Article1':{
                                    'title':'//div/div/div/div/h1/text()',
                                    'content':'//div[@class="text-area"]/div[@class="text fixclear"]|//div[@id="bd"]/div[@class="main"]/div[@class="bak con text"]/div[@class="imp"]/div[@class="bd"]'
                                    
                            },
                            'Article1Regex':{
                                    'publishDate':'//div/div/div/div/span/text()',
                                    'publishDateRegex':'(\d{4}-\d{1,2}-\d{1,2}\s*\d{2}:\d{2})',
                            },
                            'Article2':{
                                    'title':'//div[@class="summary_box border"]/div[@class="subtitle"]/h2[@class="tit"]/span/text()',
                                    'destination':'//div[@class="summary_box border"]/div[@class="subtitle"]/h2[@class="tit"]/a/text()',
                                    'content':'//div[@class="summary_box border"]/div[@class="body"]'
                            },
                            'Article3':{
                                    'title':'//div[@id="bd"]/div[@class="main"]/div[@class="con mod-other"]/div[@class="title"]/h1/text()',
                                    'content':'//div[@class="text-area"]/div[@class="text fixclear"]'
                            },
                            'Article3Regex':{
                                    'publishDate':'//div[@id="bd"]/div[@class="main"]/div[@class="con mod-other"]/div[@class="title"]/span/text()',
                                    'publishDateRegex':'(\d{4}-\d{1,2}-\d{1,2}\s*\d{2}:\d{2})',
                                    'author':'//div[@id="bd"]/div[@class="main"]/div[@class="con mod-other"]/div[@class="title"]/span/text()',
                                    'authorRegex':u'发布人：'+'(.*)',
                            },
                },
                "lvrenSpider":{
                            'Article2':{
                                    'title':'//div[@id="guide_main"]/div[@class="clear"]/div[@class="left"]/h1[@class="guide"]/span[@class="o"]/text()',
                                    'destination':'//div[@class="tc-header-logo tc-container"]/div[@class="tc-center-container"]/div[@class="tc-logo"]/div[@class="tc-title"]/strong/text()',
                                    'content':'//img[@id="jiathis_a"]/parent::*/parent::*/following-sibling::*'
                            },
                            'Article3':{
                                    'title':'//div[@id="container"]/h1/text()',
                                    'author':'//div[@id="main"]/div/a[@class="blue uline"]/text()',
                                    'publishDate':'//div[@id="main"]/div/span[@class="gray"]/text()',
                                    'destination':'//div[@class="tc-header-logo tc-container"]/div[@class="tc-center-container"]/div[@class="tc-logo"]/div[@class="tc-title"]/strong/text()',
                                    'content':'//div[@id="main"]/div[1]/following-sibling::*[@class!="sbox"]',
                            },
                },
                "BBsSpider":{
                            'Article':{
#                                    'text':'//body/table/preceding::*',
                            },
                            'ArticleRegex':{
                                    'title':'//body',
                                    'titleRegex':u'标题'+':\s*</b>([^<>]*?)\s*<br',
                                    'author':'//body',
                                    'authorRegex':u'</b>([^<>]*?)\s+<b>[^<>]*</b>[^<>]*<b>标题',
                                    'publishDate':'//body',
                                    'publishDateRegex':u'(\d{4}-\d{1,2}-\d{1,2}\s*\d{2}:\d{2}).*?<b>标题',
                                    'content':'//body',
                                    'contentRegex':'\>([^<>]+?)<|(<img[^<]*>)',
                            },
                },
}