get_pixivly
===========

Downloading Daily Top 50 of Illustrations on [Pixiv.net](http://www.pixiv.net/) for further research. :smile:

### Usage

You need to modify `pixiv/settings.py`. `IMAGES_STORE` for images and `JSONS_STORE` for jsons.

To download the images and meta data, simply rum commamnd shown below.

```
$ scrapy crawl pixiv
OR
$ scrapy crawl pixiv -a start=today -a end=20150101
```
