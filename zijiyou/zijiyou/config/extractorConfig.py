# -*- coding: utf-8 -*-

extractorConfig = {
                "bbkerSpider":{
                               "KeyList":{"keyWords":'//div[@class="doc"]/div[@class="col"]/div[@class="taglist"]/span//text()'},
                               },
                "baseSeSpider":{
                                "Article":{
                                           'mainext':True,
                                           }
                                },
                "daodaoSpider":{
                                'threshold':0.40,
                                "Attraction":{
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
                                            'feature':'//ul[@class="article-senior-tags borderBom"]/li[2]/div/a/text()',
                                            
                                            },
                                "Note":{
                                        #第一部分和NoteItem的一样
                                        'author':'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                                        'date':'//div[@class="article-title borderBom"]/p/span[2]/text()',
                                        'content':'//div[@class="article-content"]',
                                        'pvNum':'//em[@id="pvNum"]/text()',
                                        'collectionNum':'//em[@id="collectionNum"]/text()',
                                        'helpfulNum':'//em[@id="helpfulNum"]/text()',
                                        'unhelpfulNum':'//em[@id="unhelpfulNum"]/text()',
                                        #第二部分不一样
                                        'area':'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li[4]/a/text()',
                                        'type':'//div[@class="article-title borderBom"]/div/h1/text()',
                                        'title':'//div[1]/div/h1/text()'
                                        },
                                "NoteRegex":{
                                            'replyNum':'//div[2]/span[2]/text()',
                                            'replyNumRegex':'(\d+)',
                                            },
                                "note":{
                                        #第一部分和NoteItem的一样
                                        'author':'//div[@class="article-title borderBom"]/p/span/span[@class="fkLnk hvrIE6"]/text()',
                                        'date':'//div[@class="article-title borderBom"]/p/span[2]/text()',
                                        'content':'//div[@class="article-content"]',
                                        'pvNum':'//em[@id="pvNum"]/text()',
                                        'collectionNum':'//em[@id="collectionNum"]/text()',
                                        'helpfulNum':'//em[@id="helpfulNum"]/text()',
                                        'unhelpfulNum':'//em[@id="unhelpfulNum"]/text()',
                                        #第二部分不一样
                                        'area':'//div[@id="MAIN"]/div[@class="crumbs"]/ul/li/ul/li[4]/a/text()',
                                        'type':'//div[@class="article-title borderBom"]/div/h1/text()',
                                        'title':'//div[1]/div/h1/text()'
                                        },
                                "noteRegex":{
                                        'replyNum':'//div[2]/span[2]/text()',
                                        'replyNumRegex':'(\d+)',
                                        }
                                },
                   
                "lvpingSpider":{
                                'threshold':0.40,
                                "Attraction":{
                                              'name':'//h1[@property="v:name"]/text()',
                                              'desc':'//div[@id="hiddenContent"]',
                                              'area':'//div[@class="breadBar"]/a//text()', 
                                              'ticket':'//div[@id="hiddenContent"]/span[2]/following-sibling::p/text()',
                                              'replyNum':'//em[@property="v:count"]/text()',
                                              'popularity':'//div[@class="order_num"]/text()'
                                              },                                    
                                "AttractionRegex":{
                                                    'center':'//div[@class="hotel_map_detail"]/div[@class="search_map_blk"]/a/img/@src',
                                                    'centerRegex':'center=(\d+[.]?\d*)[,](\d+[.]\d*)[&]*',
                                                    'englishName':'//h1[@property="v:name"]/i/text()',
                                                    'englishNameRegex':'([\w _-]+)',      
                                                    'traffic':'//div[@id="hiddenContent"]',
                                                    'trafficRegex':'<span style="font-weight:bold;.*<span style="font-weight:bold;">',
                                                    },
                                
                                "Article":{
                                            #第一部分和CommonSenseItem的一样
                                            'author':'//div[@class="memberInfor cf desDistance"]/a[1]/text()',
                                            'publishDate':'//div[@class="memberInfor cf desDistance"]/em/text()',
                                            'content':'//div[@class="yjDetail cf"]',
                                            'replyNum':'//div[@class="memberInfor cf desDistance"]/a[2]/text()',
                                                #第二部分不一样
                                            'title':'//div[@class="viewnameShow"]/h1/text()',
                                            'area':'//div[@class="breadBar"]/a//text()',
                                            'type':'//div[@class="breadBar"]/a[5]/text()',
                                            'destination':'//div[@class="breadBar"]/a[4]/text()',
                                            },                            
                                
                                "Note":{
                                        #第一部分和NoteItem的一样
                                        'title':'//form[@id="newMasterForm"]/div[4]/div[2]/div[2]/h1/text()',
                                        'publishDate':'//form[@id="newMasterForm"]/div[4]/div[2]/div[3]/div[1]/div[1]/h6/span/text()',
                                        'content':'//form[@id="newMasterForm"]//ul[@class="playAt_detail"]',
                                        #第二部分不一样
                                        'area':'//form[@id="newMasterForm"]/div[4]/div[2]/div[1]//text()',
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
                                "MemberFriend":{
                                                'name':'//div[@class="personalinfor"]/ul/li[2]/p[1]/strong/text()',
                                                'nameList':'//li[@class="two"]/a/text()',
                                                'cityList':'//li[@class="two"]/span/text()',
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
                                'threshold':0.75, 
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
                                  'threshold':0.5,
                                  "Article":{
                                            'author':'//div[2]/div[1]/span[1]/a/text()',
                                            'publishDate':'//div[2]/div[1]/span[2]/text()',
                                            'title':'//div[1]/h1/text()',
                                            'content':'//div[@id="pnl_contentinfo"]',
                                            'destination':'//div[@class="r_con"]/div[@class="xg_mdd"]/div[@class="mdd_name"]/a/text()',
                                            },
                                  "Profile":{
                                             'error':'error'
                                             },
                                  "POI":{
                                        'name':'//div[@class="main_nav"]/div[@class="mddtit"]/h1/text()',
                                        'area':'//div[@class="spot_head"]/div[@class="l_area"]/div[@class="spot_name"]/text()',
                                        },
                                  },
                "sozhenSpider":{
                                'threshold':0.40,
                                "Article":{
                                           'author':'//div[2]/div[2]/div[1]/ul/li[1]/text()',
                                           'publishDate':'//div[2]/div[2]/div[1]/ul/li[2]/text()',
                                           'title':'//div[2]/div[2]/div[2]/div[1]/h4/text()',
                                           'content':'//div[2]/div[2]/div[2]/div[2]/div[2]/div[2]',
                                           'destination':'//div[2]/div[2]/div[2]/div[2]/div[1]/h2/text()',
                                           },
                                "Article1":{
                                            'author':'//div[2]/div[1]/div[1]/ul/li[2]/text()',
                                            'publishDate':'//div[2]/div[1]/div[1]/ul/li[1]/text()',
                                            'title':'//div[2]/div[1]/div[1]/h3/text()',
                                            'content':'//div[2]/div[1]/div[2]',
                                            'destination':'//div[2]/div[2]/div/div[1]/dl',
                                            },
                                "Article2":{
                                            'title':'//div[2]/div[2]/div[2]/div[2]/div[1]/h4/text()',
                                            'author':'//div[2]/div[2]/div[2]/div[2]/div[1]/ul/li[1]/text()',
                                            'publishDate':'//div[2]/div[2]/div[2]/div[2]/div[1]/ul/li[2]/text()',
                                            'content':'//div[2]/div[2]/div[2]/div[2]/div[2]',
                                            'destination':'//form/div[2]/div[2]/div[1]//dd//text()',
                                            },
                                "POI":{
                                       'name':'//div[@class="main_nav"]/div[@class="mddtit"]/h1/text()',
                                       'area':'//div[@class="spot_head"]/div[@class="l_area"]/div[@class="spot_name"]/text()',
                                       },
                                },
                   
                "17uSpider":{
                             'threshold':0.4,
                             #第一部分
                            "Article1":{
                                        'mainext':True,
#                                        'title':'//div[@id="bArticleContent"]/div[8]/font',
#                                        'author':'//div[@id="bArticleBody"]/div[1]/span/a/text()',
#                                        'publishDate':'//div[@id="bArticleBody"]/div[1]/span/text()',
#                                        'content':'//div[@id="bArticleContent"]',
                                        },
                            "Article2":{
                                        'mainext':True,
#                                        'title':'//div[@class="center"]/div[@class="leftside"]/div[@class="leftside_top"]/h2[@class="leftside_head"]/text()',
#                                        'content':'//div[@id="infor_main"]',
#                                        'publishDate':'//div[@class="center"]/div[@class="leftside"]/div[@class="leftside_top"]/div[@class="zxd_artinfo"]/span[1]/text()',
                                        },
                            "Article3":{
                                        'mainext':True,
#                                        'title':'//div[@id="bArticleBody"]/div[1]/h3/text()',
#                                        'content':'//div[@id="bArticleContent"]/div[6]',
#                                        'publishDate':'//div[@id="bArticleBody"]/div[1]/span/text()',
                                        }
                             },
                "lotourSpider":{
                                'threshold':0.40,
                                "Article1":{
                                            'title':'//div[@id="maincontent"]/h6//text()',
                                            'publishDate':'//div[@id="maincontent"]/p[1]/span/text()',
                                            'content':'//div[@id="zoom"]',
                                            'destination':'//td[2]/ul/li//text()',
                                            },
                                "Article2":{
                                            'title':'//div[5]/div[1]/div[1]/div[1]/div[1]/h1/text()',
                                            'publishDate':'//div[5]/div[1]/div[1]/div[1]/div[1]/p/span[1]/text()',
                                            'content':'//div[1]/div[5]/div[1]/div[1]/div[2]',
                                            'destination':'//body/div[1]/div[4]/div[2]//text()',
                                            },
                                "Article2Regex":{
                                                 'publishDate':'//div[@id="maincontent"]/p[@class="mcplp"]/span[@class="mtile"]/text()',
                                                 'publishDateRegex':'(\d{4}-\d{1,2}-\d{1,2})',
                                                },
                                },
                "sinaSpider":{
                              'threshold':0.45,
                              'Article1':{
                                          'mainext':True,
#                                         'title':'//h1[@id="artibodyTitle"]/text()',
#                                         'publishDate':'//span[@id="pub_date"]/text()',
#                                         'content':'//div[@id="artibody"]',
                                            },
                                'Article2':{
                                            'mainext':True,
#                                            'title':'//div[@id="artibodyTitle"]/h1/text()',
#                                            'publishDate':'//div[@id="artibodyTitle"]/div/text()',
#                                            'content':'//div[@id="artibody"]',
                                            },
                              },
                "hexunSpider":{
                               'threshold':0.40,
                               'Article':{
                                          'title':'//div[@id="mainbox"]/div[2]/p[1]/text()',
                                          'publishDate':'//div[@id="mainbox"]/div[2]/div[1]/font/text()',
                                          'content':'//div[@id="mainbox"]/div[2]/div[3]/div',
                                          },
                               },
                "peopleSpider":{
                                'threshold':0.40,
                                'Article':{
                                           'title':'//div[@id="p_title"]/text()',
                                           'publishDate':'//div[@id="p_publishtime"]/text()',
                                           'content':'//div[@id="p_content"]',
                                           },
                                'Article2':{
                                            'title':'//table[3]//tr[1]/td[1]/table[2]//tr[2]/td/text()',
                                            'publishDate':'//body/div/table[3]//tr[1]/td[1]/table[3]//tr[2]/td[2]/text()',
                                            'content':'//font[@id="zoom"]',
                                            },
                                },
                "sohuSpider":{
                              'threshold':0.40,
                              'Article1':{
                                          'title':'//div[1]/div[1]/h1/text()',
                                          'content':'//div[@id="sohu_content"]',
                                          'publishDate':'//div[1]/div[1]/div[1]/span/text()',
                                          },
                              'Article2':{
                                          'title':'//table[2]//tr[2]/td[1]/table[2]//tr[2]/td//text()',
                                          'content':'//table[4]//tr[4]',
                                          'publishDate':'//table[2]//tr[2]/td[1]/table[3]//tr/td[1]/text()',
                                          }
                              },
                "bbkerSpider":{
                               'threshold':0.40,
                               'Article':{
                                          'mainext':True,
#                                          'content':'//div[@id="pageright"]/div/div[2]',
#                                          'title':'//div/div[2]/center/h2/text()',
#                                          'author':'//div[@class="info"]/ul[count(li)=5]/li[1]/a/text()',
#                                          'publishDate':'//div[@class="info"]/ul[count(li)=5]/li[4]/text()',
                                          }
                               },
                "lvyou114Spider":{
                                  'threshold':0.5,
                                  'Article':{
                                            'content':'//div[1]/div[1]/div[4]',
                                            'title':'//div[3]/div[1]/div[1]/div[1]/h1/text()',
                                            'author':'//div[1]/div[1]/div[2]/a[3]/text()',
                                            'publishDate':'//div[3]/div[1]/div[1]/div[2]/text()',
                                            }
                                  },
                "21cnSpider":{
                              'threshold':0.50,
                              'Article':{
                                         'mainext':True,
#                                         'title':'//div[@id="wrap"]//div[1]/div[2]/h2/text()',
#                                         'publishDate':'//div[@id="wrap"]//div[1]/div[2]/div/div/span/text()',
#                                         'content':'//div[@id="text"]',
                                         },
                              'Article2':{
                                          'mainext':True,
#                                          'title':'//div[@id="text"]/div/h1/text()',
#                                          'publishDate':'//div[@id="text"]/div/address/span[1]/text()',
#                                          'content':'//div[@id="text"]/div/p',
                                          }
                              },
                "bytravelSpider":{
                                  'threshold':0.75,
                                  'Article1':{
                                              'mainext':True,
#                                              'title':'//table[2]//tr[1]/th/h1/text()',
#                                              'content':'//table[2]//tr[4]/td/div/font',
                                              },
                                  'Article2':{
                                              'mainext':True,
#                                              'title':'//table[2]//tr[1]/th/h1/text()',
#                                              'content':'//table[2]//tr/td[1]/table[2]//tr[2]/td',
                                              }
                                  },
                "yahooSpider":{
                               'threshold':0.40,
                               'Article1':{
                                           'title':'//div/div/div/div/h1/text()',
                                           'content':'//div[@class="text-area"]/div[@class="text fixclear"]|//div[@id="bd"]/div[@class="main"]/div[@class="bak con text"]/div[@class="imp"]/div[@class="bd"]',
                                           },
                               'Article1Regex':{
                                                'publishDate':'//div/div/div/div/span/text()',
                                                'publishDateRegex':'(\d{4}-\d{1,2}-\d{1,2}\s*\d{2}:\d{2})',
                                                },
                               'Article2':{
                                           'title':'//div[@class="summary_box border"]/div[@class="subtitle"]/h2[@class="tit"]/span/text()',
                                           'destination':'//div[@class="summary_box border"]/div[@class="subtitle"]/h2[@class="tit"]/a/text()',
                                           'content':'//div[@class="summary_box border"]/div[@class="body"]',
                                           },
                               'Article3':{
                                           'title':'//div[@id="bd"]/div[@class="main"]/div[@class="con mod-other"]/div[@class="title"]/h1/text()',
                                           'content':'//div[@class="text-area"]/div[@class="text fixclear"]',
                                           },
                               'Article3Regex':{
                                                'publishDate':'//div[@id="bd"]/div[@class="main"]/div[@class="con mod-other"]/div[@class="title"]/span/text()',
                                                'publishDateRegex':'(\d{4}-\d{1,2}-\d{1,2}\s*\d{2}:\d{2})',
                                                'author':'//div[@id="bd"]/div[@class="main"]/div[@class="con mod-other"]/div[@class="title"]/span/text()',
                                                'authorRegex':u'发布人：'+'(.*)',
                                                },
                               },
                "lvrenSpider":{
                               'threshold':0.40,
                               'Article2':{
                                           'title':'//div[@id="guide_main"]/div[@class="clear"]/div[@class="left"]/h1[@class="guide"]/span[@class="o"]/text()',
                                           'destination':'//div[@class="tc-header-logo tc-container"]/div[@class="tc-center-container"]/div[@class="tc-logo"]/div[@class="tc-title"]/strong/text()',
                                           'content':'//img[@id="jiathis_a"]/parent::*/parent::*/following-sibling::*',
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
                             'threshold':0.40,
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
                             'BBSArticle':{
                                           },
                             'BBSArticleRegex':{
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
                'QQBlogSpider':{
                                'Article':{
                                            'mainext':True,
                                            }
                                },
                'onegreenSpider':{
                                  'ImageItem':{
                                               'name':'//body/table[1]//tr[1]/td/span/text()',
                                               'imageUrls':'//body/table[2]//tr/td//img/@src',
                                               },
                                  },
                   }