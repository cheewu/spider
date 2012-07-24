# -*- coding: utf-8 -*-
lvpingSpider={
        'allowedDomains':["www.lvping.com"],
        'startUrls':[
        'http://www.lvping.com/Journals.aspx?type=0&dname=&title=&tag=0&tagn=&author=&group=0&orderby=&pageno=1', #最新发表攻略第1页
        'http://www.lvping.com/Journals.aspx?type=0&dname=&title=&tag=0&tagn=&author=&group=0&orderby=&pageno=2', #最新发表攻略第2页
        'http://www.lvping.com/Journals.aspx?type=0&dname=&title=&tag=0&tagn=&author=&group=0&orderby=&pageno=3', #最新发表攻略第3页
        'http://www.lvping.com/Journals.aspx?type=0&dname=&title=&tag=0&tagn=&author=&group=0&orderby=&pageno=4', #最新发表攻略第4页
      
        ],
        
        #普通list页正则表达式
        'normalRegex':[
            {
            #游记总页分页，如：http://www.lvping.com/Journals.aspx?type=0&dname=&title=&tag=0&tagn=&author=&group=0&orderby=&pageno=4
            'regex':r'/Journals\.aspx\?type=0&dname=&title=&tag=0&tagn=&author=&group=0&orderby=&pageno=\d+$', 
            'priority':200
            }
        ],
        
        #item页正则表达式 type对应item存放的数据表名
        'itemRegex':[
        {
            #游记、攻略文章，如：http://www.lvping.com/showjournal-d439-r1334987-journals.html
            'itemCollectionName':'Article',
            'regex':r'/showjournal\-d\d+-r\d+\-journals\.html$', 
            'priority':1000
        }, 
        {
            #游记、攻略文章，如：http://www.lvping.com/journals/AllSingleJournals.aspx?Writing=1334950
            'itemCollectionName':'Article',
            'regex':r'/journals/AllSingleJournals\.aspx\?Writing=\d+$', 
            'priority':1000
        }
        ],
        'imageXpath':['//div[@class="yjDetail cf"]//img/@src']
    }