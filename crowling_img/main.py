from icrawler.builtin import BingImageCrawler

crawler = BingImageCrawler(storage={'root_dir': r'C:\study\crowling_img\data'})
    
crawler.crawl(
    keyword='real ship top view ', 
    max_num=350
)