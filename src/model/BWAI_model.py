'''
BWAI Database Controller Framework
'''

#posts Table
class BWAI__posts(object):
    def __init__(self, client):
        super(BWAI__posts, self).__init__()
        self.collection = client['posts2']

        #Basic projection
        self.projection_basic = {
            '_id': 0
        }

    # insert post
    def insert__one(self, post_object):
        self.collection.insert(post_object)
        return "success"

    # delete all
    def delete__all(self):
        self.collection.delete_many({})
        return "success"

#posts Table
class BWAI__variable(object):
    def __init__(self, client):
        super(BWAI__variable, self).__init__()
        self.collection = client['variable']

        #Basic projection
        self.projection_basic = {
            '_id': 0
        }

    def update__variable(self, num):
        self.collection.update(
            {
                'key': "num"
            },
            {
                '$set':
                {
                    'len': num
                }
            }
        )
        return "success"