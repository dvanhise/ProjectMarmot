from game_objects.tag import Tag


# Placeholder tag for tooltip functionality
class Ward(Tag):
    id = 'ward'
    name = 'Ward'
    icon = 'ward'
    tooltip = "Protects a node from opponent scripts.  Does not stack;  Ward application replaces existing ward."
