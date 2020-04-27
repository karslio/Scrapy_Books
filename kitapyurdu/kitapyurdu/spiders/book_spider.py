import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    page_count = 0
    book_count = 1
    file = open('books.txt', 'a', encoding='utf-8')
    start_urls = ["http://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&filter_in_stock=1&filter_in_stock=1&page=1"]

    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text").getall()
        book_authors = response.css("div.author.compact.ellipsis  a::text").getall()
        book_publishers = response.css("div.publisher > span > a > span::text").getall()
        i = 0 
        while i < len(book_names):
            # yield {
            #     "name": book_names[i],
            #     "author": book_authors[i],
            #     "publisher": book_publishers[i]               
            # }
            self.file.write("-------------------------------------------\n")
            self.file.write(str(self.book_count) + ".\n")
            self.file.write("Kitap Ismi : " +book_names[i] + "\n")
            self.file.write("Yazar : " +book_authors[i] + "\n")
            self.file.write("Yayinevi : " + book_publishers[i] + "\n")
            self.book_count +=1
            i += 1

        next_url = response.css("a.next::attr(href)").get()
        self.page_count += 1

        if next_url is not None and self.page_count != 5:
            yield scrapy.Request(url = next_url, callback = self.parse)
        else:
            self.file.close()
        
            
