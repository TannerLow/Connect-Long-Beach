class ProfileData():
    fname = None
    lname = None
    major = None
    year = None
    gender = None
    profile_pic = None
    background_pic = None
    interests = []
    courses = []

    def __init__(self):
        pass

    def set_first_name(self, fname):
        self.fname = fname

    def set_last_name(self, lname):
        self.lname = lname

    def set_major(self, major):
        self.major = major

    def set_year(self, year):
        self.year = int(year)

    def set_gender(self, gender):
        self.gender = gender

    def set_profile_pic(self, profile_pic):
        self.profile_pic = profile_pic

    def set_background_pic(self, background_pic):
        self.background_pic = background_pic

    def set_interests(self, interests):
        self.interests = interests

    def set_courses(self, courses):
        self.courses = courses