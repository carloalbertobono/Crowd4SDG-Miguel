# TAGS for sharing keys and values between templates and code

d = {}
d['nsfw_tag'] = "Remove not safe for work"
d['duplicates_tag'] = "Remove near duplicates"
d['meme'] = "Remove non-photos"
d['flood_tag'] = "Flood detector"

def get_tags():
    return d