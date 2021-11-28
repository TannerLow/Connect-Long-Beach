export interface ProfileUpdateData {
    userID: number;
    pathURL: string;
    fname: string;
    lname: string;
    year: number;
    gender: string;
    major: string;
    profilePic: string;
    backgroundPic: string;
    interests: string[];
    courses: string[];
}