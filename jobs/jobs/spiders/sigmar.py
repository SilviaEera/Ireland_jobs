# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SigmarSpider(CrawlSpider):
    name = 'sigmar'
    allowed_domains = ['www.sigmarrecruitment.com']
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url = "https://www.sigmarrecruitment.com/jobs/?utf8=%E2%9C%93&search%5Bquery%5D=python+&seo_location=&commit=", headers= {
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths= "//div[@class='job-title']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths= "//span[@class='next']/a"))
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'Job Title': response.xpath("//header[@class='big-job-title']/h1/text()").get(),
            'Company Phone': response.xpath("//li[@class='job_contact_phone']/p[2]/text()").get(),
            'Location': response.xpath("//li[@class='location']/p[2]/text()").get(),
            'Salary': response.xpath("//li[@class='job_salary']/p[2]/text()").get(),
            'Job Type': response.xpath("//li[@class='job_type']/p/a/text()").get(),
            'Job Posted': response.xpath("//li[@class='job_posted']/p[2]/text()").get(),
            'Company Address': response.xpath("//li[@class='location']/p[2]/text()").get(),
            'Consultant': response.xpath("//li[@class='name']/a/text()").get().replace("\t","").replace("\n","").strip(),
            'Consultant Email': response.xpath("//li[@class='email']/a/text()").get().replace("\t","").replace("\n","").strip(),
            'Consultant Phone': response.xpath("//li[@class='phone']/a/text()").get().replace("\t","").replace("\n","").strip(),
            'Job Link': response.request.url
        }
