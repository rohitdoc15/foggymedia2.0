from google_images_search import GoogleImagesSearch

def search_images(search_term):
    # Set your API key and CX
    api_key = 'AIzaSyA6BUZRAWF3imUWzPyMs6D2ZdF7Jrz6H4Q'
   
    
    # Create a GoogleImagesSearch object
    gis = GoogleImagesSearch(api_key, cx)
    
    # Set the search parameters
    _search_params = {
        'q': search_term,
        'num': 5,  # Number of images to retrieve
    }
    
    # Perform the image search
    gis.search(search_params=_search_params)
    
    # Get the image URLs from the results
    image_urls = [image.url for image in gis.results()]
    
    return image_urls
