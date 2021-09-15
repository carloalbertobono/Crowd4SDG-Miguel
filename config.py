# TAGS for sharing keys and values between templates and code

d = {}
d['nsfw_tag'] = "Remove not-safe-for-work images"
d['duplicates_tag'] = "Remove near-duplicate images"
d['meme'] = "Remove non-photos"
d['flood_tag'] = "Select event: flooding"
d['scene_tag'] = "Select scene:"
d['object_tag'] = "Select object (YOLO):"
d['object_tag_detr'] = "Select object (DETR):"
d['post_location_tag'] = "Add location information"
d['user_location_tag'] = "Add user country"
d['user_location_sel_tag'] = "Select user location:"

def get_tags():
    return d