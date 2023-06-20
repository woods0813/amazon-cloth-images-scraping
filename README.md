# amazon-cloth-images-scraping

Uses the requests library and beatufiul soup to process the html code
from amazon pages and grab clothing images

The idea was to use the images for an object detection dataset, but other
datasets proved to be more extensive and applicable.

Still could be used as an efficient way to grab large amounts of information off
of amazon.

The amazon_category_images file is what sends the primary requests, by surfing
through the catalog of each clothing section thats desired and starting at page 2
(page 1 has a different identifier then the rest), and continuing to the next page
in order so as to make it appear as though its a real shopper

get_links then gets the appropriate links which correspond to products and jumpts to that
product page

get_images then goes through the product page to find the primary picture of the desired product
(there are many images on every product page)

Example Images: 

Coats & Jackets

![31i+ceN3z7L _SX342_SY445_](https://github.com/woods0813/amazon-cloth-images-scraping/assets/114941826/f02f5cf5-3c9e-4353-8ad0-96c6e73b312c)

Dresses

![41DrfcbToRL __AC_SX342_SY445_QL70_ML2_](https://github.com/woods0813/amazon-cloth-images-scraping/assets/114941826/57f19dab-e10c-430e-a8b9-da95108930ea)

Tops & Tees

![51+Jtncs5wL_AC_SX342_SY445_](https://github.com/woods0813/amazon-cloth-images-scraping/assets/114941826/ba68403d-2bcb-4a45-bee0-0d4c51df921e)
