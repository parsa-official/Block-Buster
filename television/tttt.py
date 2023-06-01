from imdb import Cinemagoer

imdb_id = '0903747'  # Example IMDb ID for "Breaking Bad
ia = Cinemagoer()
movie = ia.get_movie(imdb_id)

# Fetch the genre names from the Genre model

print(movie['endyear'])

#['localized title', 'cast', 'genres', 'runtimes', 'countries', 'country codes', 'language codes', 'color info', 
# 'aspect ratio', 'sound mix', 'box office', 'certificates', 'original air date', 'rating', 'votes', 'cover url', 'imdbID',
#  'videos', 'plot outline', 'languages', 'title', 'year', 'kind', 'original title', 'director', 'writer', 'producer', 
# 'composer', 'cinematographer', 'editor', 'editorial department', 'casting director', 'production design', 'art direction', 
# 'set decoration', 'costume designer', 'make up', 'production manager', 'assistant director', 'art department', 'sound crew',
#  'special effects', 'visual effects', 'stunt performer', 'camera and electrical department', 'casting department', 'costume department',
#  'location management', 'music department', 'script department', 'transportation department', 'miscellaneous crew', 'thanks', 'akas', 
# 'top 250 rank', 'production companies', 'distributors', 'special effects companies', 'other companies', 'plot', 'synopsis', 'canonical title',
#  'long imdb title', 'long imdb canonical title', 'smart canonical title', 'smart long imdb canonical title', 'full-size cover url']

