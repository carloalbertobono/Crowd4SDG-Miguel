# TAGS for sharing keys and values between templates and code

d = {}
d['nsfw_tag'] = "Remove not-safe-for-work images"
d['duplicates_tag'] = "Remove near-duplicate images"
d['meme'] = "Remove non-photos"
d['flood_tag'] = "Select event: flooding"
d['scene_tag'] = "Select scene:"
d['person_tag'] = "Select persons"
d['object_tag'] = "Select object:"
d['object_tag_detr'] = "Select object (DETR):"
d['post_location_tag'] = "Show post locations on a map"
d['user_location_tag'] = "Add author locations"
d['user_location_sel_tag'] = "Select authors from:"


def get_tags():
    return d
