from icrawler.builtin import BingImageCrawler

crawler = BingImageCrawler(
    storage={'root_dir': r'C:\Users\sungh\OneDrive\바탕 화면\study\classification_study\data\test\cats'}
)

crawler.crawl(
    keyword='real cat -cartoon -drawing -clipart -logo', 
    max_num=300
)
