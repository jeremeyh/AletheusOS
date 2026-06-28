class ListingParser:
    @staticmethod
    def normalize(raw):
        return {
            "title": raw.get("title",""),
            "price": raw.get("price",0),
            "url": raw.get("url",""),
            "marketplace": raw.get("marketplace","")
        }
